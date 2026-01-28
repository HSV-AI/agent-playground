![HSV-AI Logo](https://hsv.ai/wp-content/uploads/2022/03/logo_v11_2022.png)

# Workshop: Building Your First AI Agents
**Repository:** [https://github.com/HSV-AI/agent-playground](https://github.com/HSV-AI/agent-playground)


## 🌟 Vibe Provided Abstract
In this workshop, we will guide participants through the fundamentals of creating their own AI agents, drawing on deep backgrounds in natural language processing and real-world AI systems. Whether you’re just starting with AI or ready to level up your skills, this hands-on approach will take your learning to the next frontier.

---

## ⏱️ Agenda
1. **Introduction & Environment Checkout** (5 mins)
2. **Basic Definitions** (15 mins)
2. **Hands-on: The "Hello World" Agent** (10 mins)
3. **Hands-on: Adding Tools** (15 mins)
4. **Hands-on: Structured Workers** (10 mins)
5. **Q&A and Next Steps** (10 mins)

---

## 1. Introduction & Envorinment Checkout


### Introduction / What I do:
- Chief Technical Officer - CohesionForce, Inc
- Founder - Huntsville AI
- AI Huntsville - Workforce Development Committee
- Captain/Treasurer - Keel Mountain Volunteer Fire Department


> I believe that the best way to ensure that AI is used for the greater good is to involve the greatest number of perspectives in its development, testing, and use.

### Environment Checkout

Each notebook includes a link that will load the notebook into Google Colab. You can also load and run locally if you have your own environment.

For local development, follow the instructions in the [Repo README.md](https://github.com/HSV-AI/agent-playground/blob/dev/README.md)

## 2. Basic Definitions

### THOUGHT QUESTION - What is an Agent?

Literally thinking, how many types of agents can we name in 30 seconds?

### Now, what is an AI Agent?

HuggingFace Definition:

>An Agent is a system that leverages an AI model to interact with its environment in order to achieve a user-defined objective. It combines reasoning, planning, and the execution of actions (often via external tools) to fulfill tasks.

### THOUGHT QUESTION - How is this different from just automating a task?


The Core Loop: Explain the continuous cycle of Perceive -> Think -> Act -> Observe.

The "Brain" (Model): The LLM that provides the reasoning capabilities. It's the engine that drives the process, but it's blind and hand-less on its own.

The "Hands" (Tools): Functions the agent can call to interact with the outside world (e.g., search the web, run code, call an API). This is what makes it an "agent" and not just a chatbot.

The "Memory" (Context): How the agent keeps track of what it has done and what it has learned. This includes short-term memory (the current conversation history) and potentially long-term memory (a vector database).

The "Plan" (Reasoning): The ability to break down a complex goal into a sequence of smaller, actionable steps. This is where the "agentic" part truly shines.

Why pydantic-ai?

Type Safety: Ensures that the data going into and coming out of tools and models is exactly what is expected, preventing a whole class of errors.

Structured Output: Allows us to get predictable, parseable data objects back from the agent, not just free-form text.

