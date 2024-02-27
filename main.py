import streamlit as st
from openai import OpenAI


# Page title
st.title("Chat-GPT Clone")


# message data exemple
# messages_dummy_data = [
#     {
#       "role": "user",
#       "avatar": "😃",
#       "content": "User message content",
#     },
#     {
#       "role": "assistant",
#       "avatar": "🤖",
#       "content": "Hello, how are you?",
#     },
# ]
MESSAGES = "messages"
OPENAI_API_KEY = "OPENAI_API_KEY"
OPEN_AI_MODEL = "gpt-3.5-turbo"
USER_AVATAR = "😃"
ASSISTANT_AVATAR = "🤖"
OpenAI.api_key = st.secrets[f"{OPENAI_API_KEY}"]

# Initialising state
if OPEN_AI_MODEL not in st.session_state:
    st.session_state["openai_model"] = OPEN_AI_MODEL


if MESSAGES not in st.session_state:
    st.session_state[MESSAGES] = []


# Display chat message from history on app re-run:
for messsage in st.session_state[MESSAGES]:
    with st.chat_message(name=messsage["role"], avatar=messsage["avatar"]):
        st.write(messsage["content"])


# React to user input
prompt = st.chat_input(placeholder="Type a message...", key="user_input")
if prompt:
    with st.chat_message(name='user', avatar=USER_AVATAR):
        st.write(prompt)
    # Add user message to chat history     
    st.session_state[MESSAGES].append(
      {
        "role": "user",
        "avatar": USER_AVATAR,
        "content": prompt,
      },
    )
    response = f"Echo: {prompt}"

    # Display assistant response in chat message container
    with st.chat_message(name='assistant', avatar=ASSISTANT_AVATAR):
        message_placeholder = st.empty()
        full_response = ""
        for response in OpenAI().chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {
                  "role": m["role"],
                  "content": m["content"],
                } for m in st.session_state[MESSAGES]
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.content or ""
            message_placeholder.write(full_response)
    st.session_state[MESSAGES].append(
        {
            "role": "assistant",
            "avatar": ASSISTANT_AVATAR,
            "content": full_response,
        },
    )
