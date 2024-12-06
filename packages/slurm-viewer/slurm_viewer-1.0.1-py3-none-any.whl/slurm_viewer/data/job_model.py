from __future__ import annotations

import datetime
import re

from pydantic import BaseModel, ConfigDict, field_validator

from slurm_viewer.data.common_types import MemoryUsed, CPU_TIME_RE, PostFixUnit
from slurm_viewer.data.queue_model import JobStateCodes

TRES_USAGE_IN_AVE_RE = (r'^cpu=(?P<cpu>(?:\d+-)?\d+:\d+:\d+),energy=(?P<energy>\d+),fs/disk=(?P<disk>\d+),'
                        r'gres/gpumem=(?P<gpu_mem>\w+),gres/gpuutil=(?P<gpu_util>\d+),mem=(?P<mem>\d+K),'
                        r'pages=(?P<pages>\d+),vmem=(?P<vmem>\d+K)$')


class ExitCodeSignal:  # pylint: disable=too-few-public-methods
    def __init__(self, value: str) -> None:
        self.code: int | None = None
        self.signal: int | None = None

        if len(value) == 0:
            return

        data = value.split(':')
        if len(data) == 2:
            self.code = int(data[0])
            self.signal = int(data[1])
            return

        if len(data) == 1:
            self.code = int(data[0])
            self.signal = None
            return

    def __repr__(self) -> str:
        return f'{self.code}'


class TrackableResourceUsage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cpu: datetime.timedelta | None = None
    energy: int | None = None
    disk: MemoryUsed | None = None
    gpu_mem: MemoryUsed | None = None
    gpu_util: int | None = None
    mem: MemoryUsed | None = None
    pages: int | None = None
    vmem: MemoryUsed | None = None

    @field_validator('cpu', mode='before')
    @classmethod
    def timedelta_validator(cls, value: str) -> datetime.timedelta:
        m = re.search(CPU_TIME_RE, value)
        if not m:
            return datetime.timedelta(0)

        return datetime.timedelta(**{k: float(v) for k, v in m.groupdict().items() if v is not None})

    @field_validator('gpu_mem', 'mem', 'vmem', 'disk', mode='before')
    @classmethod
    def mem_validator(cls, value: str) -> MemoryUsed:
        return MemoryUsed(value)


class ReqAllocTrackableResources(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cpu: int | None = None
    mem: MemoryUsed | None = None
    billing: int | None = None
    gpu: int | None = None
    gpu_name: str | None = None
    node: int | None = None
    energy: int | None = None

    @field_validator('mem', mode='before')
    @classmethod
    def mem_validator(cls, value: str) -> MemoryUsed:
        return MemoryUsed(value)


class Job(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    JobID: str
    JobIDRaw: str
    JobName: str
    Partition: str
    MaxVMSize: MemoryUsed
    MaxVMSizeNode: str
    MaxVMSizeTask: str
    AveVMSize: MemoryUsed
    MaxRSS: MemoryUsed
    MaxRSSNode: str
    MaxRSSTask: str
    AveRSS: MemoryUsed
    MaxPages: str
    MaxPagesNode: str
    MaxPagesTask: str
    AvePages: str
    MinCPU: datetime.timedelta
    MinCPUNode: str
    MinCPUTask: str
    AveCPU: datetime.timedelta
    NTasks: str
    AllocCPUS: int
    Elapsed: datetime.timedelta
    State: JobStateCodes
    ExitCode: ExitCodeSignal
    AveCPUFreq: PostFixUnit
    ReqCPUFreqMin: PostFixUnit
    ReqCPUFreqMax: PostFixUnit
    ReqCPUFreqGov: PostFixUnit
    ReqMem: MemoryUsed
    ConsumedEnergy: PostFixUnit
    MaxDiskRead: MemoryUsed
    MaxDiskReadNode: str
    MaxDiskReadTask: str
    AveDiskRead: MemoryUsed
    MaxDiskWrite: MemoryUsed
    MaxDiskWriteNode: str
    MaxDiskWriteTask: str
    AveDiskWrite: MemoryUsed
    ReqTRES: ReqAllocTrackableResources
    AllocTRES: ReqAllocTrackableResources
    TRESUsageInAve: TrackableResourceUsage
    TRESUsageInMin: TrackableResourceUsage
    TRESUsageInMax: TrackableResourceUsage
    TRESUsageInTot: TrackableResourceUsage
    TRESUsageInMaxNode: str
    TRESUsageInMaxTask: str
    TRESUsageInMinNode: str
    TRESUsageInMinTask: str
    TRESUsageOutMaxNode: str
    TRESUsageOutMaxTask: str
    TRESUsageOutMax: str
    TRESUsageOutAve: str
    TRESUsageOutTot: str

    @field_validator('TRESUsageInAve', 'TRESUsageInMax', 'TRESUsageInMin', 'TRESUsageInTot', mode='before')
    @classmethod
    def tres_usage_in_ave_validator(cls, value: str) -> TrackableResourceUsage:
        m = re.search(TRES_USAGE_IN_AVE_RE, value)
        if not m:
            return TrackableResourceUsage()

        return TrackableResourceUsage(**m.groupdict())

    @field_validator('ReqTRES', 'AllocTRES', mode='before')
    @classmethod
    def req_alloc_tres_validator(cls, value: str) -> ReqAllocTrackableResources:
        if len(value) == 0:
            return ReqAllocTrackableResources()

        data = {}
        for key_values in value.split(','):
            key, value = key_values.split('=', maxsplit=1)
            if key == 'gres/gpu':
                key = 'gpu'
            if key.startswith('gres/gpu:'):
                value = key.split(':')[-1]
                key = 'gpu_name'
            data[key] = value

        return ReqAllocTrackableResources(**data)

    @field_validator('State', mode='before')
    @classmethod
    def state_validator(cls, value: str) -> JobStateCodes:
        return JobStateCodes(value.split()[0])

    @field_validator('ExitCode', mode='before')
    @classmethod
    def exit_code_validator(cls, value: str) -> ExitCodeSignal:
        return ExitCodeSignal(value)

    @field_validator('ReqMem', 'AveDiskWrite', 'AveDiskRead', 'MaxDiskWrite', 'MaxDiskRead', 'MaxVMSize', 'AveVMSize',
                     'AveRSS', 'MaxRSS', mode='before')
    @classmethod
    def mem_validator(cls, value: str) -> MemoryUsed:
        return MemoryUsed(value)

    @field_validator('AveCPUFreq', 'ReqCPUFreqMin', 'ReqCPUFreqMax', 'ReqCPUFreqGov', 'ConsumedEnergy', mode='before')
    @classmethod
    def post_fix_validator(cls, value: str) -> PostFixUnit:
        return PostFixUnit(value)

    @field_validator('Elapsed', 'MinCPU', 'AveCPU', mode='before')
    @classmethod
    def timedelta_validator(cls, value: str) -> datetime.timedelta:
        m = re.search(CPU_TIME_RE, value)
        if not m:
            return datetime.timedelta(0)

        return datetime.timedelta(**{k: float(v) for k, v in m.groupdict().items() if v is not None})

    def __repr__(self) -> str:
        return f'{self.JobID=}, {self.JobName=}, {self.State=}'
