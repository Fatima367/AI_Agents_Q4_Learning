# Beginner's Guide to OpenAI Agents SDK 🧠

This guide explains some key parts of the OpenAI Agents SDK in **simple words**, with **easy examples** in Python. It’s made for beginners who want to understand how this cool tool works!

---

## 🧩 1. Why is the `Agent` class a `dataclass`?

The `Agent` class is a `dataclass` because it **automatically gives** useful features like:

- Easy way to **create** an agent.
- Simple way to **store info** like name and instructions.
- Makes the code **shorter and cleaner**.

### ✅ Example:

```python
from dataclasses import dataclass

@dataclass
class Agent:
    name: str
    instructions: str

agent = Agent(name="Helper", instructions="You are a helpful assistant.")
print(agent)
```

No need to write extra code like `__init__` or `__str__`. The dataclass handles it!

📚 Source: [Agent Source Code](https://openai.github.io/openai-agents-python/ref/agent/)

---

## 💬 2a. What is `instructions` and why can it also be a function?

The `instructions` is like a **system prompt** — it tells the agent what role to play (e.g., “You are a teacher”).

It can be:

- A **string** – fixed instructions
- A **callable** – a function that returns instructions (this is useful when the prompt should change depending on the user)

### ✅ Example:

```python
# Static instructions
agent = Agent(name="MathHelper", instructions="You help with math.")

# Dynamic instructions using a function
def dynamic_instructions(context, agent):
    return f"You are helping {context.context.name} with math homework."

@dataclass
class UserContext:
    name: str

agent = Agent[UserContext](
    name="SmartHelper",
    instructions=dynamic_instructions
)
```

This makes your agent more flexible and smart.

---

## 💡 2b. Why is the user prompt passed to `Runner.run()`? And why is it a `classmethod`?

The **user prompt** is what the user asks, like "What is 2+2?". This changes every time, so it’s passed to the `run()` method.

`Runner.run()` is a **classmethod**, so you can use it directly without making a Runner object.

### ✅ Example:

```python
from agents import Agent, Runner
import asyncio

agent = Agent(name="MathBot", instructions="You are a math bot.")

async def main():
    result = await Runner.run(agent, "What is 2 + 2?")
    print(result.final_output)

asyncio.run(main())
```

📚 Source: [Runner Class Source](https://openai.github.io/openai-agents-python/ref/run/)

---

## 🚀 3. What does the `Runner` class do?

The `Runner` class is the **engine** that runs your agent.

It:
- Takes the agent and user prompt
- Sends it to the AI model
- Uses tools (if added)
- Returns the final answer

### ✅ Example:

```python
agent = Agent(name="WeatherBot", instructions="You give weather updates.")

async def main():
    result = await Runner.run(agent, "What's the weather today?")
    print(result.final_output)

asyncio.run(main())
```

---

## 🧪 4. What are generics in Python? Why use `TContext`?

**Generics** let you write code that works with **any type**.

In Agents SDK, `TContext` means: "This agent will work with a specific kind of context (extra info like user name, ID, etc)."

This helps with:

- ✅ Type safety
- 🔁 Flexibility
- 💡 Clarity

### ✅ Example:

```python
from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper

@dataclass
class UserContext:
    name: str
    user_id: int

agent = Agent[UserContext](
    name="Greeter",
    instructions="You greet the user."
)

async def greet(wrapper: RunContextWrapper[UserContext]):
    return f"Hello {wrapper.context.name}!"

agent.tools = [greet]

async def main():
    context = UserContext(name="Alice", user_id=1)
    result = await Runner.run(agent, "Greet me", context=context)
    print(result.final_output)

asyncio.run(main())
```

---

## 📝 Summary

- ✅ `Agent` is a `dataclass` to store data easily.
- ✅ `instructions` can be a string or a function.
- ✅ `Runner.run()` takes the user input and is easy to use.
- ✅ `Runner` runs the whole process for you.
- ✅ Generics like `TContext` help share context info in a safe way.

---

For more, visit the [OpenAI Agents SDK Docs](https://openai.github.io/openai-agents-python/).
