from typing import Dict, Any, List, Optional
import requests
import json
from .base import BaseIntegration

class CustomIntegration(BaseIntegration):
    """
    Custom API integration that can be configured for various services
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.endpoints = config.get('endpoints', {})
        self.headers = config.get('headers', {})
        self.auth_type = config.get('auth_type', 'Bearer')
        self.rate_limit = config.get('rate_limit', None)
        self.timeout = config.get('timeout', 30)
        self.retry_attempts = config.get('retry_attempts', 3)
        
        # Set up authentication headers
        if self.api_key:
            if self.auth_type == 'Bearer':
                self.headers['Authorization'] = f'Bearer {self.api_key}'
            elif self.auth_type == 'Api-Key':
                self.headers['Api-Key'] = self.api_key
            elif self.auth_type == 'X-Api-Key':
                self.headers['X-Api-Key'] = self.api_key
            else:
                self.headers[self.auth_type] = self.api_key

    def validate_credentials(self) -> bool:
        """Validate the API credentials using the test endpoint"""
        test_endpoint = self.endpoints.get('test')
        if not test_endpoint:
            return True  # No test endpoint specified, assume valid
        
        try:
            response = requests.get(
                f"{self.base_url}{test_endpoint}",
                headers=self.headers,
                timeout=self.timeout
            )
            return response.status_code == 200
        except Exception:
            return False

    def list_models(self) -> List[Dict[str, Any]]:
        """List available models using the models endpoint"""
        models_endpoint = self.endpoints.get('models')
        if not models_endpoint:
            return list(self.models.values())
        
        try:
            response = requests.get(
                f"{self.base_url}{models_endpoint}",
                headers=self.headers,
                timeout=self.timeout
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return list(self.models.values())

    def generate(self, model_id: str, prompt: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content using the specified model"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        endpoint = model.get('endpoint') or self.endpoints.get('generate')
        
        if not endpoint:
            raise ValueError("No generation endpoint specified")

        # Merge default parameters with custom ones
        merged_parameters = {
            **model.get('default_parameters', {}),
            **parameters
        }

        # Prepare the request payload
        payload = {
            'model': model_id,
            'prompt': prompt,
            **merged_parameters
        }

        # Custom payload formatting if specified
        if 'payload_format' in model:
            payload = self._format_payload(payload, model['payload_format'])

        for attempt in range(self.retry_attempts):
            try:
                response = requests.post(
                    f"{self.base_url}{endpoint}",
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return self._format_response(result, model.get('response_format'))
                
                error_msg = response.text
                raise Exception(f"API Error: {error_msg}")
            
            except Exception as e:
                if attempt == self.retry_attempts - 1:
                    raise e
                import time
                time.sleep(2 ** attempt)  # Exponential backoff

    def _format_payload(self, payload: Dict[str, Any], format_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Format the payload according to the API's requirements"""
        formatted = {}
        
        for key, value in format_spec.items():
            if isinstance(value, str):
                # Handle string templates
                if value.startswith('$'):
                    source_key = value[1:]
                    formatted[key] = payload.get(source_key)
                else:
                    formatted[key] = value
            elif isinstance(value, dict):
                # Handle nested structures
                formatted[key] = self._format_payload(payload, value)
            elif isinstance(value, list):
                # Handle arrays
                formatted[key] = [
                    self._format_payload(payload, item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                formatted[key] = value
                
        return formatted

    def _format_response(self, response: Dict[str, Any], format_spec: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format the API response according to our standard format"""
        if not format_spec:
            return response
            
        formatted = {}
        
        for key, path in format_spec.items():
            value = response
            for part in path.split('.'):
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    value = None
                if value is None:
                    break
            formatted[key] = value
            
        return formatted

    def add_model(self, model_id: str, model_config: Dict[str, Any]) -> None:
        """Add a new model configuration"""
        if model_id in self.models:
            raise ValueError(f"Model {model_id} already exists")
        
        required_fields = {'name', 'description', 'type'}
        if not all(field in model_config for field in required_fields):
            raise ValueError(f"Model config must include: {required_fields}")
        
        self.models[model_id] = model_config

    def remove_model(self, model_id: str) -> bool:
        """Remove a model configuration"""
        if model_id in self.models:
            del self.models[model_id]
            return True
        return False

    def update_model(self, model_id: str, model_config: Dict[str, Any]) -> None:
        """Update an existing model configuration"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        self.models[model_id].update(model_config)
