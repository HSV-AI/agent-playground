# Agent Playground

A playground environment for developing and testing AI agents that read instructions from markdown files and execute them using the `pydantic-ai` framework and optional toolsets (e.g., BrowserAutomation via MCP/Playwright).

Key points pulled from the package:

- Package: `agent-playground` (version 0.1.0)
- Requires: Python >= 3.12
- CLI entry point: `agent-playground` -> `agent_playground.cli:main`
- Installable via pip / editable install (`pip install -e .`)

## Features

- Run agents defined by markdown instructions
- Integrates with `pydantic-ai` for model/tool orchestration
- Includes example agents and prompt files (see `agent_playground/sbir_review`)
- Supports loading system prompts from plain text or POML files
- Provides helper example tools in `agent_playground/custom_tools`

## Requirements

- Python 3.12+
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

2. Install (editable) with pip

```bash
python -m pip install -e .
```

Or install normally:

```bash
python -m pip install .
```

If you prefer the `uv` package manager (used by some contributors), you can install the project in editable mode using `uv`'s pip shim:

```bash
uv pip install -e .
```

Dev dependencies are declared in `pyproject.toml` under `[project.optional-dependencies].dev` (pytest, black, isort, mypy).

## Usage

The package exposes a CLI entry point. You can run it either with the installed console script or as a module.

Run the CLI command directly (after installing):

```bash
agent-playground run path/to/instructions.md --debug --model gpt-4 --system-prompt-file path/to/prompt.poml
```

Or run as a module:

```bash
python -m agent_playground run path/to/instructions.md --debug
```

CLI options (from `agent_playground/cli.py`):

- `markdown_file` (argument): path to a markdown file containing instructions for the agent
- `--debug`: enable debug mode
- `--model`: model name (default: `gpt-4` in CLI defaults)
- `--system-prompt`: system prompt text
- `--system-prompt-file`: path to a system prompt file (POML or plain text)

Example:

```bash
python -m agent_playground run examples/example_instructions.md --system-prompt-file agent_playground/sbir_review/system_prompt.md
```

## Included examples

- `agent_playground/sbir_review` — an example SBIR scraping agent (`SBIRAgent`) that demonstrates:
   - configuring an OpenRouter-backed model
   - loading MCP toolsets from `mcp_config.json` (Playwright MCP example)
   - system and user prompt files (`system_prompt.md`, `user_prompt.md`)
   - asynchronous execution pattern in `agent_playground/sbir_review/agent.py`

- `agent_playground/custom_tools/basic_script.py` — small example tools and helper functions that show how to register plain tools on an agent.

## MCP Servers

The list of MCP Servers to be used for this repo can be found at the MCP Github Repo - [https://github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

## Environment & External Tools

- Some example agents rely on an MCP server (Playwright) defined in `agent_playground/sbir_review/mcp_config.json`. The provided config expects the `@playwright/mcp` npm package to be available and run via `npx`. Example MCP entry:

```json
{
   "mcpServers": {
      "playwright": {
         "command": "npx",
         "args": ["@playwright/mcp", "--headless", "--browser", "chromium"]
      }
   }
}
```

Start the MCP server per project needs (the repo does not automatically install or run npm packages). For local testing, ensure Node/npm is installed and run the configured MCP server command.

## Development

- Tests: The project lists `pytest` as a dev dependency. Add tests under `tests/` and run:

```bash
python -m pytest -q
```

- Formatting/Linting: `black` and `isort` are available in dev extras.

## Contributing

Contributions are welcome. Please open issues or pull requests against the `main` branch. Follow the repo formatting and typing conventions (Black, isort, mypy) when submitting changes.

## License

This project is licensed under the MIT License — see `LICENSE` for details.

## Where to look next

- CLI behavior: `agent_playground/cli.py`
- Package metadata & entry points: `pyproject.toml`
- Example agent & prompts: `agent_playground/sbir_review`
- Example helper tools: `agent_playground/custom_tools`

If you'd like, I can also:

- Add a small `examples/` markdown file that demonstrates the full run flow
- Add a short CONTRIBUTING.md or CODE_OF_CONDUCT

---
Updated to reflect code and metadata in the repository.
