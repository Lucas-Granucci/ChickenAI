# ChickenAI - FIRST Robotics Expert Chatbot

ChickenAI is an AI-powered chatbot that provides up-to-date information about FIRST Robotics teams and events. It leverages The Blue Alliance API and Statbotics to fetch real-time data and uses advanced language models to generate informative responses.

## Features

- 🤖 Interactive chat interface for querying FIRST Robotics information
- 🔄 Real-time data fetching from The Blue Alliance API and Statbotics
- 🧠 Intelligent response generation using AI language models
- 📊 Support for team information, team events, and all events queries

## Requirements

- Python 3.7+
- Langroid library
- The Blue Alliance API key
- LLM Model (see setup options below)
- requirements.txt

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LucasG2008/ChickenAI.git
   cd ChickenAI
   ```

2. Install the required dependencies with pip:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your The Blue Alliance API key as an environment variable.

## LLM Setup

Choose one of the following options to set up your Language Model:

### Option 1: Locally Hosted LLM

1. Install and configure your chosen LLM (e.g., Llama 3 7B)
2. Run the LLM on a local server
3. Update the `lm_config` in your code:

   ```python
   lm_config = lm.OpenAIGPTConfig(
       chat_model="local/localhost:1234/v1"
   )
   ```

   Note: The current endpoint is set to "http://localhost:1234/v1"

### Option 2: LLM API Service

1. Set up an API endpoint for your LLM service (e.g., GroqCloud)
2. Update the `lm_config` in your code:

   ```python
   lm_config = lm.OpenAIGPTConfig(
       api_base="https://api.groq.com/openai/v1",
       api_key=os.getenv("GROQ_CHICKENAI"),
       chat_model="llama-3.1-8b-instant"
   )
   ```

   Make sure to set the `GROQ_CHICKENAI` environment variable with your API key.

## Usage

Run the ChickenAI chatbot from the Command Line Interface (CLI):

```bash
python main_cli.py
```

Run the ChickenAI chatbot from the Web Interface (Streamlit):

```bash
streamlit run app.py
```

---

(README generated with assistance from Claude.ai)