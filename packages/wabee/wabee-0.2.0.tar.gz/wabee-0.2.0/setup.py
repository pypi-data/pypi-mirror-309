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
{'': ['*'], 'wabee.cli.tools': ['templates/s2i/*', 'templates/s2i/bin/*']}

install_requires = \
['chardet>=5.2.0,<6.0.0',
 'grpcio-tools>=1.68.0,<2.0.0',
 'grpcio>=1.68.0,<2.0.0',
 'inquirer>=3.4.0,<4.0.0',
 'langchain>=0.1.14,<0.2.0',
 'matplotlib>=3.8.4,<4.0.0',
 'pandas>=2.2.2,<3.0.0',
 'restrictedpython>=7.1,<8.0']

entry_points = \
{'console_scripts': ['wabee = wabee.cli.main:main', 'wb = wabee.cli.main:main']}

setup_kwargs = {
    'name': 'wabee',
    'version': '0.2.0',
    'description': 'Wabee AI Software Development Kit',
    'long_description': '![PyPI - Downloads](https://img.shields.io/pypi/dm/wabee-sdk)\n![PyPI - Format](https://img.shields.io/pypi/format/wabee-sdk)\n![PyPI - Implementation](https://img.shields.io/pypi/implementation/wabee-sdk)\n![PyPI - License](https://img.shields.io/pypi/l/wabee-sdk)\n![PyPI - Status](https://img.shields.io/pypi/status/wabee-sdk)\n![PyPI - Version](https://img.shields.io/pypi/v/wabee-sdk)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/wabee-sdk)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wabee-sdk)\n\n![Wabee AI](https://wabee-public-assets.s3.amazonaws.com/images/wabee-small-box-white.png)\n\n**wabee-sdk** is a Python module for development of modules and extensions for the Wabee agentic AI platform.\n\nWebsite: https://wabee.ai/\n\n# Installation\n\n## Dependencies\n\nwabee-sdk requires:\n\n- python = ">=3.10,<3.12"\n- langchain = "^0.1.14"\n- chardet = "^5.2.0"\n- pandas = "^2.2.2"\n- restrictedpython = "^7.1"\n- matplotlib = "^3.8.4"\n\n## User Installation\n\nThe easiest way to install the package is through `pip`:\n\n```sh\npip install -i https://test.pypi.org/pypi/ --extra-index-url https://pypi.org/simple wabee-sdk\n```\n\n# Command Line Interface\n\nThe wabee-sdk also comes as a CLI to make the process of development wabee agents tools faster and easier!\n\nTo create a brand new tool, one just needs to run:\n\n```sh\nwb tools create tool-name\n```\n\nAnd that\'s it, with no time wasted implementing boilerplate code, the tool is ready to be executed and updated according to the business requirements.\n\n# Example\n\n## Tool Configuration\n\nTo create a tool manually, the first step is to define its configuration. In other words, all the necessary data to initialize the tool must be held by this object.\n\n```python\nclass APIGatewayToolConfig(WabeeAgentToolConfig):\n    base_url: str\n    api_key: str\n```\n\n## Tool Input\n\nThen, define the tool input, which is the data that will be processed by the tool, for instance\n\n```python\nclass APIGatewayToolConfig(WabeeAgentToolInput):\n    headers: dict[str, str] = WabeeAgentToolField(\n        name="headers",\n        description="http request headers",\n        example={\n            "Content-Type": "application/json"\n        }\n    )\n```\n\nFinally, implement the tool itself, following the example below:\n\n## Tool\n\n```python\nclass APIGatewayTool(WabeeAgentTool):\n    base_url: str\n    api_key: str\n\n    def execute(\n        self,\n        api_gateway_tool_input: APIGatewayToolInput\n    ) -> str:\n        print(f"Requesting API on {self.base_url} with headers: {api_gateway_tool_input.headers}")\n        return "200"\n\n    @classmethod\n    def create(\n        cls,\n        api_gateway_tool_config: APIGatewayToolConfig\n    ) -> APIGatewayTool:\n        return cls(\n            name="api_gateway_tool",\n            description="api_gateway_tool",\n            base_url=api_gateway_tool_config.base_url,\n            api_key=api_gateway_tool_config.api_key\n        )\n```\n\n## Tool Factory\n\nThe last step is to expose a factory function so other modules can easily instantiate the tool.\n\n```python\ndef _create_tool(**kwargs: Any) -> WabeeAgentTool:\n    return APIGatewayTool.create(APIGatewayToolConfig(**kwargs))\n```\n\nAlthough, it is possible to create the tool manually, it is highly recommended to create it using the CLI. Moreover, it is mandatory to keep all the classes and functions on the same file!\n',
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
