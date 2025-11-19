# 💻 Coding Challenge Generator (FARM Stack)

An AI-powered, full-stack web application that lets users generate, solve, and manage coding challenges. Built using the FARM stack — **FastAPI**, **React**, and **MongoDB** — with additional integration of LLMs for intelligent challenge generation. Features AI-powered challenge creation, authentication, and containerised deployment with Docker, Kubernetes, and Nginx on AWS.

This project is designed to showcase a complete production-ready system, including:

🚀 Full-stack architecture (FastAPI + React + MongoDB)  
🤖 AI/LLM integration for automatic challenge generation  
📦 Dockerized services with Docker Compose  
🌐 Nginx as a reverse proxy and API gateway  
☁️ Deployed to AWS with Kubernetes  
📊 Future-ready with monitoring, CI/CD, and VectorDB support  


#### Project Outcome:

A fully functional, cloud-deployed AI system for interview question generation. Architected for extensibility, performance, and ease of integration with additional LLMs or frontend tools. Suitable for enterprise use or further customisation.

# How to run?

### Steps:

To begin this project, follow these steps:

1. Clone the repository to your local machine:

```
git clone https://github.com/M-Hamza380/Code-Challenge-Generator.git
```

2. Create a virtual environment: (using Python or uv)

```
python -m venv 'your virtual env folder name'
```

or 

```
uv venv 'your virtual env folder name'
```

3. Setting Environment Variable in PowerShell:

```
$env:UV_LINK_MODE = "copy"
```

Setting Environment Variable in Unix/Linux:

```
export UV_LINK_MODE=copy
```

4. Activate your virtual environment: (using VS Code CMD terminal)

```
your virtual env folder name\Scripts\activate
```

or 

PowerShell Execution Policy Issues:

If you receive an error stating that script execution is disabled, you need to change PowerShell's execution policy.

```
1. Close your current PowerShell session.
2. Open a new PowerShell window as an administrator.
3. Execute the following command to allow scripts to run:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Press Y to confirm the change.
```

4. Install the required libraries: (pyproject.toml)

```
uv sync --active
```

6. Open your terminal in VS Code and run the command:

```
python server.py
```
