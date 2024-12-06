from setuptools import setup, find_packages

setup(
    name="sonika-langchain-bot",
    version="0.0.4", 
    description="Agente langchain con LLM",
    author="Erley Blanco Carvajal",
    license="MIT License",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Encuentra automáticamente todos los paquetes
    install_requires=[
        "langchain==0.3.0",
        "langchain-community==0.3.0",
        "langchain-core==0.3.5",
        "langchain-openai==0.2.0",
        "langgraph==0.2.39",
        "langgraph-checkpoint==2.0.2",
        "langgraph-sdk==0.1.34",
        "dataclasses-json==0.6.7",
        "python-dateutil==2.9.0.post0",
        "tiktoken==0.7.0",
        "pydantic==2.9.2",
        "faiss-cpu==1.8.0.post1",
        "pypdf==5.0.0",
        "python-dotenv==1.0.1",
        "typing_extensions==4.12.0",
        "typing-inspect==0.9.0",
    ],
    extras_require={
        "dev": [
            "sphinx>=8.1.3,<9.0.0",
            "sphinx-rtd-theme>=3.0.1,<4.0.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Cambia según la versión mínima de Python que soportes
)
