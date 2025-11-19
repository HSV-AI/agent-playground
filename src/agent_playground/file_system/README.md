# File System Agent

## Overview

The File System Agent is a specialized agent designed to autonomously fulfill user file system requests using provided File System tools. It operates within the agent_playground framework, enabling automated interactions with the file system.

## Agent Purpose

The File System Agent serves to:
- Navigate and explore directory structures.
- Read file contents and metadata.
- Search for patterns and content across files.
- Manage files and directories programmatically.

This agent is particularly useful for tasks such as analyzing project structures, extracting information from codebases, and processing files.

## MCP Tools and Functions

The agent provides access to the following MCP tools via the Filesystem resource:

- **list_allowed_directories** - Lists all directories that the agent has permission to access.
- **list_directory** - Lists the contents of a specified directory.
- **read_file** - Reads the complete contents of a specified file.
- **get_file_info** - Retrieves metadata and information about a file or directory.
- **search_files** - Searches for patterns or text across multiple files using regex or simple text matching.
- **write_file** - Creates or overwrites files with specified content.
- **create_directory** - Creates new directories.
- **move_file** - Moves or renames files and directories.
- **copy_file** - Copies files and directories.
- **delete_file** - Removes files and directories.

## System Prompt Summary

The system prompt defines the agent's core behavior and constraints:

- **Strict Tool Use**: The agent must use the File System tools for all operations and avoid guessing content.
- **Exit Strategy**: The agent must return a summary of actions upon success or a detailed error message upon failure.
- **Error Handling**: The agent must abort tasks and report errors for issues like missing files or insufficient permissions.

## User Prompt Summary

The user prompt is an example of a useful prompt to use with the agent.

## Example Usage

```python
from agent_playground.file_system.agent import run_agent

# Example: List directory contents
result = run_agent("List all files in the current directory")

# Example: Search for a pattern
result = run_agent("Find all Python files and search for the function 'async_handler'")

# Example: Read a file
result = run_agent("Read the contents of agent.py")
```

## Architecture

The agent follows the standard agent_playground architecture:
1. **agent.py** - Main agent implementation using Claude API with MCP tools.
2. **mcp_config.json** - Configuration for MCP server connection.
3. **system_prompt.md** - System instructions and constraints.
4. **user_prompt.md** - User-facing documentation and usage patterns.

## Integration

The File System Agent can be integrated into larger workflows or applications that require automated file system operations. It maintains compatibility with the agent_playground framework for chaining with other specialized agents.

## Security Considerations

- File operations are sandboxed to configured directories.
- The agent respects file permissions of the runtime environment.
- Sensitive operations may require explicit user authorization.
- All file access is logged through the MCP protocol.

