# AgentHub Core

Core package for the AgentHub framework, providing base classes and utilities.

## Installation

```bash
pip install agenthub-tools-core
```

## Usage

```python
from agenthub_tools.core import BaseTool

class MyTool(BaseTool):
    name = "my-tool"
    description = "My custom tool"
    
    def execute(self, **kwargs):
        # Implement tool logic
        pass
```
