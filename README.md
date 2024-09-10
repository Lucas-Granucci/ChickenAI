# ChickenAI - FIRST Robotics Expert Chatbot

ChickenAI is an AI-powered chatbot that provides up-to-date information about FIRST Robotics teams and events. It leverages The Blue Alliance API to fetch real-time data and uses advanced language models to generate informative responses.

## Features

- Interactive chat interface for querying FIRST Robotics information
- Real-time data fetching from The Blue Alliance API
- Intelligent response generation using AI language models
- Support for team information, team events, and all events queries

## Requirements

- Python 3.7+
- Langroid library
- The Blue Alliance API key
- Locally hosted LLM (e.g., Llamma 3 7B)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/LucasG2008/ChickenAI.git
   cd ChickenAI
   ```
   
2. Install the required dependencies with Anaconda:
   
   ```
   conda create --name chickenai --file requirements.txt
   conda activate chickenai
   ```

3. Set up your The Blue Alliance API key as an environment variable:

4. Set up your locally hosted LLM:
   - Install and configure your chosen LLM (e.g., Llama 3 7B)
   - Run the LLM on a local server
   - Current endpoint is set to "http://localhost:1234/v1"

5. Run the ChickenAI application:
   
   ```
   python assistant/chickenai.py
   ```


## Usage

Run the ChickenAI chatbot:

python assistant/chickenai.py

(Readme generated with help from Claude.ai)