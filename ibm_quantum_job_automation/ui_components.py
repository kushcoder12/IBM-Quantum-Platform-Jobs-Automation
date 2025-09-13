"""
UI components for the IBM Quantum Circuit JOB Automation application
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from config import IBM_BACKENDS, QUICK_ACTIONS
from utils import (
    validate_qasm, calculate_success_metrics, 
    add_message_to_chat, clear_chat_history, 
    get_results_csv, format_timestamp, check_qiskit, check_groq
)
from llm_service import get_llm_response, process_quick_action
from quantum_service import execute_quantum_circuit

def render_header():
    """Render the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>IBM Quantum Circuit JOB Automation</h1>
        <p>Create, modify, and execute multiple JOBs for quantum circuits with AI assistance</p>
    </div>
    """, unsafe_allow_html=True)

def render_api_keys_section():
    """Render API keys input section"""
    with st.expander("API Keys", expanded=True):
        ibm_api_key = st.text_input(
            "IBM Quantum API Token",
            type="password",
            help="Get your token from: https://quantum-computing.ibm.com/"
        )
        
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Get your key from: https://console.groq.com/"
        )
    
    return ibm_api_key, groq_api_key

def render_circuit_parameters():
    """Render circuit parameters section"""
    with st.expander("⚙️ Circuit Parameters", expanded=True):
        backend_name = st.selectbox(
            "Quantum Backend",
            IBM_BACKENDS,
            help="Choose your IBM Quantum backend"
        )
        
        st.session_state.shots = st.number_input(
            "Shots per Job",
            min_value=100,
            max_value=10000,
            value=st.session_state.shots,
            step=100
        )
        
        st.session_state.jobs_count = st.number_input(
            "Number of Jobs",
            min_value=1,
            max_value=50,
            value=st.session_state.jobs_count
        )
    
    return backend_name

def render_qasm_editor():
    """Render QASM code editor section"""
    with st.expander("QASM Code", expanded=True):
        st.session_state.current_qasm = st.text_area(
            "Current QASM Circuit",
            value=st.session_state.current_qasm,
            height=200,
            help="Edit your QASM 2.0 code here"
        )
        
        # Validate QASM
        if st.button("🔍 Validate QASM"):
            is_valid, message = validate_qasm(st.session_state.current_qasm)
            if is_valid:
                st.success(f"✅ QASM code is valid! {message}")
            else:
                st.error(f"❌ QASM validation failed: {message}")

def render_execution_section(ibm_api_key, backend_name):
    """Render circuit execution section"""
    st.header("Execute")
    
    if st.button("Run Quantum Circuit", disabled=st.session_state.job_running):
        if not ibm_api_key:
            st.error("❌ Please provide IBM Quantum API token")
        else:
            st.session_state.job_running = True
            
            with st.spinner("Executing quantum circuit..."):
                results, status = execute_quantum_circuit(
                    st.session_state.current_qasm,
                    ibm_api_key,
                    backend_name,
                    st.session_state.shots,
                    st.session_state.jobs_count
                )
            
            st.session_state.job_running = False
            
            if status == "Success":
                st.session_state.results_data = results
                st.success(f"✅ Successfully completed {len(results)} jobs!")
            else:
                st.error(f"❌ Execution failed: {status}")

def render_results_section():
    """Render results display section"""
    if st.session_state.results_data:
        st.header("Results")
        
        df = pd.DataFrame(st.session_state.results_data)
        st.dataframe(df, use_container_width=True)
        
        # Download CSV
        csv = get_results_csv(st.session_state.results_data)
        st.download_button(
            label="Download Results CSV",
            data=csv,
            file_name=f"quantum_results_{format_timestamp()}.csv",
            mime="text/csv"
        )
        
        # Quick stats
        total_shots, total_1s, success_rate = calculate_success_metrics(df)
        
        col1a, col1b, col1c = st.columns(3)
        col1a.metric("Total Shots", total_shots)
        col1b.metric("'1' Results", total_1s)
        col1c.metric("Success Rate", f"{success_rate:.1f}%")

def render_chat_interface(groq_api_key):
    """Render AI chat interface"""
    st.header("🤖 AI Assistant Chat")
    
    # Chat History Display
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">👤 You: {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">🤖 Assistant: {message["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat Input
    with st.container():
        user_input = st.text_area(
            "Type your message:",
            placeholder="Ask me about QASM code, quantum circuits, or modifications...",
            height=100,
            key="user_input"
        )
        
        col2a, col2b, col2c = st.columns([1, 1, 2])
        
        with col2a:
            if st.button("Send"):
                if user_input.strip() and groq_api_key:
                    # Add user message to history
                    add_message_to_chat("user", user_input)
                    
                    # Get AI response
                    with st.spinner("AI is thinking..."):
                        ai_response = get_llm_response(user_input, groq_api_key)
                    
                    # Add AI response to history
                    add_message_to_chat("assistant", ai_response)
                    
                    # Check if response contains QASM code and offer to update
                    if "OPENQASM" in ai_response:
                        st.info("💡 The AI response contains QASM code. You can copy it to the QASM editor on the left.")
                    
                    st.rerun()
                elif not groq_api_key:
                    st.error("❌ Please provide Groq API key")
                else:
                    st.warning("⚠️ Please enter a message")
        
        with col2b:
            if st.button("🗑️ Clear Chat"):
                clear_chat_history()
                st.rerun()

def render_quick_actions(groq_api_key):
    """Render quick action buttons"""
    st.header("⚡ Quick Actions")
    
    col2d, col2e = st.columns(2)
    
    with col2d:
        if st.button("Generate Bell State"):
            if groq_api_key:
                add_message_to_chat("user", QUICK_ACTIONS["bell_state"])
                ai_response = process_quick_action("bell_state", groq_api_key)
                add_message_to_chat("assistant", ai_response)
                st.rerun()
            else:
                st.error("❌ Please provide Groq API key")
    
    with col2e:
        if st.button("🔄 Generate Random Circuit"):
            if groq_api_key:
                add_message_to_chat("user", QUICK_ACTIONS["random_circuit"])
                ai_response = process_quick_action("random_circuit", groq_api_key)
                add_message_to_chat("assistant", ai_response)
                st.rerun()
            else:
                st.error("❌ Please provide Groq API key")

def render_status_indicators(ibm_api_key, groq_api_key):
    """Render status indicators"""
    st.header("📈 Status")
    
    col2f, col2g, col2h = st.columns(3)
    
    with col2f:
        ibm_status = "🟢 Connected" if ibm_api_key else "🔴 Not Connected"
        st.markdown(f"**IBM Quantum:** {ibm_status}")
    
    with col2g:
        groq_status = "🟢 Connected" if groq_api_key else "🔴 Not Connected"
        st.markdown(f"**Groq AI:** {groq_status}")
    
    with col2h:
        qiskit_status = "🟢 Available" if check_qiskit() else "🔴 Not Available"
        st.markdown(f"**Qiskit:** {qiskit_status}")

def render_footer():
    """Render footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>⚛️ IBM Quantum Circuit JOB Automation | Built with Streamlit, Qiskit & Groq</p>
        <p><small>Make sure to keep your API keys secure and never share them publicly.</small></p>
    </div>
    """, unsafe_allow_html=True)