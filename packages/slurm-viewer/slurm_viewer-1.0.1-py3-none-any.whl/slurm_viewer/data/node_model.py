""" Pydantic model for capturing SLURM node information. """
from __future__ import annotations

import datetime
import re
from enum import Enum
from typing import Any

import dateutil.parser
from typing_extensions import Annotated

from pydantic import BaseModel, Field, AliasChoices, field_validator, computed_field, ConfigDict

from slurm_viewer.data.common_types import MemoryUsed

CFGTRESS_RE = r'^cpu=(?P<cpu>\d+),mem=(?P<mem>\d+\w),billing=(?P<billing>\d+),gres/gpu=(?P<gpu>\d+)$'
ALLOCTRESS_RE = (r'^cpu=(?P<cpu>\d+),mem=(?P<mem>\d+\w)(?:,gres/gpu=(?P<gpu_alloc>\d+))'
                 r'(?:,gres/gpu:(?P<gpu_type>\S+)=(?P<gpu_total>\d+))?$')


class State(Enum):
    """ Node state """
    IDLE = 'IDLE'
    DOWN = 'DOWN'
    MIXED = 'MIXED'
    ALLOCATED = 'ALLOCATED'
    DRAIN = 'DRAIN'
    MAINTENANCE = 'MAINTENANCE'
    RESERVED = 'RESERVED'
    NOT_RESPONDING = 'NOT_RESPONDING'
    PLANNED = 'PLANNED'
    COMPLETING = 'COMPLETING'
    REBOOT_REQUESTED = 'REBOOT_REQUESTED'
    INVALID_REG = 'INVALID_REG'


class CfgTRES(BaseModel):
    """ Configured Trackable Resources """
    cpu: int = -1
    mem: str = 'NA'
    billing: int = -1
    gpu: int = -1


class AllocTRES(BaseModel):
    """ Allocated Trackable Resources """
    cpu: int = -1
    mem: str = 'NA'
    gpu_alloc: int | None = None
    gpu_type: str | None = None
    gpu_total: int | None = None


class GPU(BaseModel):
    """ GPU name and count. """
    name: str
    amount: int

    def __str__(self) -> str:
        return f'{self.name}:{self.amount}'


def gpu_mem_from_features(_features: list[str]) -> MemoryUsed | None:
    """ Get the GPU memory from features. """
    for feature in _features:
        m = re.search(r'^.*.(?P<gpu_mem>\d{2,})[Gg]\w*$', feature)
        if m is None:
            continue

        try:
            return MemoryUsed.from_mb(int(m['gpu_mem']) * 1024)
        except ValueError:
            return None

    return None


