import streamlit as st 
from be import chatbot
from langchain_core.messages import HumanMessage
CONFIG = {"configurable": {"thread_id": "1"}}
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = [] # so that our chats are not lost when we click enter that
    #just reruns whole page and msg history is refreshed

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')
if user_input:
    st.session_state['message_history'].append({"role": "user", "content": user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]},config=CONFIG)
    # ai_message = response['messages'][-1].content
    # st.session_state['message_history'].append({"role": "assistant", "content": ai_message})
    # with st.chat_message('assistant'):
    #     st.text(ai_message)

    # Streaming: stream message chunks and show tokens as they arrive
    def stream_message_chunks():
        for message_chunk, _metadata in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode="messages",
        ):
            if getattr(message_chunk, "content", None):
                yield message_chunk.content

    with st.chat_message("assistant"):
        full_response = st.write_stream(stream_message_chunks())
    st.session_state["message_history"].append({"role": "assistant", "content": full_response})