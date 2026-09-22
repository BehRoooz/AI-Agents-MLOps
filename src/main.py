import os
import logging

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from tools.calculator import Calculator, CalculatorInput

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Prompt location to use for the agent
prompt_location = "prompts/complete_agent_prompt.txt"

# --- Loading environment variables ---
load_dotenv(override=True)

def main():
    # --- 1. Retrieving the Groq API key ---
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        logger.error("The GROQ_API_KEY environment variable is not defined. Please configure it in the .env file.")
        return

    # --- 2. Initializing the Groq LLM via OpenAI-compatible endpoint ---
    try:
        llm = ChatOpenAI(
            model="openai/gpt-oss-20b",
            temperature=0.7,
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        logger.info(f"Client Groq LLM '{llm.model_name}' successfully initialized.")
    except Exception as e:
        logger.error(f"Error initializing Groq LLM: {e}")
        return

    # --- 3. Defining the tools and messages to send to the LLM ---
    tools = [
        Tool(
            name="Calculator",
            func=Calculator,
            description=(
                "Useful for performing arithmetic operations and mathematical functions (e.g., sqrt, log, sin). "
                "Takes a FORMAL mathematical expression as a string, e.g., '2 + 2 * 3' or 'sqrt(144) + 5'."
                "Does NOT use natural language to describe the operation."
            ),
            args_schema=CalculatorInput
        )
    ]
    logger.info(f"{len(tools)} tools defined and ready for the agent.")

    # --- 4. Loading the system prompt (persona + business rules) ---
    try:
        with open(prompt_location, "r", encoding="utf-8") as f:
            system_prompt = f.read().strip()
        logger.info(f"System prompt loaded from '{prompt_location}'.")
    except FileNotFoundError:
        logger.error(f"The file '{prompt_location}' is not found. Please ensure it exists.")
        return
    except Exception as e:
        logger.error(f"Error loading the prompt: {e}")
        return

    # --- 5. Creating the ReAct agent (LangGraph) ---
    # create_react_agent returns a compiled LangGraph graph that implements
    # the ReAct loop: Reason → Act (tool call) → Observe → Reason...
    agent = create_react_agent(llm, tools, prompt=system_prompt)
    logger.info("Agent ReAct LangGraph created with the LLM and the Calculator tool.")

    # --- 6. Executing the agent with questions focused on calculations ---
    questions = [
        "What is the square root of 144 plus 5?",
        "Calculate 15 * (3 + 7) / 2.",
        "How many is 789 - 123?",
        "What is the result of (100 / 4) + (20 * 3)?",
        "Divide 1 by zero.", # Test of error handling of the tool
        "Is the sky blue?" # Test to see if the agent tries to use the calculator
    ]
    print("\n--- Starting tests of the agent (Calculator only) ---")
    for i, q in enumerate(questions):
        print(f"\n--- Question {i+1}: {q} ---")
        try:
            result = agent.invoke({"messages": [HumanMessage(content=q)]})
            final_answer = result["messages"][-1].content
            print(f"Agent's final response: {final_answer}")
        except Exception as e:
            logger.error(f"Error executing the agent for the question '{q}': {e}")
            print(f"The agent encountered an error: {e}")
        print("---------------------------------")

    print("\n--- End of tests of the agent ---")

if __name__ == "__main__":
    main()
