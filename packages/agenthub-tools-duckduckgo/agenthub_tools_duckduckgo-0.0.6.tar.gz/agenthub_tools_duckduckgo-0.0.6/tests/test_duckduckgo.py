import pytest
from aihive_tools.duckduckgo import DuckduckgoTool

def test_tool_creation():
    tool = DuckduckgoTool()
    assert tool.name == "duckduckgo"
    assert isinstance(tool.description, str)
