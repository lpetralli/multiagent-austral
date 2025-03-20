from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from tools import add_employee_learning_status, create_one_mail_draft

model = ChatOpenAI(model="gpt-4o")

employee_agent = create_react_agent(
    model=model,
    tools=[add_employee_learning_status],
    name="employee_agent",
    prompt="You are an employee agent responsible for managing employee learning status records. You have access to tools that can add employee learning status information to the system. Always use one tool at a time and only when necessary."
)

mail_agent = create_react_agent(
    model=model,
    tools=[create_one_mail_draft],
    name="mail_agent",
    prompt="You are a mail agent responsible for creating mail drafts. You have access to tools that can create mail drafts. Always use one tool at a time and only when necessary. You can't create more than one mail draft at a time."
)

# Create supervisor workflow
workflow = create_supervisor(
    [employee_agent, mail_agent],
    model=model,
    output_mode="last_message", # "full_history"
    prompt=(
        "You are a team supervisor managing a employee agent and a mail agent. "
        "For employee learning status records, use employee_agent. "
        "For mail drafts, use mail_agent."
    )
)
# Compile and run
app = workflow.compile()