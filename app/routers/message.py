from fastapi import APIRouter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

router = APIRouter(prefix="/message")

# Prompt template
template = """Question: {question}
Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

# Initialize the LLM (Gemini 2.5 Flash via OpenRouter)
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="google/gemini-2.5-flash",  # ✅ Latest Gemini model on OpenRouter
)


@router.post("/")
def create_new_message(message: str):

    llm_chain = LLMChain(prompt=prompt, llm=llm)

    # Example question
    question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

    # Run the chain
    print(llm_chain.run(message))

    return ""
