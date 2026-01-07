# Workshop: Building Your First AI Agents
**Presenter:** J. (HSV-AI)
**Duration:** 1 Hour
**Repository:** [https://github.com/HSV-AI/agent-playground](https://github.com/HSV-AI/agent-playground)

---

## 🌟 Abstract
In this workshop, we will guide participants through the fundamentals of creating their own AI agents, drawing on deep backgrounds in natural language processing and real-world AI systems. Whether you’re just starting with AI or ready to level up your skills, this hands-on approach will take your learning to the next frontier.

---

## ⏱️ Agenda
1. **Introduction & Theory** (15 mins)
2. **Hands-on: The "Hello World" Agent** (10 mins)
3. **Hands-on: Adding Tools** (15 mins)
4. **Hands-on: Structured Workers** (10 mins)
5. **Q&A and Next Steps** (10 mins)

---

## 1. Introduction: What is Agentic AI?

> **🗣️ Speaker Notes:**
> - Start by contrasting a standard LLM (Chatbot) with an Agent.
> - **LLM:** "I think the weather is nice." (Hallucination/Training Data)
> - **Agent:** *Checks API* -> "The weather is 72°F and sunny."
> - Explain the Loop: **Perceive** -> **Think (Reason)** -> **Act (Tool)** -> **Observe Result**.

0:00 - 0:05 | Introduction & Setup

Welcome & Speaker Intro (J.)

What is "Agentic AI"? (Brief Definition)

Environment Check (Google Colab / GitHub Repo)

0:05 - 0:15 | Concepts: The Agentic Loop

The Core Loop: Explain the continuous cycle of Perceive -> Think -> Act -> Observe.

The "Brain" (Model): The LLM that provides the reasoning capabilities. It's the engine that drives the process, but it's blind and hand-less on its own.

The "Hands" (Tools): Functions the agent can call to interact with the outside world (e.g., search the web, run code, call an API). This is what makes it an "agent" and not just a chatbot.

The "Memory" (Context): How the agent keeps track of what it has done and what it has learned. This includes short-term memory (the current conversation history) and potentially long-term memory (a vector database).

The "Plan" (Reasoning): The ability to break down a complex goal into a sequence of smaller, actionable steps. This is where the "agentic" part truly shines.

Why pydantic-ai?

Type Safety: Ensures that the data going into and coming out of tools and models is exactly what is expected, preventing a whole class of errors.

Structured Output: Allows us to get predictable, parseable data objects back from the agent, not just free-form text.

### The Tech Stack
Today we are using **PydanticAI**.
- **Why?** It brings production-grade type safety to agents. If your agent tries to call a tool with the wrong arguments, Pydantic catches it *before* it breaks your code.

---

## 2. Hands-on: Setup

Open Google Colab and install the necessary libraries.

```python
# 💻 CODE BLOCK for Colab
!pip install pydantic-ai nest_asyncio
!pip install devtools

import nest_asyncio
nest_asyncio.apply() # Required for running async agents in Jupyter