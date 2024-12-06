from setuptools import setup, find_packages

setup(
    name="agentsys",
    version="0.3.0",
    packages=find_packages(include=['agentsys', 'agentsys.*', 'core', 'middleware', 'plugins', 'protocols', 'config']),
    install_requires=[
        "numpy",
        "pydantic>=2.0.0",
        "python-dotenv>=0.19.0",
        "typing-extensions>=4.0.0",
        "aiofiles>=23.2.1",
        "pytest-asyncio>=0.23.0",
        "aiohttp>=3.9.0",
        "asyncio>=3.4.3"
    ],
)
