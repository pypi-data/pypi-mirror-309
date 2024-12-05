from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    """Base class that all AIHive tools must implement."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the tool."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the tool does."""
        pass
    
    @abstractmethod
    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        """Execute the tool's main functionality."""
        pass
