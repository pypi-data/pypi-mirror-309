# AIHive Core

Core package for the AIHive framework, providing base classes and utilities.

## Installation

```bash
pip install aihive-tools-core
```

## Usage

```python
from aihive_tools.core import BaseTool

class MyTool(BaseTool):
    name = "my-tool"
    description = "My custom tool"
    
    def execute(self, **kwargs):
        # Implement tool logic
        pass
```
