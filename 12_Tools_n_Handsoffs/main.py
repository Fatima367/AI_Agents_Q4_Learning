import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from agents import function_tool
import rich

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

provider = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client= provider
)

config = RunConfig(
    model=  model,
    model_provider= provider,
    tracing_disabled= True
)


@function_tool
def get_location():
    """Gets the location of a user"""
    return "Your current location is Karachi"


@function_tool
def get_breaking_news():
    """Gets breaking news"""
    return "BREAKING NEWS!! 14TH AUGUST AFTER 19 DAYS!!!"


plant_agent= Agent(
    name= "Plants Info Agent",
    instructions= "You only tell plants and their related topics briefly",
    handoff_description= "Tells about plants and their related topics briefly"
)

async def main():
    agent = Agent(
    name= "Assistant",
    instructions= """
    You are a helpful assistant. 
    - You have to use tools or handsoff to appropriate agent to solve user queries. 
    - Donot answer on your own make sure to use relevant tools or agents to respond accurately.
    """,
    tools= [get_location, get_breaking_news],
    handoffs= [plant_agent]
    )

    result = await Runner.run(
        agent,
        """
        1. What is my current loaction?
        2. Any breaking news?
        3. What is photosynthesis?
        """, 
        run_config=config)
    
    print('='*100)
    print(f"\nResponse:\n{result.final_output}\n")
    print(f"Responded by: {result.last_agent.name}\n")
    print(result.new_items)

if __name__ == "__main__":
    asyncio.run(main())
