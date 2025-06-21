# agent.py
from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from datetime import datetime

class Agent:
    def __init__(self, model_name="gpt-4.1", user_role=None):
        """Initialize the agent with OpenAI API key and model name."""
        self.model = ChatOpenAI(model=model_name)
        self.user_role = user_role
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
        role_info = ""
        if self.user_role:
            role_mapping = {
                "alumno": "student",
                "profesor": "professor", 
                "administrativo": "administrative staff"
            }
            role_in_english = role_mapping.get(self.user_role, self.user_role)
            role_info = f"The user has identified themselves as: {self.user_role} ({role_in_english}). "
        
        # Define tool capabilities for each agent
        tools_info = """
        IMPORTANT: Here are the specific tools each subagent has access to:
        
        STUDENT AGENT TOOLS:
        - consultar_faltas: Check how many absences a student has in their courses and if they risk failing due to attendance
        - gestionar_recordatorio_examen: Send exam reminders or check exam dates for courses
        
        PROFESSOR AGENT TOOLS:
        - subir_tema_siu: Upload class topics to SIU system (validates against syllabus)
        - crear_recordatorio_evento: Create academic event reminders for students in AI and Big Data courses
        - gestionar_archivo_materia: Manage course files (upload, hide, show, or delete files in virtual campus)
        
        ADMINISTRATIVE AGENT TOOLS:
        - enviar_recordatorio_horas_siu: Send reminders to professors who haven't logged their teaching hours
        - procesar_redencion_gastos: Process expense reimbursements (automatically classifies as reimbursable or non-reimbursable)
        - crear_post_linkedin: Create and publish professional content on LinkedIn using AI
        
        When a user asks what you can help with, explain the relevant capabilities based on their role.
        """
        
        workflow = create_supervisor(
            [student_agent, professor_agent, administrative_agent],
            model=self.model,
            output_mode="last_message",
            prompt=(
                f"You are a team supervisor managing a student agent, professor agent, and administrative agent. "
                f"{role_info}"
                f"{tools_info}\n"
                "For student-related tasks, use student_agent. "
                "For professor-related tasks, use professor_agent. "
                "For administrative staff tasks, use administrative_agent. "
                "The subagents are in charge of using their tools if applicable, confirming whether the tool call was successful or not, and then their turn ends. "
                "After a subagent completes its task, you should respond to the user with the appropriate information. "
                + ("" if self.user_role else "If the user's role (student, professor, or administrative staff) is not clear from their message, you must first ask them to specify their role before proceeding with any task. "
                "For example, you could say: 'Para poder ayudarte mejor, ¿podrías indicarme si eres estudiante, profesor o personal administrativo?' ") +
                "Do not mention other agents, neither any delegation of tasks, to the final user. You are the supervisor, you will be the one to answer back to the student, professor, and administrative staff. "
                "When users ask how you can help or what you can do, explain the specific capabilities available for their role based on the tools information above. "
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