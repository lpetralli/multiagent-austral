import streamlit as st
from agent import Agent
from langchain_core.messages import HumanMessage, AIMessage
agent = Agent()

# Main Streamlit app
st.title("Agent Chat Bot")

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
if prompt := st.chat_input("User input"):
    # Create a HumanMessage and add it to chat history
    human_message = HumanMessage(content=prompt)
    st.session_state.messages.append(human_message)

    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)

    # Debug: Print input to the graph in terminal
    print("\n===== DEBUG - INPUT TO AGENT =====")
    for i, msg in enumerate(st.session_state.messages):
        print(f"Message {i}: {msg.__class__.__name__} - Content: {msg.content[:100]}...")

    # Invoke the agent to get a list of AI messages with a spinner to show processing

    #TODO: Add streaming
    
    with st.spinner("Thinking..."):
        response = agent.invoke(st.session_state.messages)

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
