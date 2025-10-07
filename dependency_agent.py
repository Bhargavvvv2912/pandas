# dependency_agent.py

import os
import sys
import google.generativeai as genai
from agent_logic import DependencyAgent

# --- Configuration for the Pandas Experiment ---
AGENT_CONFIG = {
    "REQUIREMENTS_FILE": "requirements-dev.txt",
    ##"PRIMARY_REQUIREMENTS_FILE": "primary_requirements.txt", # We'll create an empty one for this experiment
    "METRICS_OUTPUT_FILE": "metrics_output.txt",
    "MAX_LLM_BACKTRACK_ATTEMPTS": 3,
    "MAX_RUN_PASSES": 5, # Give it a few more passes for a complex project
}

if __name__ == "__main__":
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        sys.exit("Error: GEMINI_API_KEY environment variable not set.")
    
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Using a specific model and API version for stability
    # IMPORTANT: Update your google-generativeai library first! `pip install --upgrade google-generativeai`
    llm_client = genai.GenerativeModel('gemini-1.5-flash-latest')

    agent = DependencyAgent(config=AGENT_CONFIG, llm_client=llm_client)
    agent.run()