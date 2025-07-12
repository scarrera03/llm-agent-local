import requests
import re
import time
from duckduckgo_search import DDGS

# === CONFIGURATION ===
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "mistral"  # LM Studio may ignore this if only one model is loaded
TEMPERATURE = 0.7

# === UTILITY FUNCTIONS ===

def call_llm(messages):
    response = requests.post(
        LM_STUDIO_URL,
        headers={"Content-Type": "application/json"},
        json={
            "model": "mistral-7b-instruct-v0.1.Q4_0",  # Make sure to use the exact model name
            "messages": messages,
            "temperature": TEMPERATURE,
        },
    )
    
    data = response.json()
    
    # Clear error handling
    if "choices" not in data:
        print("⚠️ Error in model response:")
        print(data)
        return "Content not found in the response"

    return data["choices"][0]["message"]["content"]


def search(query):
    with DDGS() as ddgs:
        results = ddgs.text(query)
        return next(results, {}).get("body", "No results found.")

def extract_action(response):
    match = re.search(r"Action\s*\[(.*?)\]", response)
    return match.group(1).strip() if match else None

def is_final_answer(response):
    return "Final Answer" in response

# === MAIN AGENT ===

def run_agent(task):
    messages = [{"role": "user", "content": "You are an intelligent agent. Use Thought, Action, Observation, and Final Answer to solve:\n" + task}]
    print(f"Task: {task}\n")

    for step in range(5):  # maximum 5 cycles
        response = call_llm(messages)
        print(response)
        messages.append({"role": "assistant", "content": response})

        if is_final_answer(response):
            break

        action = extract_action(response)
        if action:
            observation = search(action)
            print(f"\n[OBSERVATION] {observation}\n")
            messages.append({"role": "user", "content": f"Observation: {observation}"})
        else:
            print("No action found. Stopping.")
            break
        time.sleep(1)

if __name__ == "__main__":
    question = input("Type your question for the agent: ")
    run_agent(question)
