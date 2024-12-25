from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import json

class BaseIntegration(ABC):
    """Base class for all API integrations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get('name', '')
        self.description = config.get('description', '')
        self.api_key = config.get('api_key', '')
        self.base_url = config.get('base_url', '')
        self.models = config.get('models', {})
        self.custom_parameters = config.get('custom_parameters', {})

    @abstractmethod
    def validate_credentials(self) -> bool:
        """Validate the API credentials"""
        pass

    @abstractmethod
    def list_models(self) -> List[Dict[str, Any]]:
        """List available models for this integration"""
        pass

    @abstractmethod
    def generate(self, model_id: str, prompt: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content using the specified model"""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert integration config to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'base_url': self.base_url,
            'models': self.models,
            'custom_parameters': self.custom_parameters,
            'has_api_key': bool(self.api_key)
        }

    @classmethod
    def from_json(cls, json_str: str) -> 'BaseIntegration':
        """Create integration instance from JSON string"""
        config = json.loads(json_str)
        return cls(config)

    def update_config(self, new_config: Dict[str, Any]) -> None:
        """Update integration configuration"""
        self.config.update(new_config)
        self.__init__(self.config)
