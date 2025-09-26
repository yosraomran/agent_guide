# main.py (version avec agent multi-outils et Google Gemini)

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# --- Importations LangChain ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.chains import LLMMathChain
from langchain_core.prompts import PromptTemplate
import google.generativeai as genai

# Charger les variables d'environnement
load_dotenv()

# --- Initialisation du LLM et des Outils ---

# Configurer et initialiser le LLM Google Gemini
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", # Using a powerful and versatile model
        temperature=0,
        convert_system_message_to_human=True
    )
except Exception as e:
    print(f"Erreur lors de la configuration de Google Gemini : {e}")
    print("Veuillez vérifier que votre clé GOOGLE_API_KEY est bien définie dans le fichier .env")
    llm = None

# --- Configuration des Outils ---

# 1. Outil de recherche Web
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="DuckDuckGo Search",
    func=search.run,
    description="Utile pour répondre aux questions sur l'actualité et les événements récents."
)

# 2. Outil Wikipedia
wikipedia_api = WikipediaAPIWrapper()
wikipedia = WikipediaQueryRun(api_wrapper=wikipedia_api)
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia.run,
    description="Utile pour rechercher des informations factuelles sur des sujets, des personnes et des lieux dans une encyclopédie."
)

# 3. Outil de calcul
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
calculator_tool = Tool(
    name="Calculator",
    func=llm_math_chain.run,
    description="Utile pour répondre aux questions nécessitant un calcul mathématique."
)

# Regrouper les outils dans une liste
tools = [search_tool, wikipedia_tool, calculator_tool]

# --- Configuration de l'Agent ReAct ---

# Le prompt ReAct fonctionne très bien avec Gemini.
prompt_template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""
prompt = PromptTemplate.from_template(prompt_template)

# Créer l'agent et l'exécuteur
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# --- Application FastAPI ---
app = FastAPI(title="API pour Agent LLM v3 (Multi-Outils avec Gemini)", version="3.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class AgentRequest(BaseModel):
    message: str

@app.post("/agent-chat")
async def agent_chat(request: AgentRequest):
    """
    Reçoit une question et la traite avec un agent LangChain multi-outils utilisant Gemini.
    """
    if not llm:
        return {"error": "Le LLM Google Gemini n'est pas configuré. Vérifiez votre clé API."}
    
    try:
        # Invoquer l'agent avec la question de l'utilisateur
        response = agent_executor.invoke({
            "input": request.message
        })
        return {"response": response['output']}
    except Exception as e:
        return {"error": f"Erreur lors de l'exécution de l'agent : {str(e)}"}

@app.get("/")
def read_root():
    return {"status": "L'API de l'agent LLM v3 (Multi-Outils) est en ligne !"}