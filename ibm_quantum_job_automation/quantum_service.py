"""
Quantum computing service for executing circuits on IBM Quantum backends
"""

import streamlit as st
from datetime import datetime
from utils import check_qiskit

def execute_quantum_circuit(qasm_code, ibm_api_key, backend_name, shots, jobs_count):
    """Execute the quantum circuit on IBM Quantum backend"""
    if not check_qiskit():
        return [], "Qiskit not available"
    
    try:
        # Import Qiskit components
        from qiskit import QuantumCircuit
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
        
        # Authenticate with IBM Quantum
        service = QiskitRuntimeService(channel="ibm_cloud", token=ibm_api_key)
        
        # Load QASM circuit
        qc = QuantumCircuit.from_qasm_str(qasm_code)
        
        # Choose backend
        backend = service.backend(backend_name)
        
        # Initialize sampler
        sampler = Sampler(backend)
        
        # Store results
        results_data = []
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for job_idx in range(jobs_count):
            status_text.text(f"Running Job {job_idx + 1}/{jobs_count}...")
            progress_bar.progress((job_idx + 1) / jobs_count)
            
            # Run the circuit
            job = sampler.run([qc], shots=shots)
            result = job.result()
            
            job_id = job.job_id()
            
            # Extract results
            pub_result = result[0]
            counts = pub_result.data.c.get_counts()
            
            # Get counts for each bit value
            count_0 = counts.get('0', 0)
            count_1 = counts.get('1', 0)
            
            # Append to results list
            results_data.append({
                'job_id': job_id,
                'idx': job_idx,
                'circ_name': 'quantum_circuit',
                'bit1': '1',
                'count1': count_1,
                'bit0': '0',
                'count0': count_0,
                'shots': shots,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        progress_bar.empty()
        status_text.empty()
        
        return results_data, "Success"
        
    except Exception as e:
        return [], f"Error: {str(e)}"

def get_backend_status(ibm_api_key, backend_name):
    """Get status of the selected backend"""
    if not check_qiskit():
        return "Unknown - Qiskit not available"
    
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
        
        service = QiskitRuntimeService(channel="ibm_cloud", token=ibm_api_key)
        backend = service.backend(backend_name)
        
        # Get backend properties
        status = backend.status()
        return f"Available ({status.pending_jobs} pending jobs)"
        
    except Exception as e:
        return f"Error: {str(e)}"