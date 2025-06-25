from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import chainlit as cl
import requests
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found")

@function_tool
def get_crypto_data():
    data = requests.get("https://api.coinlore.net/api/global/")
    result = data.json()
    return result

external_client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client= external_client
)

crypto_agent = Agent(
    name= "Crypto Data Agent",
    instructions= "You are a Crypto Data Agent you get the current Market Rate of Crypto Currencies using the tools.",
    tools= [get_crypto_data],
    model= model
)

@cl.on_chat_start
async def welcome():
   await cl.Message(
       author= "AI Crypto Data Agent",
       content="Hello, I'm your Crypto Data Agent. How can I help you?"
       ).send()
   
@cl.on_message
async def chats(message: cl.Message):
    user_input = message.content.strip()

    try:
        result = Runner.run_streamed(crypto_agent, user_input)

        response = cl.Message(author="Crypto Data Agent", content="")
        await response.send()

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                delta = event.data.delta
                await response.stream_token(delta)

        # Important: Tell the frontend the message is done
        await response.update()

    except Exception as e:
        print("Error:", e)
        await cl.Message("Oops! Something went wrong please try again.").send()