# See https://github.com/python/mypy/issues/1362
# mypy: disable-error-code="operator, no-any-return"
# pylint: disable=comparison-with-callable,unsupported-membership-test
class Node(BaseModel):
    """ Slurm node model. """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    active_features: list[str]
    alloc_tres: Annotated[AllocTRES, Field(validation_alias=AliasChoices('alloc_tres', 'tres_used'))]
    arch: str = Field(validation_alias=AliasChoices('arch', 'architecture'))
    available_features: Annotated[list[str], Field(validation_alias=AliasChoices('available_features', 'features'))]
    boards: int
    boot_time: datetime.datetime | None
    cfgtres: CfgTRES = Field(validation_alias=AliasChoices('cfgtres', 'tres'))
    cores_per_socket: int = Field(validation_alias=AliasChoices('cores_per_socket', 'cores'))
    cpu_alloc: int = Field(validation_alias=AliasChoices('cpu_alloc', 'alloc_cpus'))
    cpu_efctv: int | None = Field(validation_alias=AliasChoices('cpu_efctv', 'effective_cpus'))
    cpu_tot: int = Field(validation_alias=AliasChoices('cpu_tot', 'cpus'))
    cpuload: float = Field(validation_alias=AliasChoices('cpuload', 'cpu_load'))
    gres: list[GPU]
    last_busy_time: datetime.datetime | None = Field(validation_alias=AliasChoices('last_busy_time', 'last_busy'))
    mcs_label: str
    mem_alloc:  Annotated[MemoryUsed, Field(validation_alias=AliasChoices('alloc_mem', 'alloc_memory'))]
    mem_avail: Annotated[MemoryUsed, Field(validation_alias=AliasChoices('freemem', 'free_mem'))]
    mem_tot: Annotated[MemoryUsed, Field(validation_alias=AliasChoices('realmemory', 'real_memory'))]
    node_addr: str = Field(validation_alias=AliasChoices('node_addr', 'address'))
    node_hostname: str = Field(validation_alias=AliasChoices('node_hostname', 'hostname'))
    node_name: str = Field(validation_alias=AliasChoices('node_name', 'name'), repr=True)
    os: str = Field(validation_alias=AliasChoices('os', 'operating_system'))
    owner: str
    partitions: list[str]
    resume_after_time: datetime.datetime | None = Field(validation_alias=AliasChoices('resume_after_time', 'resume_after'))
    slurmd_start_time: datetime.datetime | None
    sockets: int
    states: Annotated[list[State], Field(alias='state', default_factory=list, description='State of the node.')]
    threads_per_core: int = Field(validation_alias=AliasChoices('threads_per_core', 'threads'))
    tmp_disk: int = Field(validation_alias=AliasChoices('tmp_disk', 'temporary_disk'))
    version: str
    weight: int

    @computed_field(description='Available CPU cores.')
    def cpu_avail(self) -> int:
        return self.cpu_tot - self.cpu_alloc

    @computed_field(description='Total GPUs.')
    def gpu_tot(self) -> int:
        return sum(x.amount for x in self.gres)

    @computed_field(description='Allocated GPUs.')
    def gpu_alloc(self) -> int:
        if self.alloc_tres.gpu_alloc is not None:
            return self.alloc_tres.gpu_alloc
        return 0

    @computed_field(description='Available GPUs.')
    def gpu_avail(self) -> int:
        if self.gres:
            return self.gpu_tot - self.gpu_alloc
        return 0

    @computed_field(description='GPU type.')
    def gpu_type(self) -> str:
        return ','.join(sorted({x.name for x in self.gres}))

    @computed_field(description='Amount of GPU memory (GB)')
    def gpu_mem(self) -> MemoryUsed | str:
        mem = gpu_mem_from_features(self.available_features)
        if mem is not None:
            return mem

        # Dirty fix for Alice
        if '2080' in self.gpu_type:
            return MemoryUsed.from_mb(11 * 1024)

        if self.gpu_type == 'tesla_t4':
            return MemoryUsed.from_mb(16 * 1024)

        return '-'

    @computed_field(description='Number of available CPUs divided by the number of available GPUs.')
    def cpu_gpu(self) -> float | str:
        if self.gpu_avail == 0:
            return '-'
        return self.cpu_avail / self.gpu_avail

    @computed_field(description='Available CPU memory divided by the number of available GPUs.')
    def mem_gpu(self) -> float | str:
        if self.gpu_avail == 0:
            return '-'
        # noinspection PyTypeChecker
        return self.mem_avail.GB / self.gpu_avail

    @computed_field(description='State of the node as a string.')
    def state(self) -> str:
        return ','.join([x.name.lower() for x in self.states])

    @field_validator('resume_after_time', 'boot_time', 'last_busy_time', 'slurmd_start_time', mode='before')
    @classmethod
    def date_validator(cls, value: Any) -> datetime.datetime | None:
        if value is None:
            return None

        if isinstance(value, dict):
            return  datetime.datetime.fromtimestamp(value['number'])

        if isinstance(value, int):
            return datetime.datetime.fromtimestamp(value)

        if not isinstance(value, datetime.datetime) and len(value) > 0:
            return None

        # noinspection PyTypeChecker
        return dateutil.parser.parse(value)

    @field_validator('available_features', 'active_features', 'partitions', mode='before')
    @classmethod
    def list_validator(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        return value.split(',')

    @field_validator('gres', mode='before')
    @classmethod
    def gres_validator(cls, _value: str) -> list[GPU]:
        if len(_value) == 0:
            return []

        if ',' in _value:
            values = _value.split(',')
        else:
            values = [_value]

        gpus = []
        for value in values:
            data = value.split(':')
            if len(data) < 3:
                continue

            name = data[1]
            try:
                num_gpus = int(re.split(r'\D+', data[2])[0])
            except ValueError:
                num_gpus = 0

            # Dirty fix for Alice
            if '4g.40gb' in name:
                name = 'a100_4g'
            if '3g.40gb' in name:
                name = 'a100_3g'
            if name == '1(S':
                name = 'tesla_t4'
                num_gpus = 1
            # End

            gpus.append(GPU(name=name, amount=num_gpus))
        return gpus

    @field_validator('cfgtres', mode='before')
    @classmethod
    def cfgtres_validator(cls, value: str) -> CfgTRES:
        m = re.search(CFGTRESS_RE, value)
        if not m:
            return CfgTRES()

        return CfgTRES(**m.groupdict())

    @field_validator('alloc_tres', mode='before')
    @classmethod
    def alloctres_validator(cls, value: str) -> AllocTRES:
        m = re.search(ALLOCTRESS_RE, value)
        if not m:
            return AllocTRES()

        return AllocTRES(**m.groupdict())

    @field_validator('states', mode='before')
    @classmethod
    def state_validator(cls, value: str | list[str]) -> list[State]:
        if isinstance(value, list):
            return [State(x) for x in value]
        return [State(x) for x in value.split('+')]

    @field_validator('cpuload', mode='before')
    @classmethod
    def cpuload_validator(cls, value: str | dict) -> float:
        if isinstance(value, (int, str)):
            return float(value)

        return float(value['number'])

    @field_validator('mem_avail', 'mem_alloc', 'mem_tot', mode='before')
    @classmethod
    def mem_validator(cls, value: str | int | dict) -> MemoryUsed:
        if isinstance(value, int) or isinstance(value, str):  # pylint: disable=consider-merging-isinstance
            return MemoryUsed.from_mb(int(value))

        return MemoryUsed.from_mb(value['number'])


def create_node(_node_dict: dict, _node_name_ignore_prefix: list[str]) -> Node:
    node = Node(**_node_dict)
    for ignore_prefix in _node_name_ignore_prefix:
        if node.node_name.startswith(ignore_prefix):
            node.node_name = node.node_name.removeprefix(ignore_prefix)
            break
    return node
