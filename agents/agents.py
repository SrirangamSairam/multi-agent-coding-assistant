from autogen_agentchat.agents import AssistantAgent

from models.model_clients import gemini_model_client, ollama_client


requirement_analysis_agent = AssistantAgent(
    name="RequirementAnalysisAgent",
    description="Agent that takes requirements in natural human language and refines them into structure software requirements.",
    model_client=ollama_client,
    system_message="You are an expert senior software engineer that takes requirements in natural human language and refines them into structure software requirements."
)

coding_agent = AssistantAgent(
    name="CodingAgent",
    description="Agent that takes structured software requirements and generates production ready code and validates the code by executing it.",
    model_client=ollama_client,
    system_message="You are a Python language expert with expertise in all Python Frameworks. "
                "Your first task is to take structured software requirements and create a production ready code base following all the best and latest practices. "
                "Ensure you choose an appropriate framework for the given requirements. "
                "The generated code should be easily scalable, follows chosen frameworks' code base structure. "
                "Your Second task is to execute the generated code and validate it. "
                "Ensure that the code is generating expected results after executing it."
                "No matter the requirement, the code generated should use a framework so that it can be deployed and ran on an Azure app service."
)

# code_executor = DockerCommandLineCodeExecutor(work_dir="coding")
# coding_agent = CodeExecutorAgent(
#     name="CodingAgent",
#     description="Agent that takes structured software requirements and generates production ready code and validates the code by executing it.",
#     model_client=ollama_client,
#     code_executor=code_executor,
#     system_message="You are a Python language expert with expertise in all Python Frameworks. "
#                 "Your first task is to take structured software requirements and create a production ready code base following all the best and latest practices. "
#                 "Ensure you choose an appropriate framework for the given requirements. "
#                 "The generated code should be easily scalable, follows chosen frameworks' code base structure. "
#                 "Your Second task is to execute the generated code and validate it. "
#                 "Ensure that the code is generating expected results after executing it.",
# )

code_review_agent = AssistantAgent(
    name="CodeReviewAgent",
    description="Agent that takes a Python code and reviews it for correctness, efficiency, and security. "
                "If improvements are needed, it provides feedback for re-iteration",
    model_client=ollama_client,
    system_message="You are an expert in python code. "
                   "Your task is to take the code and review it for correctness, efficiency, and security. "
                   "If improvements are needed, please provide proper feedback for re-iteration. "
)

document_agent = AssistantAgent(
    name="DocumentationAgent",
    description="Agent that takes a Python code and generates documentation.",
    model_client=ollama_client,
    system_message="You are an expert in python code. "
                   "Your first task is to take the code and generate proper documentation. "
                   "The generated documentation should cover steps to setup, cover why a decision is made and should explain complex logics."
)

test_cases_agent = AssistantAgent(
    name="TestCasesAgent",
    description="Agent that takes a Python code and generates test cases.",
    model_client=ollama_client,
    system_message="You are an expert in python code. "
                   "Your first task is to take the code and generate proper test cases. "
                   "The generated test cases should test all the possible scenarios both positive and negative ."
                   "Ensure Edge cases are thoroughly tested."
)

deployment_agent = AssistantAgent(
    name="DeploymentAgent",
    description="Agent that takes a Python code and generates deployment scripts.",
    model_client=ollama_client,
    system_message="You are an expert DevOps engineer. "
                   "Your first task is to take the code and generate proper deployment scripts. "
                   "Assume you are deploying to an Azure App Service and Github Actions for CICD. "
                   "Follow best practices for generating deployment scripts and ensure all the requirements are fully considered."
)

streamlit_agent = AssistantAgent(
    name="StreamlitAgent",
    description="Agent that takes a Python code and generates streamlit UI.",
    model_client=ollama_client,
    system_message="You are an expert Python developer. "
                   "Your task is to take understand the backend code and generate appropriate UI using Streamlit. "
                   "The UX should be easy for any non-technical and technical people to navigate. "
                   "Ensure all the UI button actions are properly integrated with backend API's ."
                   "Also add a default 404 page or redirect the users to home page if they are wrong path.",
)