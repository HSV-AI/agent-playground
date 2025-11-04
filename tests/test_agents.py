import pytest
from unittest.mock import patch

# Import all agents from the agent_playground package
from agent_playground.file_system.agent import FileSystemAgent
from agent_playground.git_tools.agent import GitToolsAgent
from agent_playground.github_issues.agent import GitHubIssuesAgent
from agent_playground.sbir_review.agent import SBIRAgent

@pytest.fixture
def mock_llm():
    with patch('agent_playground.file_system.agent.LLM') as mock:
        yield mock

@pytest.fixture
def mock_mcp():
    with patch('agent_playground.file_system.agent.MCP') as mock:
        yield mock

def test_file_system_agent(mock_llm, mock_mcp):
    agent = FileSystemAgent()
    # Add assertions and mock behavior as needed
    assert agent is not None

def test_git_tools_agent(mock_llm, mock_mcp):
    agent = GitToolsAgent()
    # Add assertions and mock behavior as needed
    assert agent is not None

def test_github_issues_agent(mock_llm, mock_mcp):
    agent = GitHubIssuesAgent()
    # Add assertions and mock behavior as needed
    assert agent is not None

def test_sbir_review_agent(mock_llm, mock_mcp):
    agent = SBIRAgent()
    # Add assertions and mock behavior as needed
    assert agent is not None
