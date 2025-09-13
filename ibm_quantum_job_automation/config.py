"""
Configuration file for IBM Quantum Circuit JOB Automation
Contains all constants, default values, and configuration settings
"""

# Default QASM circuit
DEFAULT_QASM = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
x q[0];
measure q[0] -> c[0];"""

# Default parameters
DEFAULT_SHOTS = 1024
DEFAULT_JOBS_COUNT = 10

# Available IBM Quantum backends
IBM_BACKENDS = [
    "ibm_brisbane", 
    "ibm_lagos", 
    "ibm_perth", 
    "ibm_kyoto"
]

# LLM System prompt for quantum computing assistance
LLM_SYSTEM_PROMPT = """You are a quantum computing assistant helping users create and modify QASM code for quantum circuits. 

You can help users with:
1. Creating QASM 2.0 code for quantum circuits
2. Modifying existing QASM code
3. Suggesting optimal shot counts and job parameters
4. Explaining quantum circuits and operations

When providing QASM code, always use proper QASM 2.0 format starting with:
OPENQASM 2.0;
include "qelib1.inc";

Keep responses concise and focused on quantum computing topics."""

# Quick action prompts
QUICK_ACTIONS = {
    "bell_state": "Generate QASM code for a Bell state (|00⟩ + |11⟩)/√2 using two qubits",
    "random_circuit": "Generate a random quantum circuit with 2-3 qubits using different gates like H, X, Y, Z, CNOT"
}

# UI Configuration
PAGE_CONFIG = {
    "page_title": "IBM Quantum Circuit JOB Automation",
    "page_icon": "⚛️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Model configuration for Groq
GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_TEMPERATURE = 0.7
GROQ_MAX_TOKENS = 1000