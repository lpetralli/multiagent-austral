from contextlib import asynccontextmanager
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from tools import add_employee_learning_status, create_one_mail_draft

model = ChatOpenAI(model="gpt-4o")

@asynccontextmanager
async def make_graph():
    # Configure MCP clients for different services
    async with MultiServerMCPClient(
        {
            "zapier": {
                "url": "https://actions.zapier.com/mcp/sk-ak-G0oxdyN6atDoKkALt8PHcICEAI/sse",
                "transport": "sse",
            }
        }
    ) as mcp_client:
        # Get MCP tools
        mcp_tools = mcp_client.get_tools()
        
        # Create agents with both custom and MCP tools
        employee_agent = create_react_agent(
            model=model,
            tools=[add_employee_learning_status] + mcp_tools,
            name="employee_agent",
            prompt="You are an employee agent responsible for managing employee learning status records. You have access to tools that can add employee learning status information to the system and other utility tools. Always use one tool at a time and only when necessary."
        )

        mail_agent = create_react_agent(
            model=model,
            tools= mcp_tools,
            name="mail_agent",
            prompt="You are a mail agent responsible for creating mail drafts. You have access to tools that can create mail drafts and other utility tools. Always use one tool at a time and only when necessary. You can't create more than one mail draft at a time."
        )

        # Create supervisor workflow
        workflow = create_supervisor(
            [employee_agent, mail_agent],
            model=model,
            output_mode="last_message",  # "full_history"
            prompt=(
                "You are a team supervisor managing an employee agent and a mail agent. "
                "For employee learning status records, use employee_agent. "
                "For mail drafts, use mail_agent. "
                "You also have access to math and weather tools through both agents."
            )
        )
        
        # Compile and yield the workflow
        app = workflow.compile()
        yield app

# Usage example:
# async def run_agent(query):
#     async with make_graph() as app:
#         response = await app.ainvoke({"input": query})
#         return response