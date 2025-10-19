# Multi Agentic Coding Framework using AutoGen

A comprehensive multi-agent system that automates the entire software development lifecycle using AutoGen 0.7.5's SelectorGroupChat architecture.

## Features

### Six Collaborative Agents Working Through SelectorGroupChat:

1. **📋 Requirement Analysis Agent** - Converts natural language to structured requirements
2. **💻 Coding Agent** - Generates functional, production-ready Python code
3. **🔍 Code Review Agent** - Reviews code for correctness, efficiency, and security
4. **📚 Documentation Agent** - Creates comprehensive documentation
5. **🧪 Test Case Generation Agent** - Generates unit and integration tests using pytest
6. **🚀 Deployment Configuration Agent** - Creates deployment scripts and configurations
7. **🎨 Streamlit Agent** - Creates streamlit UI screens

### Key Capabilities:

- **Iterative Code Improvement** - Automatic re-review loop with configurable iterations
- **Interactive Streamlit UI** - Beautiful, user-friendly interface
- **SelectorGroupChat Architecture** - Intelligent agent selection and coordination
- **Async/Await Support** - Efficient asynchronous processing
- **Automatic Output Generation** - Saves all artifacts to organized files
- **Processing History** - Track all previous runs
- **Template Library** - Pre-built requirement templates

## Architecture

The framework uses AutoGen's **SelectorGroupChat** pattern where:

- A model-based selector chooses the next agent to speak
- Agents collaborate through shared context
- Each agent has a specialized role and system message
- Termination conditions control workflow completion
- Messages flow through a centralized team structure

```
User Input → RequirementAnalyst → CodingAgent → CodeReviewer
                                        ↓ (if needs improvement)
                                    CodingAgent (iterate)
                                        ↓ (if approved)
                                  DocumentationAgent → TestAgent → DeploymentAgent
```

## Prerequisites

- **Python 3.10 or higher** (Required for AutoGen 0.7.5)
- **OpenAI API key** (or compatible API endpoint)
- **pip** package manager
- **Git** (for cloning repository)

## Installation

### Step 1: Clone or Download the Project

```bash
# Create project directory
mkdir multi_agentic_framework
cd multi_agentic_framework

# Download the files:
# - autogen_framework.py
# - streamlit_app.py
# - requirements.txt
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# .env file
GEMINI_API_KEY=gemini_api_key_here
OLLAMA_API_KEY=ollama_api_key
```

### Step 5: Run the streamlit application from application root folder

```bash
streamlit run streamlit_app.py
```