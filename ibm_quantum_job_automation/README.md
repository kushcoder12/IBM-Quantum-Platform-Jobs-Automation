# IBM Quantum Circuit JOB Automation

A Streamlit application for creating, modifying, and executing multiple jobs for quantum circuits on IBM Quantum backends with AI assistance.

## Features

- 🚀 Execute multiple quantum jobs automatically
- 🤖 AI-powered QASM code generation and assistance
- 📊 Real-time results tracking and visualization
- 💾 Export results to CSV
- 🔧 Interactive QASM code editor with validation
- ⚡ Quick action templates for common quantum circuits

## Project Structure

```
├── main.py                 # Main application entry point
├── config.py              # Configuration settings and constants
├── styles.py              # CSS styles for the UI
├── utils.py               # Utility functions
├── quantum_service.py     # Quantum computing service
├── llm_service.py         # LLM integration service
├── ui_components.py       # UI component functions
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   streamlit run main.py
   ```

2. Configure your API keys:
   - **IBM Quantum API Token**: Get from [IBM Quantum Platform](https://quantum-computing.ibm.com/)
   - **Groq API Key**: Get from [Groq Console](https://console.groq.com/)

3. Create or modify QASM circuits using the editor or AI assistant

4. Configure circuit parameters (backend, shots, number of jobs)

5. Execute your quantum circuits and download results

## API Keys Required

- **IBM Quantum**: For executing circuits on real quantum hardware
- **Groq**: For AI-powered quantum computing assistance

## Supported IBM Quantum Backends

- ibm_brisbane
- ibm_lagos
- ibm_perth
- ibm_kyoto

## File Descriptions

### `main.py`
Main application entry point that orchestrates the entire application flow.

### `config.py`
Contains all configuration constants, default values, and settings including:
- Default QASM circuit templates
- IBM Quantum backend options
- LLM system prompts
- UI configuration parameters

### `styles.py`
CSS styling definitions for the Streamlit interface including:
- Chat message styling
- Status indicators
- Main header design
- Container layouts

### `utils.py`
Utility functions for common operations:
- Session state initialization
- QASM code validation
- Library availability checks
- Data processing and formatting
- Chat history management

### `quantum_service.py`
Quantum computing service layer handling:
- IBM Quantum authentication
- Circuit execution on quantum backends
- Job management and progress tracking
- Results collection and formatting

### `llm_service.py`
LLM integration service for AI assistance:
- Groq API communication
- Quantum computing context awareness
- Quick action processing
- QASM code extraction from responses

### `ui_components.py`
Modular UI components including:
- API key input sections
- Circuit parameter controls
- QASM code editor
- Chat interface
- Results display
- Status indicators

## Security Notes

- Never commit API keys to version control
- Store API keys securely using environment variables or Streamlit secrets
- Keep your IBM Quantum and Groq API keys private

## Contributing

1. Follow the modular structure when adding new features
2. Add new configuration to `config.py`
3. Create reusable UI components in `ui_components.py`
4. Keep business logic separate in service files
5. Update requirements.txt for new dependencies

## License

This project is provided as-is for educational and research purposes.

## Support

For issues related to:
- **IBM Quantum**: Check the [IBM Quantum documentation](https://docs.quantum-computing.ibm.com/)
- **Groq API**: Check the [Groq documentation](https://console.groq.com/docs)
- **Streamlit**: Check the [Streamlit documentation](https://docs.streamlit.io/)
