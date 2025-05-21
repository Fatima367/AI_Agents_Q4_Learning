
# OpenAI Agents SDK - Beginner’s Guide

This guide answers some key questions about the OpenAI Agents SDK in simple terms, with easy-to-understand explanations and code examples. It’s designed for beginners to help you understand the Agent class, Runner class, and concepts like generics in Python. Let’s dive in!

---

## 1. Why is the `Agent` class defined as a `dataclass`?

In Python, a `dataclass` is used when a class is mostly for **storing data**. It automatically creates useful methods like `__init__`, `__repr__`, and `__eq__` so you don’t have to write them yourself. It **automatically gives** useful features like:

- Easy way to **create** an agent.
- Simple way to **store info** like name and instructions.
- Makes the code **shorter and cleaner**.

The `Agent` class stores settings like the system prompt, tools, and name. That's why it's a perfect fit for a `dataclass`. 

### Example:

```python
from dataclasses import dataclass

@dataclass
class Agent:
    name: str
    instructions: str

agent = Agent(name="MyAgent", instructions="Help the user.")
print(agent)
# Output: Agent(name='MyAgent', instructions='Help the user.')
```

So no need to write extra code like `__init__` or `__str__`. The dataclass handles it!

📚 Source: [Agent Source Code](https://openai.github.io/openai-agents-python/ref/agent/)


---

## 2a. What is the `instructions` field and why can it be callable?

The `instructions` field in `Agent` holds the **system prompt**, which is like the agent’s job description.

You can set it as:
- A **string** → if the message is fixed.
- A **function (callable)** → a function that returns instructions (this is useful when the prompt should change depending on the user)

This makes the agent flexible!

### Example:

```python
# Fixed instructions (string)
instructions = "You are a helpful assistant."

# Dynamic instructions (function)
def dynamic_instructions(context):
    return f"You are helping with task: {context['task']}"

# Both can be used as `instructions` in the Agent
```

---

## 2b. Why is the user prompt passed to `Runner.run()` and why is it a classmethod?

- The **user prompt** is the message the human sends.
- It is passed to the `run()` method of `Runner`, which handles the **conversation process**.
- `run()` is a **classmethod**, which means it's called on the class (`Runner.run(...)`) instead of an object (`runner.run(...)`), so you can use it directly without making a Runner object.

This is useful when you don't need to create a `Runner` object first—it simplifies running the agent.

### Example:

```python
class Runner:
    @classmethod
    def run(cls, agent, prompt):
        print(f"Agent: {agent.name}")
        print(f"User said: {prompt}")

Runner.run(agent=Agent("Test", "Test instructions"), prompt="Hello?")
```

📚 Source: [Runner Class Source](https://openai.github.io/openai-agents-python/ref/run/)

---

## 3. What is the purpose of the `Runner` class?

The `Runner` class is responsible for actually **running** the agent. It handles:
- Taking the user’s prompt
- Passing it to the agent
- Managing the tools
- Returning the agent's response

You can think of the `Agent` as the brain 🧠, and the `Runner` as the body that makes it do things 🏃‍♂️.

---

## 4. What are generics in Python? Why use `TContext`?

**Generics** allow you to write code that works with **any type**.

`TContext` is a **generic type**. It lets the Agent SDK work with **any kind of context** (extra data or info like user name, ID, etc) while keeping type hints clear.

This helps with:

- ✅ Type safety
- 🔁 Flexibility
- 💡 Clarity

### Example:

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Box(Generic[T]):
    def __init__(self, content: T):
        self.content = content

box1 = Box[int](123)       # content is an int
box2 = Box[str]("hello")  # content is a string
```

In OpenAI Agents SDK:

```python
TContext = TypeVar("TContext")

@dataclass
class Agent(Generic[TContext]):
    instructions: str | Callable[[TContext], str]
```

So `TContext` can be:
- a dictionary
- a custom object
- or anything else

This helps you **customize** how the agent works with your specific app.

---

## ✅ Summary

| Question | Answer |
|---------|--------|
| Why `dataclass`? | Makes it easier to store agent info like name & instructions. |
| Why can `instructions` be callable? | To allow dynamic system messages. |
| Why is user prompt passed in `Runner.run()`? | To handle the user message and generate a response. |
| Why is `run()` a classmethod? | So it can be used without creating a `Runner` object. |
| Purpose of `Runner`? | Runs the agent: handles input, tools, and responses. |
| What are generics? | A way to make code work with any type. |
| Why use `TContext`? | So the agent can work with any kind of context data. |

---

For more, visit the [OpenAI Agents SDK Docs](https://openai.github.io/openai-agents-python/).