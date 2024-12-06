from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from ..dataloader import DataLoader, LOGGER


class SetupPipelineStep(ABC):
    @abstractmethod
    def setup(
        self,
        dataloader: DataLoader,
        previous_step: Optional[SetupPipelineStep] = None,
        force: bool = False,
    ):
        pass


__all__ = ["SetupPipelineStep", "DataLoader", "LOGGER"]
