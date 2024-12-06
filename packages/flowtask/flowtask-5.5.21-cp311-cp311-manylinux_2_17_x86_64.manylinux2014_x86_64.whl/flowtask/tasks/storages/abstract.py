from typing import Any
from pathlib import PurePath
from abc import ABC, abstractmethod
from navconfig.logging import logging


class AbstractTaskStorage(ABC):
    def __init__(self, *args, **kwargs) -> None:
        self.path: PurePath = None
        self.logger = logging.getLogger("FlowTask.Task.Storage")

    def get_path(self) -> PurePath:
        return self.path

    @abstractmethod
    async def open_task(self, task: str, program: str = None, **kwargs) -> Any:
        """open_task.
        Open A Task from Task Storage, support JSON, YAML and TOML formats.
        """
