"""
Utility functions for the IBM Quantum Circuit JOB Automation application
"""

import streamlit as st
from datetime import datetime
import pandas as pd
from config import DEFAULT_QASM, DEFAULT_SHOTS, DEFAULT_JOBS_COUNT

# Check library availability
def check_qiskit():
    """Check if Qiskit is available"""
    try:
        from qiskit import QuantumCircuit
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
        return True
    except ImportError:
        return False

def check_groq():
    """Check if Groq is available"""
    try:
        from groq import Groq
        return True
    except ImportError:
        return False

def init_session_state():
    """Initialize Streamlit session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_qasm' not in st.session_state:
        st.session_state.current_qasm = DEFAULT_QASM
    if 'shots' not in st.session_state:
        st.session_state.shots = DEFAULT_SHOTS
    if 'jobs_count' not in st.session_state:
        st.session_state.jobs_count = DEFAULT_JOBS_COUNT
    if 'results_data' not in st.session_state:
        st.session_state.results_data = []
    if 'job_running' not in st.session_state:
        st.session_state.job_running = False

def validate_qasm(qasm_code):
    """Validate QASM code"""
    if not check_qiskit():
        return False, "Qiskit not available"
    
    try:
        from qiskit import QuantumCircuit
        qc = QuantumCircuit.from_qasm_str(qasm_code)
        return True, f"Circuit: {qc.num_qubits} qubits, {qc.depth()} depth"
    except Exception as e:
        return False, str(e)

def format_timestamp():
    """Get formatted timestamp for file names"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def calculate_success_metrics(results_df):
    """Calculate success metrics from results dataframe"""
    if results_df.empty:
        return 0, 0, 0
    
    total_shots = sum(results_df['count0'] + results_df['count1'])
    total_1s = sum(results_df['count1'])
    success_rate = (total_1s / total_shots * 100) if total_shots > 0 else 0
    
    return total_shots, total_1s, success_rate

def add_message_to_chat(role, content):
    """Add a message to chat history"""
    st.session_state.chat_history.append({
        "role": role,
        "content": content
    })

def clear_chat_history():
    """Clear the chat history"""
    st.session_state.chat_history = []

def get_results_csv(results_data):
    """Convert results data to CSV format"""
    if not results_data:
        return ""
    
    df = pd.DataFrame(results_data)
    return df.to_csv(index=False)