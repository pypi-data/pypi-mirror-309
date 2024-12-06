# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wabee',
 'wabee.cli',
 'wabee.cli.commands',
 'wabee.cli.tools',
 'wabee.rpc',
 'wabee.rpc.protos',
 'wabee.tools']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=5.2.0,<6.0.0',
 'grpcio-tools>=1.68.0,<2.0.0',
 'grpcio>=1.68.0,<2.0.0',
 'inquirer>=3.4.0,<4.0.0',
 'pyyaml>=6.0.1,<7.0.0',
 'restrictedpython>=7.1,<8.0']

entry_points = \
{'console_scripts': ['wabee = wabee.cli.main:main', 'wb = wabee.cli.main:main']}

setup_kwargs = {
    'name': 'wabee',
    'version': '0.2.1',
    'description': 'Wabee AI Software Development Kit',
    'long_description': '![PyPI - Downloads](https://img.shields.io/pypi/dm/wabee)\n![PyPI - Format](https://img.shields.io/pypi/format/wabee)\n![PyPI - Implementation](https://img.shields.io/pypi/implementation/wabee)\n![PyPI - License](https://img.shields.io/pypi/l/wabee)\n![PyPI - Status](https://img.shields.io/pypi/status/wabee)\n![PyPI - Version](https://img.shields.io/pypi/v/wabee)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/wabee)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wabee)\n\n![Wabee AI](https://wabee-public-assets.s3.amazonaws.com/images/wabee-small-box-white.png)\n\n# Wabee SDK\n\n**wabee-sdk** is a Python module for development of modules and extensions for the Wabee agentic AI platform.\n\n## Installation\n\n```bash\npip install wabee\n```\n\n## Command Line Interface (CLI)\n\nThe Wabee SDK includes a powerful CLI tool to streamline the development of Wabee agent tools.\n\n### Creating a New Tool\n\nCreate a new tool using the interactive CLI:\n\n```bash\nwabee tools create\n```\n\nThis command will prompt you for:\n- Tool name\n- Tool type (simple or complete)\n- Tool description\n- Initial version\n\n#### Tool Types\n\n1. **Simple Tool**: \n   - Ideal for straightforward, single-function tools\n   - Uses the `@simple_tool` decorator\n   - Less boilerplate code\n   - Perfect for quick implementations\n\n2. **Complete Tool**:\n   - Full class implementation\n   - More control over tool behavior\n   - Better for complex tools with multiple operations\n   - Includes error handling infrastructure\n\n### Building Tool Containers\n\nBuild a tool into a container image:\n\n```bash\nwabee tools build <tool_directory> [options]\n```\n\nOptions:\n- `--image`: Specify custom image name (default: toolname:latest)\n\nExample:\n```bash\nwabee tools build ./my-tool\n```\n\n## Tool Project Structure\n\nWhen you create a new tool, the following structure is generated:\n\n```\nmy_tool/\n├── my_tool_tool.py      # Main tool implementation\n├── requirements.txt     # Python dependencies\n├── server.py           # gRPC server implementation\n└── toolspec.yaml       # Tool specification and metadata\n```\n\n## RPC Server\n\nEach built tool runs as a gRPC server that exposes a standardized interface for tool execution. The server:\n\n- Listens on port 50051 by default (configurable via WABEE_GRPC_PORT)\n- Automatically handles input validation using your Pydantic schemas\n- Provides standardized error handling and reporting\n- Supports streaming responses for long-running operations\n\nWhen you build a tool with `wabee tools build`, the resulting container image includes:\n- Your tool implementation\n- All dependencies\n- A pre-configured gRPC server\n- Generated protocol buffers for type-safe communication\n\nYou can run the built container with:\n```bash\ndocker run -p 50051:50051 mytool:latest\n```\n\n### toolspec.yaml\n\nThe tool specification file contains metadata about your tool:\n\n```yaml\ntool:\n  name: MyTool\n  description: Your tool description\n  version: 0.1.0\n  entrypoint: my_tool_tool.py\n```\n\n### Requirements\n\n- Python >=3.11,<3.12\n- Docker (for building containers)\n- Internet connection (for downloading S2I builder)\n\n## Development Examples\n\n### Simple Tool Example\n\n```python\nfrom pydantic import BaseModel\nfrom wabee.tools.simple_tool import simple_tool\n\nclass MyToolInput(BaseModel):\n    message: str\n\n@simple_tool(schema=MyToolInput)\nasync def my_tool(input_data: MyToolInput) -> str:\n    return f"Processed: {input_data.message}"\n```\n\n### Complete Tool Example\n\n```python\nfrom typing import Optional, Type\nfrom pydantic import BaseModel\nfrom wabee.tools.base_tool import BaseTool\nfrom wabee.tools.tool_error import ToolError\n\nclass MyToolInput(BaseModel):\n    message: str\n\nclass MyTool(BaseTool):\n    args_schema: Type[BaseModel] = MyToolInput\n\n    async def execute(self, input_data: MyToolInput) -> tuple[Optional[str], Optional[ToolError]]:\n        try:\n            result = f"Processed: {input_data.message}"\n            return result, None\n        except Exception as e:\n            return None, ToolError(type="EXECUTION_ERROR", message=str(e))\n```\n\n## Contributing\n\nSuggestions are welcome! Please feel free to submit bug reports or feedbacks as a Github issues.\n\n## Links\n\n- Website: https://wabee.ai/\n- Documentation: https://documentation.wabee.ai\n- GitHub: https://github.com/wabee-ai/wabee-sdk\n\n',
    'author': 'Developers',
    'author_email': 'developers@wabee.ai',
    'maintainer': 'Developers',
    'maintainer_email': 'developers@wabee.ai',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
