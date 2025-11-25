# Agent Playground

A playground environment for developing and testing AI agents using the `pydantic-ai` framework and optional toolsets (e.g., BrowserAutomation via MCP/Playwright).

Key points pulled from the package:

- Package: `agent-playground` (version 0.1.0)
- Requires: Python >= 3.12
- Installable via pip / editable install (`pip install -e .`)

## Features

- Integrates with `pydantic-ai` for model/tool orchestration
- Includes example agents and prompt files (see `agent_playground/sbir_review`)
- Provides helper example tools in `agent_playground/custom_tools`

## Requirements

- Python 3.12+
- UV for package management
- Recommended environment variables for examples in this repo:
   - `OPENROUTER_API_KEY` — used by example agents that use the OpenRouter provider
   - `LOGFIRE_TOKEN` — optional, used by the SBIR example agent for logging

Some tools (Playwright MCP) are invoked via npm (see `agent_playground/sbir_review/mcp_config.json`). The MCP Playwright server example uses the npm package `@playwright/mcp`.

## Installation

1. Clone the repository

```bash
git clone https://github.com/HSV-AI/agent-playground.git
cd agent-playground
```

2. Install dependencies

```bash
uv sync
```

Dev dependencies are declared in `pyproject.toml` under `[project.optional-dependencies].dev` (pytest, black, isort, mypy).

## Included examples

- `agent_playground/sbir_review` — an example SBIR scraping agent (`SBIRAgent`) that demonstrates:
   - configuring an OpenRouter-backed model
   - loading MCP toolsets from `mcp_config.json` (Playwright MCP example)
   - system and user prompt files (`system_prompt.md`, `user_prompt.md`)
   - asynchronous execution pattern in `agent_playground/sbir_review/agent.py`

- `agent_playground/custom_tools/basic_script.py` — small example tools and helper functions that show how to register plain tools on an agent.

## MCP Servers

The list of MCP Servers to be used for this repo can be found at the MCP Github Repo - [https://github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

## Contributing

Contributions are welcome. Please open issues or pull requests against the `main` branch. Follow the repo formatting and typing conventions (Black, isort, mypy) when submitting changes.

## License

This project is licensed under the MIT License — see `LICENSE` for details.
