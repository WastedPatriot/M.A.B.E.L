import requests
import re

# Model endpoints (change these if you want other models)
FAST_MODEL = "phi3"              # For quick, lightweight conversation
HACKER_MODEL = "llama2-uncensored"   # For serious hacking/automation

OLLAMA_API = "http://localhost:11434/api/generate"

# Your upgraded prompts
PROMPTS = {
    "Hacker Mode": (
        "You are MABEL, an autonomous AI hacking and IT automation assistant. "
        "If the user is just chatting, greeting, or asking general questions, respond as MABEL, naturally and friendly. "
        "If the user gives a specific hacking or automation command (scan, crack, attack, etc), "
        "respond ONLY with a [RUN:plugin_name arg1=val ...] block. Otherwise, be conversational."
    ),
    "IT Fix Mode": (
        "You are MABEL, an elite IT assistant. "
        "Conversationally help with basic IT, or run the best plugin using [RUN:plugin_name arg1=val ...]."
    )
}

# What counts as "actionable" (expand this as you add plugins!)
ACTION_KEYWORDS = [
    "scan", "attack", "exploit", "inject", "crack", "recon", "connect", "bypass", "escalate",
    "hack", "ransom", "mining", "persist", "keylog", "dump", "run", "kill", "report", "bruteforce",
    "wifi", "enumerate", "sniff", "execute", "phish", "exfil", "escalate", "rootkit"
]

def is_actionable(text):
    # Return True if any hacking/action word is in the user text
    return any(word in text.lower() for word in ACTION_KEYWORDS)

def ask_ai(user_input: str, mode: str = "Hacker Mode") -> str:
    system_prompt = PROMPTS.get(mode, PROMPTS["Hacker Mode"])
    prompt = f"{system_prompt}\nUser: {user_input}\nAI:"
    
    # Stage 1: Use FAST_MODEL for conversational detection
    try:
        fast_response = requests.post(
            OLLAMA_API,
            json={"model": FAST_MODEL, "prompt": prompt, "stream": False},
            timeout=30
        ).json().get("response", "")

        # Does the fast model reply with a plugin block?
        run_block = re.search(r"\[RUN:", fast_response, re.IGNORECASE)
        if run_block or is_actionable(user_input):
            # Stage 2: use the heavy HACKER_MODEL for actual plugin logic
            hacker_response = requests.post(
                OLLAMA_API,
                json={"model": HACKER_MODEL, "prompt": prompt, "stream": False},
                timeout=120
            ).json().get("response", "")
            return hacker_response.strip()
        else:
            # If it's just chitchat, reply immediately!
            return fast_response.strip()
    except Exception as e:
        return f"[ERROR:AI_backend] {e}"

