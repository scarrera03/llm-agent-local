import requests
import re
import time
from duckduckgo_search import DDGS

# === CONFIGURACIÓN ===
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "mistral"  # LM Studio puede ignorar esto si solo hay un modelo cargado
TEMPERATURE = 0.7

# === FUNCIONES DE UTILIDAD ===

def call_llm(messages):
    response = requests.post(
        LM_STUDIO_URL,
        headers={"Content-Type": "application/json"},
        json={
            "model": "mistral-7b-instruct-v0.1.Q4_0",  # Asegurate de usar el nombre exacto
            "messages": messages,
            "temperature": 0.7,
        },
    )
    
    data = response.json()
    
    # ✅ Manejo claro de errores
    if "choices" not in data:
        print("⚠️ Error en la respuesta del modelo:")
        print(data)
        return "❌ No se encontró el contenido en la respuesta"

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

# === AGENTE PRINCIPAL ===

def run_agent(task):
    messages = [{"role": "user", "content": "You are an intelligent agent. Use Thought, Action, Observation, and Final Answer to solve:\\n" + task}]
    print(f"Task: {task}\n")

    for step in range(5):  # máximo 5 ciclos
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
    pregunta = input("Escribí tu pregunta para el agente: ")
    run_agent(pregunta)
