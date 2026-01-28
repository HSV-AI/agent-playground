import pytest
from datetime import timezone, datetime
import asyncio
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
    ImageUrl,
    DocumentUrl
)

from agent_playground.custom_tools.agent import ToolsAgent
from agent_playground.custom_tools.models import User

models.ALLOW_MODEL_REQUESTS = False
pytestmark = pytest.mark.asyncio

async def test_runner_user_tool():

    runner = ToolsAgent()
    prompt = "Prompt doesn't matter"
    model = TestModel(call_tools=["get_user"])
    with capture_run_messages() as messages:
        with runner._agent.override(model=model):
            result = await runner.run(prompt)

    assert "John" in str(result.output)
    
    assert messages == [
        ModelRequest(
            parts=[
                UserPromptPart(
                    content=prompt, 
                    timestamp=IsNow(tz=timezone.utc)
                )
            ]
        ), 
        ModelResponse(
            parts=[
                ToolCallPart(
                    tool_name='get_user', 
                    args={}, 
                    tool_call_id=IsStr(),
                )
            ], 
            usage=RequestUsage(
                input_tokens=IsInt(), 
                output_tokens=IsInt()
            ), 
            model_name='test', 
            timestamp=IsNow(tz=timezone.utc)
        ), 
        ModelRequest(
            parts=[
                ToolReturnPart(
                    tool_name='get_user', 
                    content=User(
                        name='John', 
                        age=30), 
                    tool_call_id=IsStr(),
                    timestamp=IsNow(tz=timezone.utc)
                )
            ]
        ), 
        ModelResponse(
            parts=[
                TextPart(
                    content='{"get_user":{"name":"John","age":30}}'
                )
            ], 
            usage=RequestUsage(
                input_tokens=IsInt(), 
                output_tokens=IsInt()
            ), 
            model_name='test', 
            timestamp=IsNow(tz=timezone.utc)
        )
    ]

async def test_runner_current_time_tool():

    runner = ToolsAgent()
    prompt = "Prompt doesn't matter"
    model = TestModel(call_tools=["get_current_time"])
    with capture_run_messages() as messages:
        with runner._agent.override(model=model):
            result = await runner.run(prompt)

    # Get the current date and time
    now = datetime.now()

    # Format the datetime object into a string with year, month, and day
    # %Y for 4-digit year, %m for zero-padded month, %d for zero-padded day
    formatted_date = now.strftime("%Y-%m-%d") 
    assert formatted_date in str(result.output)
    
    assert messages == [
        ModelRequest(
            parts=[
                UserPromptPart(
                    content=prompt, 
                    timestamp=IsNow(tz=timezone.utc)
                )
            ]
        ), 
        ModelResponse(
            parts=[
                ToolCallPart(
                    tool_name='get_current_time', 
                    args={}, 
                    tool_call_id=IsStr(),
                )
            ], 
            usage=RequestUsage(
                input_tokens=IsInt(), 
                output_tokens=IsInt()
            ), 
            model_name='test', 
            timestamp=IsNow(tz=timezone.utc)
        ),
        ModelRequest(
            parts=[
                ToolReturnPart(
                    tool_name='get_current_time', 
                    content=IsNow(),
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
            model_name='test', 
            timestamp=IsNow(tz=timezone.utc)
        )
    ]

async def test_runner_company_logo_tool():

    runner = ToolsAgent()
    prompt = "Prompt doesn't matter"
    model = TestModel(call_tools=["get_company_logo"])
    with capture_run_messages() as messages:
        with runner._agent.override(model=model):
            result = await runner.run(prompt)

    assert "See file" in str(result.output)
    
    assert messages == [
        ModelRequest(
            parts=[
                UserPromptPart(
                    content=prompt, 
                    timestamp=IsNow(tz=timezone.utc)
                )
            ]
        ), 
        ModelResponse(
            parts=[
                ToolCallPart(
                    tool_name='get_company_logo', 
                    args={}, 
                    tool_call_id=IsStr(),
                )
            ], 
            usage=RequestUsage(
                input_tokens=IsInt(), 
                output_tokens=IsInt()
            ), 
            model_name='test', 
            timestamp=IsNow(tz=timezone.utc)
        ),
        ModelRequest(
            parts=[
                ToolReturnPart(
                    tool_name='get_company_logo', 
                    content=IsStr(),
                    tool_call_id=IsStr(),
                    timestamp=IsNow(tz=timezone.utc)
                ),
                UserPromptPart(
                    content=[ IsStr(),
                    ImageUrl(url='https://iili.io/3Hs4FMg.png')],
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
            model_name='test', 
            timestamp=IsNow(tz=timezone.utc)
        )
    ]

async def test_runner_get_document_tool():

    runner = ToolsAgent()
    prompt = "Prompt doesn't matter"
    model = TestModel(call_tools=["get_document"])
    with capture_run_messages() as messages:
        with runner._agent.override(model=model):
            result = await runner.run(prompt)

    assert "See file" in str(result.output)
    
    assert messages == [
        ModelRequest(
            parts=[
                UserPromptPart(
                    content=prompt, 
                    timestamp=IsNow(tz=timezone.utc)
                )
            ]
        ), 
        ModelResponse(
            parts=[
                ToolCallPart(
                    tool_name='get_document', 
                    args={}, 
                    tool_call_id=IsStr(),
                )
            ], 
            usage=RequestUsage(
                input_tokens=IsInt(), 
                output_tokens=IsInt()
            ), 
            model_name='test', 
            timestamp=IsNow(tz=timezone.utc)
        ),
        ModelRequest(
            parts=[
                ToolReturnPart(
                    tool_name='get_document', 
                    content=IsStr(),
                    tool_call_id=IsStr(),
                    timestamp=IsNow(tz=timezone.utc)
                ),
                UserPromptPart(
                    content=[ IsStr(),
                    DocumentUrl(url='https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf')],
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
            model_name='test', 
            timestamp=IsNow(tz=timezone.utc)
        )
    ]
