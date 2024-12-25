from typing import Dict, Any, List, Optional
import json
from datetime import datetime
from integrations.base import BaseIntegration

class UnifiedAPI:
    """
    Unified API system that manages multiple API integrations
    """
    
    def __init__(self):
        self.integrations: Dict[str, BaseIntegration] = {}
        self.max_integrations = 200
        self._load_integrations()

    def _load_integrations(self) -> None:
        """Load saved integrations from storage"""
        # TODO: Implement persistent storage
        pass

    def add_integration(self, integration_id: str, integration: BaseIntegration) -> bool:
        """Add a new API integration"""
        if len(self.integrations) >= self.max_integrations:
            raise ValueError(f"Maximum number of integrations ({self.max_integrations}) reached")
        
        if integration_id in self.integrations:
            raise ValueError(f"Integration with ID {integration_id} already exists")
        
        self.integrations[integration_id] = integration
        return True

    def remove_integration(self, integration_id: str) -> bool:
        """Remove an API integration"""
        if integration_id in self.integrations:
            del self.integrations[integration_id]
            return True
        return False

    def get_integration(self, integration_id: str) -> Optional[BaseIntegration]:
        """Get an integration by ID"""
        return self.integrations.get(integration_id)

    def list_integrations(self) -> List[Dict[str, Any]]:
        """List all registered integrations"""
        return [
            {
                'id': integration_id,
                **integration.to_dict()
            }
            for integration_id, integration in self.integrations.items()
        ]

    def generate(self, integration_id: str, model_id: str, prompt: str, 
                parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate content using a specific integration and model"""
        integration = self.get_integration(integration_id)
        if not integration:
            raise ValueError(f"Integration {integration_id} not found")

        if not parameters:
            parameters = {}

        try:
            result = integration.generate(model_id, prompt, parameters)
            return {
                'status': 'success',
                'integration_id': integration_id,
                'model_id': model_id,
                'result': result,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                'status': 'error',
                'integration_id': integration_id,
                'model_id': model_id,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }

    def validate_all_credentials(self) -> Dict[str, bool]:
        """Validate credentials for all integrations"""
        results = {}
        for integration_id, integration in self.integrations.items():
            try:
                results[integration_id] = integration.validate_credentials()
            except Exception:
                results[integration_id] = False
        return results

    def get_available_models(self, integration_id: str = None) -> Dict[str, List[Dict[str, Any]]]:
        """Get available models, optionally filtered by integration"""
        if integration_id:
            integration = self.get_integration(integration_id)
            if not integration:
                raise ValueError(f"Integration {integration_id} not found")
            return {integration_id: integration.models}
        
        return {
            integration_id: integration.models
            for integration_id, integration in self.integrations.items()
        }

    def to_json(self) -> str:
        """Export all integrations to JSON"""
        export_data = {
            'integrations': {
                integration_id: integration.to_dict()
                for integration_id, integration in self.integrations.items()
            },
            'max_integrations': self.max_integrations,
            'exported_at': datetime.utcnow().isoformat()
        }
        return json.dumps(export_data, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'UnifiedAPI':
        """Create UnifiedAPI instance from JSON export"""
        data = json.loads(json_str)
        api = cls()
        api.max_integrations = data.get('max_integrations', 200)
        
        for integration_id, integration_data in data.get('integrations', {}).items():
            # TODO: Implement integration loading from data
            pass
        
        return api
