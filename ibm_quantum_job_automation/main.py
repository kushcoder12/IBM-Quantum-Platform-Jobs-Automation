"""
Main application file for IBM Quantum Circuit JOB Automation
Run with: streamlit run main.py
"""

import streamlit as st
from config import PAGE_CONFIG
from styles import CUSTOM_CSS
from utils import init_session_state, check_qiskit, check_groq
from ui_components import (
    render_header, render_api_keys_section, render_circuit_parameters,
    render_qasm_editor, render_execution_section, render_results_section,
    render_chat_interface, render_quick_actions, render_status_indicators,
    render_footer
)

def check_dependencies():
    """Check and display dependency status"""
    if not check_qiskit():
        st.error("⚠️ Qiskit not installed. Please install: pip install qiskit qiskit-ibm-runtime")
    
    if not check_groq():
        st.error("⚠️ Groq not installed. Please install: pip install groq")

def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(**PAGE_CONFIG)
    
    # Apply custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()
    
    # Check dependencies
    check_dependencies()
    
    # Render header
    render_header()
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 2])
    
    # Left Column - Configuration and Controls
    with col1:
        st.header("🔧 Configuration")
        
        # API Keys Section
        ibm_api_key, groq_api_key = render_api_keys_section()
        
        # Circuit Parameters
        backend_name = render_circuit_parameters()
        
        # QASM Code Editor
        render_qasm_editor()
        
        # Execute Circuit
        render_execution_section(ibm_api_key, backend_name)
        
        # Results Section
        render_results_section()
    
    # Right Column - AI Chat Interface
    with col2:
        # Chat Interface
        render_chat_interface(groq_api_key)
        
        # Quick Actions
        render_quick_actions(groq_api_key)
        
        # Status indicators
        render_status_indicators(ibm_api_key, groq_api_key)
    
    # Footer
    render_footer()

if __name__ == "__main__":
    main()