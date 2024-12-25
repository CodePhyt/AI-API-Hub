from flask import Flask, render_template, request, jsonify, session
from integrations.custom_integration import CustomIntegration
from api.unified import UnifiedAPI

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Initialize the UnifiedAPI
unified_api = UnifiedAPI()

# Provider configurations
providers = {
    'huggingface': {
        'name': 'Hugging Face',
        'icon': 'fa-robot',
        'requires_api_key': True,
        'api_key_name': 'HUGGINGFACE_API_KEY'
    },
    'openai': {
        'name': 'OpenAI',
        'icon': 'fa-brain',
        'requires_api_key': True,
        'api_key_name': 'OPENAI_API_KEY'
    },
    'stability': {
        'name': 'Stability AI',
        'icon': 'fa-palette',
        'requires_api_key': True,
        'api_key_name': 'STABILITY_API_KEY'
    },
    'custom': {
        'name': 'Custom API',
        'icon': 'fa-gear',
        'requires_api_key': True,
        'api_key_name': 'CUSTOM_API_KEY'
    }
}

@app.route('/')
def index():
    integrations = unified_api.list_integrations()
    return render_template('index.html', 
                         providers=providers,
                         integrations=integrations)

@app.route('/api/integrations', methods=['GET'])
def list_integrations():
    return jsonify(unified_api.list_integrations())

@app.route('/api/integrations', methods=['POST'])
def add_integration():
    data = request.json
    integration_id = data.get('integration_id')
    config = data.get('config', {})
    
    try:
        integration = CustomIntegration(config)
        unified_api.add_integration(integration_id, integration)
        return jsonify({'status': 'success', 'message': 'Integration added'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    integration_id = data.get('integration_id')
    model_id = data.get('model_id')
    prompt = data.get('prompt')
    parameters = data.get('parameters', {})

    try:
        result = unified_api.generate(integration_id, model_id, prompt, parameters)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/models', methods=['GET'])
def list_models():
    integration_id = request.args.get('integration_id')
    try:
        models = unified_api.get_available_models(integration_id)
        return jsonify({'status': 'success', 'models': models})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/key', methods=['POST'])
def update_api_key():
    data = request.json
    provider = data.get('provider')
    api_key = data.get('api_key')
    
    if not provider or not api_key:
        return jsonify({'status': 'error', 'message': 'Missing provider or API key'}), 400
    
    session[f'{provider}_api_key'] = api_key
    return jsonify({'status': 'success', 'message': 'API key updated'})

@app.route('/api/validate', methods=['POST'])
def validate_credentials():
    data = request.json
    integration_id = data.get('integration_id')
    integration = unified_api.get_integration(integration_id)
    if not integration:
        return jsonify({'status': 'error', 'message': 'Integration not found'}), 404
    
    is_valid = integration.validate_credentials()
    return jsonify({'status': 'success', 'valid': is_valid})

if __name__ == '__main__':
    app.run(debug=True)