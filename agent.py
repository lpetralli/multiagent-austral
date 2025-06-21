# agent.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from datetime import datetime

class Agent:
    def __init__(self, model_name="gemini-2.0-flash"):
        """Initialize the agent with Google Gemini model."""
        # Get API key from environment variable
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        self.model = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0,
            google_api_key=api_key
        )
        self.graph = None
        self._initialize_workflow()
        
    def _initialize_workflow(self):
        """Initialize the student, professor, and administrative agents and create the supervisor workflow."""
        # Import tools here to avoid circular imports
        from tools import subir_tema_siu, crear_recordatorio_evento, gestionar_archivo_materia, enviar_recordatorio_horas_siu, consultar_faltas, gestionar_recordatorio_examen, procesar_redencion_gastos, crear_post_linkedin
        
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Create student agent
        student_agent = create_react_agent(
            model=self.model,
            tools=[consultar_faltas, gestionar_recordatorio_examen],
            name="student_agent",
            prompt=
            f"""
            You are a student agent responsible for helping students with academic tasks. You have access to tools that can help students submit assignments and manage their academic records. 
            Always use one tool at a time and only when necessary.
            Do not answer back to the student, you report back to the supervisor agent so tha he can answer back to the student.
            Today's date is {current_date}.
            """
        )
        
        # Create professor agent
        professor_agent = create_react_agent(
            model=self.model,
            tools=[crear_recordatorio_evento, subir_tema_siu, gestionar_archivo_materia],
            name="professor_agent",
            prompt=
            f"""
            You are a professor agent responsible for helping professors with academic management. You have access to tools that can create academic event reminders and manage course information. 
            Always use one tool at a time and only when necessary. The SIU is the name for the learning management system of the university.
            Do not answer back to the professor, you report back to the supervisor agent so tha he can answer back to the professor.
            Today's date is {current_date}.
            """
        )
        
        # Create administrative agent
        administrative_agent = create_react_agent(
            model=self.model,
            tools=[enviar_recordatorio_horas_siu, procesar_redencion_gastos, crear_post_linkedin],
            name="administrative_agent",
            prompt=
            f"""
            You are an administrative agent responsible for helping administrative staff with university management tasks. You have access to tools that can help with administrative procedures. 
            Always use one tool at a time and only when necessary.
            Do not answer back to the administrative staff, you report back to the supervisor agent so tha he can answer back to the administrative staff.
            Today's date is {current_date}.
            """
        )

        # Create supervisor workflow
        workflow = create_supervisor(
            [student_agent, professor_agent, administrative_agent],
            model=self.model,
            output_mode="last_message",
            prompt=(
                f"You are a team supervisor managing a student agent, professor agent, and administrative agent. "
                "For student-related tasks like submitting assignments, use student_agent. "
                "For professor-related tasks like creating academic event reminders, use professor_agent. "
                "For administrative staff tasks like university management procedures, use administrative_agent. "
                "The subagents are in charge of using their tools if applicable, confirming whether the tool call was successful or not, and then their turn ends. "
                "After a subagent completes its task, you should respond to the user with the appropriate information. "
                "If the user's role (student, professor, or administrative staff) is not clear from their message, you must first ask them to specify their role before proceeding with any task. "
                "For example, you could say: 'Para poder ayudarte mejor, ¿podrías indicarme si eres estudiante, profesor o personal administrativo?' "
                "Do not mention other agents, neither any delegation of tasks, to the final user. You are the supervisor, you will be the one to answer back to the student, professor, and administrative staff."
                f"Today's date is {current_date}."
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