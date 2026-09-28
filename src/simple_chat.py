import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
groq_api_key = os.getenv("GROQ_API_KEY")

# With Groq
#llm = ChatGroq(temperature=0, 
#                model_name="openai/gpt-oss-20b")

# With OpenAI
llm = ChatOpenAI(
            model="openai/gpt-oss-20b",
            temperature=0.7,
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1"
        )

questions = [
    "Calculate 17 * 23",
    "What is the square root of 256?",
]

for q in questions:
    response = llm.invoke(q)
    print(f"Q: {q}\nA: {response.content}\n")