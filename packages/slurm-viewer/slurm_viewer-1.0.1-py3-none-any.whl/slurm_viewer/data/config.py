from __future__ import annotations

import enum
import os
import platform
from pathlib import Path
from typing import cast

import tomlkit
from pydantic import BaseModel, field_validator, Field, AliasChoices


def get_config_filename(filename: Path) -> Path:
    if 'SLURM_VIEW_CONFIG' in os.environ:
        filename = Path(os.environ['SLURM_VIEW_CONFIG'])
        if filename.exists():
            return filename

    if filename.exists():
        return filename

    filename = Path.home() / '.config/slurm-viewer/settings.toml'
    if filename.exists():
        return filename

    raise RuntimeError('Settings file could not be found. ')


class Tabs(str, enum.Enum):
    NODES = 'nodes'
    JOBS = 'jobs'
    GPU = 'gpu'
    PRIORITY = 'priority'


class Cluster(BaseModel):
    servers: list[str] = Field(default=[], validation_alias=AliasChoices('server', 'servers'))
    name: str = 'Local'
    node_name_ignore_prefix: list[str] = []
    partitions: list[str] = []
    tabs: list[Tabs] = [Tabs.NODES, Tabs.JOBS, Tabs.GPU]

    # TOML doesn't support None, so have to check it here.
    @field_validator('servers', mode='before')
    @classmethod
    def server_validator(cls, value: str | list[str] | None) -> list[str]:
        if value is None or value == 'None':
            return []

        if isinstance(value, str):
            return [value]

        return value


class UiSettings(BaseModel):
    node_columns: list[str] = []
    queue_columns: list[str] = []
    priority_columns: list[str] = []
    auto_refresh: bool = False
    refresh_interval: int = 30  # seconds


class Config(BaseModel):
    clusters: list[Cluster] = []
    ui: UiSettings = UiSettings()

    @classmethod
    def init(cls) -> Config:
        return Config.load(get_config_filename(Path('settings.toml')))

    @classmethod
    def load(cls, _filename: Path | str) -> Config:
        if not Path(_filename).exists():
            raise RuntimeError(f'Settings file "{Path(_filename).absolute().resolve()}" does not exist.')

        with Path(_filename).open('r', encoding='utf-8') as settings_file:
            setting = Config(**cast(dict, tomlkit.loads(settings_file.read())))

        return setting

    def get_cluster(self, name: str) -> Cluster | None:
        for cluster in self.clusters:
            if cluster.name == name:
                return cluster

        return None


def create_default_config() -> None:
    config = Config()
    config.ui.node_columns = [
        "node_name",
        "state",
        "gpu_tot",
        "gpu_alloc",
        "gpu_avail",
        "gpu_type",
        "gpu_mem",
        "cpu_tot",
        "cpu_alloc",
        "cpu_avail",
        "mem_tot",
        "mem_avail",
        "cpu_gpu",
        "mem_gpu",
        "cpuload",
        "partitions",
        "active_features"
    ]
    config.ui.queue_columns = [
        "user",
        "job_id",
        "reason",
        "exec_host",
        "start_time",
        "submit_time",
        "start_delay",
        "run_time",
        "time_limit",
        "command",
        "work_dir"
    ]
    config.ui.priority_columns = [
        "user_name",
        "job_id",
        "job_priority_n",
        "age_n",
        "fair_share_n",
        "partition_name"
    ]

    config.clusters.append(Cluster())

    config_path = Path('~/.config/slurm-viewer/settings.toml').expanduser().resolve()
    config_path.parent.mkdir(exist_ok=True)

    if config_path.exists():
        overwrite = input('Config file already exists, overwrite? [Y/n] ')
        if overwrite.lower() == 'n':
            print(f'Skipping config file generation, file already exists: {config_path}')
            return

    with open(config_path, 'w', encoding='utf-8') as settings_file:
        doc = tomlkit.document()
        ui = tomlkit.table()
        ui.update(**config.ui.model_dump())
        doc['ui'] = ui

        clusters = tomlkit.aot()
        cluster = Cluster(name=platform.node()).model_dump()
        cluster['servers'] = 'None'
        cluster['tabs'] = ['nodes', 'jobs']
        clusters.append(tomlkit.item(cluster))
        doc['clusters'] = clusters

        tomlkit.dump(doc, settings_file, sort_keys=True)
    print(f'Config file generated: {config_path}')


if __name__ == '__main__':
    create_default_config()
