import pytest
from datetime import timezone, datetime
from dirty_equals import IsNow, IsStr, IsInt

from pydantic_ai import models, capture_run_messages, RequestUsage
from pydantic_ai.models.test import TestModel
from pydantic_ai import (
    ModelResponse,
    SystemPromptPart,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
    ModelRequest,
    ModelMessage
)
from pydantic_ai.models.function import AgentInfo, FunctionModel

from agent_playground.file_system.agent import FileSystemAgent

models.ALLOW_MODEL_REQUESTS = False
pytestmark = pytest.mark.asyncio

def call_file_tool(  
    messages: list[ModelMessage], info: AgentInfo
) -> ModelResponse:
    if len(messages) == 1:
        # first call, call the weather forecast tool
        user_prompt = messages[0].parts[-1]
        args = {'path': 'tests'}  
        return ModelResponse(parts=[ToolCallPart('list_directory', args)])
    else:
        # second call, return the forecast
        msg = messages[-1].parts[0]
        assert msg.part_kind == 'tool-return'
        return ModelResponse(parts=[TextPart(f'File content: {msg.content}')])


async def test_runner_get_file_tool():
    runner = FileSystemAgent()
    print(runner._toolsets)

    for toolset in runner._toolsets:
        tools = await toolset.list_tools()
        for tool in tools:
            print(f"\nName: {tool.name} - Description: {tool.description}\n")
            print(tool)

    prompt = "Prompt doesn't matter"
    model = TestModel(call_tools=["list_directory"])
    with capture_run_messages() as messages:
        with runner._agent.override(model=FunctionModel(call_file_tool)):
            result = await runner.run(prompt)

    assert "File content" in str(result.output)  # Adjust based on expected output
    
    # print(messages)

    assert messages == [
        ModelRequest(
            parts=[
                SystemPromptPart(
                    content=IsStr(), 
                    timestamp=IsNow(tz=timezone.utc)    
                ),
                UserPromptPart(
                    content=prompt, 
                    timestamp=IsNow(tz=timezone.utc)
                )
            ]
        ), 
        ModelResponse(
            parts=[
                ToolCallPart(
                    tool_name='list_directory', 
                    args={'path': 'tests'}, 
                    tool_call_id=IsStr(),
                )
            ], 
            usage=RequestUsage(
                input_tokens=IsInt(), 
                output_tokens=IsInt()
            ), 
            model_name='function:call_file_tool:',
            timestamp=IsNow(tz=timezone.utc)
        ), 
        ModelRequest(
            parts=[
                ToolReturnPart(
                    tool_name='list_directory', 
                    content=IsStr(),
                    tool_call_id=IsStr(),
                    timestamp=IsNow(tz=timezone.utc)
                )
            ]
        ), 
        ModelResponse(
            parts=[
                TextPart(
                    content=IsStr()
                )
            ], 
            usage=RequestUsage(
                input_tokens=IsInt(), 
                output_tokens=IsInt()
            ), 
            model_name='function:call_file_tool:', 
            timestamp=IsNow(tz=timezone.utc)
        )
    ]
