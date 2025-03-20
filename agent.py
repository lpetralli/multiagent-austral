# agent.py
from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

class Agent:
    def __init__(self, model_name="gpt-4o"):
        """Initialize the agent with OpenAI API key and model name."""
        self.model = ChatOpenAI(model=model_name)
        self.graph = None
        self._initialize_workflow()
        
    def _initialize_workflow(self):
        """Initialize the employee and mail agents and create the supervisor workflow."""
        # Import tools here to avoid circular imports
        from tools import add_employee_learning_status, create_one_mail_draft
        
        # Create employee agent
        employee_agent = create_react_agent(
            model=self.model,
            tools=[add_employee_learning_status],
            name="employee_agent",
            prompt="You are an employee agent responsible for managing employee learning status records. You have access to tools that can add employee learning status information to the system. Always use one tool at a time and only when necessary."
        )
        
        # Create mail agent
        mail_agent = create_react_agent(
            model=self.model,
            tools=[create_one_mail_draft],
            name="mail_agent",
            prompt="You are a mail agent responsible for creating mail drafts. You have access to tools that can create mail drafts. Always use one tool at a time and only when necessary. You can't create more than one mail draft at a time."
        )
        
        # Create supervisor workflow
        workflow = create_supervisor(
            [employee_agent, mail_agent],
            model=self.model,
            output_mode="last_message",
            prompt=(
                "You are a team supervisor managing an employee agent and a mail agent. "
                "For employee learning status records, use employee_agent. "
                "For mail drafts, use mail_agent."
            )
        )
        
        # Compile workflow
        self.graph = workflow.compile()
    
    def invoke(self, messages):
        """
        Invoke the agent with a list of messages.
        
        Args:
            messages: List of message objects
            
        Returns:
            Dictionary with updated messages
        """
        if self.graph is None:
            raise ValueError("Workflow has not been initialized")
        
        # Initialize the state with the provided messages
        initial_state = {"messages": messages}
        
        # Run the graph synchronously and obtain the output
        #graph_output = self.graph.stream(initial_state, stream_mode="updates")
        graph_output = self.graph.invoke(initial_state)
        return graph_output