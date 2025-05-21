
# 📘 Understanding OpenAI Agents SDK (Beginner Guide)

This guide answers some key beginner questions about how the **OpenAI Agents SDK** is designed, especially around the `Agent` and `Runner` classes. You'll also learn a bit about **generics in Python**.

---

## 💡 1. Why is the `Agent` class defined as a `dataclass`?

In Python, a `dataclass` is used when a class is mostly for **storing data**. It automatically creates useful methods like `__init__`, `__repr__`, and `__eq__` so you don’t have to write them yourself.

The `Agent` class stores settings like the system prompt, tools, and name. That's why it's a perfect fit for a `dataclass`.

### ✅ Simple Example:

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

---

## 🧠 2a. What is the `instructions` field and why can it be callable?

The `instructions` field in `Agent` holds the **system prompt**, which is like the agent’s job description.

You can set it as:
- A **string** → if the message is fixed.
- A **function (callable)** → if the message needs to change based on some context.

This makes the agent flexible!

### ✅ Simple Example:

```python
# Fixed instructions (string)
instructions = "You are a helpful assistant."

# Dynamic instructions (function)
def dynamic_instructions(context):
    return f"You are helping with task: {context['task']}"

# Both can be used as `instructions` in the Agent
```

---

## 🗨️ 2b. Why is the user prompt passed to `Runner.run()` and why is it a classmethod?

- The **user prompt** is the message the human sends.
- It is passed to the `run()` method of `Runner`, which handles the **conversation process**.
- `run()` is a **classmethod**, which means it's called on the class (`Runner.run(...)`) instead of an object (`runner.run(...)`).

This is useful when you don't need to create a `Runner` object first—it simplifies running the agent.

### ✅ Simple Example:

```python
class Runner:
    @classmethod
    def run(cls, agent, prompt):
        print(f"Agent: {agent.name}")
        print(f"User said: {prompt}")

Runner.run(agent=Agent("Test", "Test instructions"), prompt="Hello?")
```

---

## 🏃 What is the purpose of the `Runner` class?

The `Runner` class is responsible for actually **running** the agent. It handles:
- Taking the user’s prompt
- Passing it to the agent
- Managing the tools
- Returning the response

You can think of the `Agent` as the brain 🧠, and the `Runner` as the body that makes it do things 🏃‍♂️.

---

## 🧰 What are generics in Python? Why use `TContext`?

**Generics** allow you to write code that works with **any type**.

`TContext` is a **generic type**. It lets the Agent SDK work with **any kind of context** (extra data) while keeping type hints clear.

### ✅ Simple Example:

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

Let me know if you want to add this to a project or turn it into a blog!
