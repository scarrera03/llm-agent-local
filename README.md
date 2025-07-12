# 🤖 Local LLM Agent with LM Studio & DuckDuckGo Search

This project showcases a simple, local-first reasoning agent that interacts with a large language model (LLM) running in **LM Studio**, and optionally performs real-time web searches using **DuckDuckGo**. The agent follows a reasoning loop inspired by the ReAct (Reasoning + Acting) framework.

---

## Project Structure

LLM-Agents-Local/
├── agent.py # Main script for interacting with the local LLM
├── README.md # This file
├── requirements.txt # Python dependencies
└── screenshots/ # Screenshots for documentation/demo
    ├── lmstudio_loaded.png
    ├── terminal_success.png


---

## Features

- Local inference using LM Studio and a GGUF model (e.g. Mistral 7B).
- ReAct-style loop: Thought → Action → Observation → Final Answer.
- Action execution via DuckDuckGo search API.
- Simple regex-based action parsing from LLM responses.
- Up to 5 cycles per run.

---

## ▶️ How to Run

1. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
   
2. Make sure LM Studio is running at http://localhost:1234 with the model loaded (e.g. mistral-7b-instruct-v0.1.Q4_0).
3. Run the agent script:
```bash
python agent.py
```

4. Enter your task or question when prompted:
```css
What are the top programming languages in 2025?
```
# Example Output

The agent will reason about your input, perform actions like web search, and return a final answer.

```vbnet
Task: What is the capital of Japan?

Thought: I need to find the capital city of Japan.
Action [capital of Japan]
Observation: The capital of Japan is Tokyo.
Final Answer: Tokyo.
```

# Dependencies

requests

duckduckgo_search

re

time
You can install everything with:

```bash
pip install -r requirements.txt
```
# Screenshots

| LM Studio Loaded                     | Terminal Output                       |
| ------------------------------------ | ------------------------------------- |
| ![](screenshots/lmstudio_loaded.png) | ![](screenshots/terminal_success.png) |


# License
This project is open source and free to use for learning or prototyping purposes.
