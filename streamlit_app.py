import asyncio
import streamlit as st
from datetime import datetime

from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMessageTermination, MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import TextMessage

from agents.agents import (
    requirement_analysis_agent,
    coding_agent,
    code_review_agent,
    document_agent,
    test_cases_agent,
    deployment_agent,
    streamlit_agent
)
from models.model_clients import ollama_client

# Page config
st.set_page_config(
    page_title="Multi Agent Coding Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi Agent Coding Agent")
st.markdown("*Automated development workflow with AI agents*")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    max_iterations = st.slider("Max Iterations", 5, 50, 20)
    st.markdown("---")
    st.markdown("### 🔄 Workflow Steps")
    st.markdown("""
    1. 📋 **Requirement Analysis**
    2. 💻 **Coding**
    3. 🔍 **Code Review**
    4. 📝 **Documentation**
    5. 🧪 **Test Cases**
    6. 🚀 **Deployment Config**
    7. 🎨 **Streamlit UI**
    """)

# Main input area
st.header("📝 Enter Your Requirement")
user_input = st.text_area(
    "Describe what you want to build:",
    placeholder="Example: Create a Python application that calculates the Fibonacci sequence...",
    height=150
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'running' not in st.session_state:
    st.session_state.running = False


async def run_team_workflow(user_requirement: str, max_iter: int):
    """Run the multi-agent team workflow"""

    participants = [
        requirement_analysis_agent,
        coding_agent,
        code_review_agent,
        document_agent,
        test_cases_agent,
        deployment_agent,
        streamlit_agent
    ]

    termination = TextMessageTermination("WORKFLOW_COMPLETE") | MaxMessageTermination(max_messages=max_iter) | TextMentionTermination("WORKFLOW_COMPLETE")

    team = SelectorGroupChat(
        participants=participants,
        model_client=ollama_client,
        termination_condition=termination,
        selector_prompt="After all the tasks are completed, end with WORKFLOW_COMPLETE."
    )

    task_message = TextMessage(
        content=f"""Develop an application based on the following requirement.
        {user_requirement}

        Please follow this workflow:
        1. RequirementAnalysisAgent: Analyze and create structured requirements
        2. CodingAgent: Implement the code based on requirements
        3. CodeReviewAgent: Review the code (if needs improvement, send back to CodingAgent - max {max_iter} iterations)
        4. DocumentationAgent: Generate comprehensive documentation
        5. TestCasesAgent: Create unit and integration tests
        6. DeploymentAgent: Generate deployment configuration
        7. StreamlitAgent: Generate streamlit UI

        Each agent should complete their task and hand off to the next agent.

        CodeReviewAgent can request improvements upto {max_iter - 4} times.
        Please follow this workflow and start with RequirementAnalysisAgent.
        """,
        source="user"
    )

    # Collect messages
    messages = []
    async for agent_message in team.run_stream(task=task_message):
        messages.append(agent_message)
        yield agent_message

    # return messages


def get_agent_icon(agent_name: str) -> str:
    """Return emoji icon for each agent"""
    icons = {
        "RequirementAnalysis": "📋",
        "Coding": "💻",
        "CodeReview": "🔍",
        "Documentation": "📝",
        "TestCases": "🧪",
        "Deployment": "🚀",
        "Streamlit": "🎨"
    }
    for key, icon in icons.items():
        if key.lower() in agent_name.lower():
            return icon
    return "🤖"


def display_message(agent_message, index):
    """Display a message in a formatted container"""
    source = getattr(agent_message, 'source', 'Unknown')
    content = getattr(agent_message, 'content', str(agent_message))

    icon = get_agent_icon(source)

    with st.container():
        col1, col2 = st.columns([0.15, 0.85])

        with col1:
            st.markdown(f"### {icon}")
            st.caption(source)

        with col2:
            with st.expander(f"**Message {index + 1}** - {source}", expanded=True):
                st.markdown(content)

                # If content looks like code, show it in a code block
                if "```" in content or "def " in content or "class " in content:
                    st.code(content, language="python")

        st.markdown("---")


# Run button
if st.button("🚀 Start Agent Workflow", type="primary", disabled=st.session_state.running):
    if not user_input.strip():
        st.error("⚠️ Please enter a requirement first!")
    else:
        st.session_state.running = True
        st.session_state.messages = []

        # Progress area
        progress_placeholder = st.empty()
        messages_placeholder = st.container()

        with progress_placeholder:
            with st.spinner("🔄 Coding Agent Team is working..."):
                try:
                    # Run the workflow
                    async def process():
                        message_count = 0
                        async for agent_message in run_team_workflow(user_input, max_iterations):
                            st.session_state.messages.append(agent_message)
                            message_count += 1

                            # Update display in real-time
                            with messages_placeholder:
                                st.markdown(f"### 📨 Agent Messages ({message_count})")
                                for index, msg in enumerate(st.session_state.messages):
                                    display_message(msg, index)


                    # Run async function
                    asyncio.run(process())

                    progress_placeholder.success(f"✅ Workflow completed! Generated {len(st.session_state.messages)} messages.")

                except Exception as e:
                    progress_placeholder.error(f"❌ Error: {str(e)}")
                    st.exception(e)
                finally:
                    st.session_state.running = False

# Display existing messages
if st.session_state.messages:
    st.markdown("---")
    st.markdown(f"### 📨 Agent Messages ({len(st.session_state.messages)})")

    for idx, message in enumerate(st.session_state.messages):
        display_message(message, idx)

    # Download button for all messages
    if st.button("💾 Download All Messages"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        all_content = "\n\n".join([
            f"=== Message {i + 1} - {getattr(msg, 'source', 'Unknown')} ===\n{getattr(msg, 'content', str(msg))}"
            for i, msg in enumerate(st.session_state.messages)
        ])
        st.download_button(
            label="📥 Download as Text File",
            data=all_content,
            file_name=f"agent_messages_{timestamp}.txt",
            mime="text/plain"
        )

# Footer
st.markdown("---")
st.caption("Built with Streamlit and AutoGen | Multi-Agent Development Team")