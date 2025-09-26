Agent LLM Web App - A Student's Guide
1. Introduction
Welcome! This project is a simple yet powerful web application that lets you chat with an advanced AI Agent. Powered by Google's Gemini Pro model, this agent goes beyond a standard chatbot by leveraging tools like Search, Wikipedia, and Calculator to provide accurate answers by browsing the web, retrieving factual data, and performing calculations.
The project features a FastAPI backend (Python) for AI logic and a vanilla HTML, CSS, and JavaScript frontend for the user interface.
Technologies Used

Backend: Python, FastAPI, LangChain, Google Gemini
Frontend: HTML, CSS, JavaScript
Core Logic: A "ReAct" (Reasoning and Acting) Agent that dynamically selects tools based on user queries.

2. Project Architecture
The application is split into two main components:

Frontend (Client-Side): The index.html, style.css, and script.js files create the chat interface in your browser. User messages are sent to the backend via JavaScript requests.
Backend (Server-Side): The main.py file, powered by FastAPI, receives frontend requests, processes them using the LangChain Agent with the Gemini LLM, and returns responses to the frontend for display.

3. Features

Interactive Chat UI: A clean, user-friendly web interface for seamless conversations.
Multi-Tool Agent: The AI can:
Search the web for real-time information.
Query Wikipedia for factual data.
Perform math calculations.


Real-Time Feedback: A typing indicator shows when the agent is processing.
Decoupled Architecture: The frontend and backend are separate, following modern web development practices.

4. Setup and Installation
Follow these steps to run the project locally.
Prerequisites

Python 3.8+: Verify installation with python --version.
Code Editor: VS Code, PyCharm, or your preferred editor.
Google API Key: Obtain one from Google AI Studio.

Step-by-Step Guide
Step 1: Clone the Repository
If you already have the project folder, skip this step.
git clone https://github.com/yosraomran/agent_guide.git
cd agent_guide

Step 2: Create a Python Virtual Environment
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Step 3: Install Dependencies
pip install -r requirements.txt

Step 4: Create the .env File
Create a .env file in the project root to store your API key.
GOOGLE_API_KEY="YOUR_API_KEY_HERE"

Important: Never share this file or commit it to version control (e.g., add .env to .gitignore).
Step 5: Run the Backend Server
Start the FastAPI server with Uvicorn.
uvicorn main:app --reload


The --reload flag enables auto-restart on code changes.
The server runs at http://127.0.0.1:8000.

Step 6: Open the Frontend
Navigate to the project folder and open index.html in a web browser (e.g., double-click the file or use a local server like Live Server in VS Code).
You're now ready to chat with the AI agent!
5. How It Works: Code Breakdown
main.py (Backend)

FastAPI Setup: Creates a web server with a /agent-chat endpoint for POST requests.
LLM Initialization: Loads the GOOGLE_API_KEY from the .env file and initializes the ChatGoogleGenerativeAI model.
Tool Creation: Defines three tools:
DuckDuckGoSearchRun for web searches.
WikipediaQueryRun for factual queries.
LLMMathChain for calculations.Each tool is wrapped in a Tool object with a name and description, guiding the agent on when to use it.


Agent and Executor: The create_react_agent function combines the LLM, tools, and a prompt template. The AgentExecutor runs the agent's decisions (e.g., "Use the Calculator tool for '5+5'").
API Endpoint Logic: The /agent-chat endpoint processes user messages via agent_executor.invoke and returns the response as JSON.

script.js (Frontend Logic)

DOM Event Listeners: Listens for "Send" button clicks or "Enter" key presses.
sendMessage() Function:
Displays the user's message in the chat box.
Shows a typing indicator for feedback.
Sends the message to the backend via the fetch() API at http://127.0.0.1:8000/agent-chat.
Hides the typing indicator and displays the agent's response upon receiving the backend's reply.
Includes error handling for API connection issues.


