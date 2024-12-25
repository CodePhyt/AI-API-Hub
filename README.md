# AI Interface Hub

A unified interface for accessing various AI models and services through their APIs. This open-source project provides a clean, user-friendly web interface for interacting with different AI providers while managing your own API keys.

## Features

- **Multiple AI Providers Support**:
  - Hugging Face (Various ML models)
  - OpenAI (GPT-4, DALL-E 3)
  - Stability AI (Stable Diffusion)
  - Anthropic (Claude)
  - Replicate (Open-source models)

- **Model Categories**:
  - Language Models (Chat, Text Generation)
  - Image Generation (Text-to-Image, Image-to-Image)
  - Audio (Text-to-Speech, Music Generation)
  - Video (Text-to-Video)

- **Key Features**:
  - Secure API key management
  - Dark/Light theme support
  - Responsive design
  - Easy-to-use interface
  - Direct access to provider documentation

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-interface-hub.git
cd ai-interface-hub
```

2. Install dependencies:
```bash
pip install flask requests python-dotenv
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## API Key Configuration

1. Click the "API Settings" button in the header
2. For each provider you want to use:
   - Visit their website to obtain an API key
   - Enter the API key in the corresponding provider card
   - Keys are stored securely in your browser session

## Supported APIs

### Hugging Face
- **Website**: [huggingface.co](https://huggingface.co)
- **API Documentation**: [Hugging Face API Docs](https://huggingface.co/docs/api-inference/index)
- **Available Models**: GPT-2, BLOOM, Stable Diffusion, Bark, MusicGen

### OpenAI
- **Website**: [openai.com](https://openai.com)
- **API Documentation**: [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- **Available Models**: GPT-4, DALL-E 3

### Stability AI
- **Website**: [stability.ai](https://stability.ai)
- **API Documentation**: [Stability API Docs](https://platform.stability.ai/docs/api-reference)
- **Available Models**: Stable Diffusion XL

### Anthropic
- **Website**: [anthropic.com](https://anthropic.com)
- **API Documentation**: [Claude API Reference](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- **Available Models**: Claude 2

### Replicate
- **Website**: [replicate.com](https://replicate.com)
- **API Documentation**: [Replicate API Reference](https://replicate.com/docs/reference/http)
- **Available Models**: SDXL Image Mixer, ZeroScope

## Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a new branch for your feature
3. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all the AI providers for their amazing APIs
- Built with Flask and modern web technologies
- Inspired by the need for a unified AI interface
