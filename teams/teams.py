import asyncio

from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console

from agents.agents import requirement_analysis_agent, coding_agent, code_review_agent, document_agent, test_cases_agent, \
    deployment_agent, streamlit_agent
from models.model_clients import gemini_model_client

participants = [
    requirement_analysis_agent, coding_agent, code_review_agent, document_agent, test_cases_agent, deployment_agent, streamlit_agent
]

max_iterations = 20
termination = TextMentionTermination("WORKFLOW_COMPLETE") | MaxMessageTermination(max_messages=max_iterations)

team = SelectorGroupChat(
    participants=participants,
    model_client=gemini_model_client,
    termination_condition=termination
)

user_input = """Create a Python function that calculates the Fibonacci sequence up to n numbers.
    The function should be efficient, handle edge cases (n <= 0, n = 1, n = 2),
    and include input validation. It should return a list of Fibonacci numbers."""

task_message = TextMessage(
    content=f"""Develop an application based on the following requirement.
     {user_input}
     
     Please follow this workflow:
    1. RequirementAnalysisAgent: Analyze and create structured requirements
    2. CodingAgent: Implement the code based on requirements
    3. CodeReviewAgent: Review the code (if needs improvement, send back to CodingAgent - max {max_iterations} iterations)
    4. DocumentationAgent: Generate comprehensive documentation
    5. TestCasesAgent: Create unit and integration tests
    6. DeploymentAgent: Generate deployment configuration
    7. StreamlitAgent: Generate streamlit UI
    
    Each agent should complete their task and hand off to the next agent.
    
    CodeReviewAgent can request improvements upto {max_iterations - 4} times.
    Please follow this workflow and start with RequirementAnalysisAgent.
    After all the tasks are completed, end with WORKFLOW_COMPLETE.
""",
    source="user"
)

async def run_task():
    await Console(team.run_stream(task=task_message))

asyncio.run(run_task())