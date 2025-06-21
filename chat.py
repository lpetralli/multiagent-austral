import streamlit as st
from dotenv import load_dotenv
from agent import Agent
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# Initialize session state for user role
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# Initialize agent with user role if available
if "agent" not in st.session_state:
    st.session_state.agent = None

# Login screen
if st.session_state.user_role is None:
    # Add the image at the top, centered
    image_path = "Universidad Austral Logo.png"
    
    left_co, cent_co, last_co = st.columns(3)
    with cent_co:
        st.image(image_path, use_container_width=True)
    
    st.markdown("---")
    
    st.title("Bienvenido al Agente de la Universidad Austral")
    st.subheader("Por favor, selecciona tu rol:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👨‍🎓 Alumno", use_container_width=True):
            st.session_state.user_role = "alumno"
            st.session_state.agent = Agent(user_role="alumno")
            st.rerun()
    
    with col2:
        if st.button("👨‍🏫 Profesor", use_container_width=True):
            st.session_state.user_role = "profesor"
            st.session_state.agent = Agent(user_role="profesor")
            st.rerun()
    
    with col3:
        if st.button("💼 Administrativo", use_container_width=True):
            st.session_state.user_role = "administrativo"
            st.session_state.agent = Agent(user_role="administrativo")
            st.rerun()

else:
    # Chat interface
    # Add logout button in sidebar
    with st.sidebar:
        st.write(f"**Rol actual:** {st.session_state.user_role.capitalize()}")
        if st.button("Cerrar sesión"):
            st.session_state.user_role = None
            st.session_state.agent = None
            st.session_state.messages = []
            st.rerun()
    
    # Add the image at the bottom, centered
    image_path = "Universidad Austral Logo.png"
    
    left_co, cent_co, last_co = st.columns(3)
    with cent_co:
        st.image(image_path, use_container_width=True)
    
    st.markdown("---")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display all previous chat messages
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage) and message.content:
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage) and message.content and message.name == "supervisor":
            with st.chat_message("assistant"):
                st.markdown(message.content)
    
    # React to user input
    if prompt := st.chat_input("Escribe tu mensaje aquí..."):
        # Create a HumanMessage and add it to chat history
        human_message = HumanMessage(content=prompt)
        st.session_state.messages.append(human_message)
    
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
    
        # Debug: Print input to the graph in terminal
        print("\n===== DEBUG - INPUT TO AGENT =====")
        print(f"User role: {st.session_state.user_role}")
        for i, msg in enumerate(st.session_state.messages):
            print(f"Message {i}: {msg.__class__.__name__} - Content: {msg.content[:100]}...")
    
        # Invoke the agent to get a list of AI messages with a spinner to show processing
        with st.spinner("Pensando..."):
            response = st.session_state.agent.invoke(st.session_state.messages)
    
            # Debug: Print output from the graph in terminal
            print("\n===== DEBUG - OUTPUT FROM AGENT =====")
            print(f"Response keys: {list(response.keys())}")
            print(f"Number of messages: {len(response['messages'])}")
    
            # Update the session state with the new response
            st.session_state.messages = response["messages"]
    
            # Find the last supervisor message with content
            last_supervisor_message = None
            for message in reversed(response["messages"]):
                if isinstance(message, AIMessage) and message.content and message.name == "supervisor":
                    last_supervisor_message = message
                    break
    
            # Debug: Print details about the last message in terminal
            print(f"\n===== DEBUG - LAST SUPERVISOR MESSAGE =====")
            if last_supervisor_message:
                print(f"Type: {type(last_supervisor_message)}")
                print(f"Name: {last_supervisor_message.name}")
                print(f"Content preview: {last_supervisor_message.content[:100]}...")
    
                # Display the last supervisor message
                st.chat_message("assistant").markdown(last_supervisor_message.content)