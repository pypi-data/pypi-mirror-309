from setuptools import setup

# This setup.py exists for backwards compatibility. For actual configuration,
# see pyproject.toml

if __name__ == "__main__":
    setup(
        name="agentsys",
        version="0.7.0",
        packages=["agentsys"],
        python_requires=">=3.10",
        install_requires=[
            "openai>=1.0.0",
            "pydantic>=2.0.0",
            "locksys>=0.1.0",
        ],
        extras_require={
            "dev": [
                "pytest",
                "pytest-cov",
                "pytest-mock",
                "pytest-asyncio",
                "black",
            ]
        },
    )
