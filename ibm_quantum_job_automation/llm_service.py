"""
LLM integration service for AI-powered quantum computing assistance
"""

from utils import check_groq
from config import LLM_SYSTEM_PROMPT, GROQ_MODEL, GROQ_TEMPERATURE, GROQ_MAX_TOKENS

def get_llm_response(user_message, groq_api_key):
    """Get response from Groq LLM"""
    if not check_groq():
        return "Error: Groq library not available"
    
    try:
        from groq import Groq
        
        client = Groq(api_key=groq_api_key)
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": LLM_SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model=GROQ_MODEL,
            temperature=GROQ_TEMPERATURE,
            max_tokens=GROQ_MAX_TOKENS
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting LLM response: {str(e)}"

def process_quick_action(action_type, groq_api_key):
    """Process a quick action request"""
    from config import QUICK_ACTIONS
    
    if action_type not in QUICK_ACTIONS:
        return "Error: Unknown action type"
    
    prompt = QUICK_ACTIONS[action_type]
    return get_llm_response(prompt, groq_api_key)

def extract_qasm_from_response(response):
    """Extract QASM code from AI response"""
    lines = response.split('\n')
    qasm_lines = []
    in_qasm = False
    
    for line in lines:
        if 'OPENQASM' in line:
            in_qasm = True
        if in_qasm:
            qasm_lines.append(line)
        if in_qasm and line.strip() == '' and len(qasm_lines) > 5:
            break
    
    return '\n'.join(qasm_lines).strip() if qasm_lines else None