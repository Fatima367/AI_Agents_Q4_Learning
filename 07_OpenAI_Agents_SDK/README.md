# OpenAI Agents SDK - Beginner’s Guide

This guide answers some key questions about the OpenAI Agents SDK in simple terms, with easy-to-understand explanations and code examples. It’s designed for beginners to help you understand the Agent class, Runner class, and concepts like generics in Python. Let’s dive in!

---

## 1. Why is the `Agent` class defined as a dataclass?

A dataclass in Python is a special way to create a class that makes it easier to handle data. The `Agent` class in the OpenAI Agents SDK is a dataclass because it simplifies storing and managing the agent’s properties, like its name, instructions, and tools.

Using a dataclass means:
- Easy initialization of attributes.
- A readable string representation of the object.
- Comparison between objects (e.g., checking if two agents are equal).

### Example: Creating an Agent with a Dataclass

```python
from dataclasses import dataclass
from agents import Agent

# The Agent class is a dataclass (simplified example)
@dataclass
class Agent:
    name: str
    instructions: str

# Create an agent
agent = Agent(name="Helper", instructions="You are a helpful assistant.")
print(agent)
```

---

## 2a. Why is the system prompt contained in the `Agent` class as `instructions`? Why can it also be a callable?

- **String**: A fixed prompt, like `"You are a math tutor."`
- **Callable**: A function to generate prompts dynamically.

### Example: Instructions as a String vs. Callable

```python
from agents import Agent, Runner
from dataclasses import dataclass
import asyncio

# Instructions as a string
agent1 = Agent(
    name="MathTutor",
    instructions="You are a math tutor."
)

# Instructions as a callable (function)
def dynamic_instructions(context, agent):
    return f"You are a tutor helping {context.context.name} with math."

@dataclass
class UserContext:
    name: str

agent2 = Agent[UserContext](
    name="DynamicTutor",
    instructions=dynamic_instructions
)

async def main():
    context = UserContext(name="Alice")
    result = await Runner.run(agent2, "Solve 2+2", context=context)
    print(result.final_output)

asyncio.run(main())
```

---

## 2b. Why is the user prompt passed to `Runner.run`, and why is it a `classmethod`?

The user prompt is the task-specific input (e.g., “What is 2 + 2?”). It’s passed to `Runner.run()` to process that specific input with the agent’s instructions.

It’s a `classmethod` so you can use `Runner.run()` directly without needing to instantiate `Runner`.

### Example:

```python
from agents import Agent, Runner
import asyncio

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant."
)

async def main():
    result = await Runner.run(agent, "What is 2 + 2?")
    print(result.final_output)

asyncio.run(main())
```

---

## 3. What is the purpose of the `Runner` class?

`Runner` is the engine that:
- Sends the user prompt to the agent.
- Calls the language model (LLM).
- Handles tools, context, and handoffs.
- Returns the final result.

### Example:

```python
from agents import Agent, Runner
import asyncio

agent = Agent(
    name="WeatherAssistant",
    instructions="You provide weather updates."
)

async def main():
    result = await Runner.run(agent, "What’s the weather like today?")
    print(result.final_output)

asyncio.run(main())
```

---

## 4. What are Generics in Python? Why are they used for `TContext`?

Generics allow functions/classes to work with different types while enforcing type safety.

`TContext` is a generic for the `context` object — extra data passed to the agent (e.g., user info).

Benefits:
- ✅ Type safety
- 🔄 Flexibility
- 📚 Clarity

### Example:

```python
from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper
import asyncio

@dataclass
class UserContext:
    name: str
    user_id: int

agent = Agent[UserContext](
    name="Assistant",
    instructions="You are a helpful assistant."
)

async def greet_user(wrapper: RunContextWrapper[UserContext]) -> str:
    return f"Hello, {wrapper.context.name}!"

agent.tools = [greet_user]

async def main():
    context = UserContext(name="Bob", user_id=123)
    result = await Runner.run(agent, "Greet me!", context=context)
    print(result.final_output)

asyncio.run(main())
```

---

## ✅ Key Takeaways

- `Agent` uses a `dataclass` to simplify handling its properties.
- `instructions` can be a string or callable to allow flexibility.
- The user prompt goes into `Runner.run()` because it changes each time.
- `Runner` is the engine that manages prompts, tools, responses.
- Generics (`TContext`) ensure type-safe and consistent context usage.

---

For more details, see the [OpenAI Agents SDK documentation](https://platform.openai.com/docs/assistants/overview).
