"""
Command-line interface for the Agent Playground.
"""
import os
import sys
from typing import Optional

import click

from agent_playground.agent import Agent, AgentConfig


@click.group()
@click.version_option()
def main() -> None:
    """Agent Playground - Run agents from markdown files."""
    pass


@main.command()
@click.argument("markdown_file", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option("--debug", is_flag=True, help="Enable debug mode")
@click.option("--model", default="gpt-4", help="LLM model to use")
@click.option("--system-prompt", help="System prompt text")
@click.option("--system-prompt-file", type=click.Path(exists=True, file_okay=True, dir_okay=False), 
              help="Path to system prompt file (.poml or plain text)")
def run(markdown_file: str, debug: bool = False, model: str = "gpt-4", 
        system_prompt: Optional[str] = None, system_prompt_file: Optional[str] = None) -> None:
    """Run an agent with the given markdown file."""
    click.echo(f"Running agent on {markdown_file}")
    
    try:
        # Create agent configuration
        config = AgentConfig(
            debug=debug,
            model=model,
            system_prompt=system_prompt,
            system_prompt_file=system_prompt_file
        )
        
        # Initialize agent with configuration
        agent = Agent(config=config)
        
        if system_prompt_file:
            click.echo(f"Using system prompt from: {system_prompt_file}")
        
        result = agent.run(markdown_file)
        click.echo(f"Agent completed with result: {result}")
    except Exception as e:
        click.echo(f"Error running agent: {str(e)}", err=True)
        if debug:
            import traceback
            click.echo(traceback.format_exc(), err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
