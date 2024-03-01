import openai
import os
import streamlit as st
from streamlit_chat import message

# Set API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

st.set_page_config(page_title="HiBots", page_icon=":robot_face:")

# Sidebar setup
st.sidebar.image("./hi_logo.png")
st.sidebar.title("HiBots")
st.sidebar.markdown("version  2024.02.29a")
st.sidebar.markdown("Harness your Intelligence Ecosystem™️")

# Add selection buttons in the sidebar
bot_selection = st.sidebar.radio(
    "Choose your bot:",
    ('PracticeBot', 'CoachBot'),
    key='bot_selection'
)

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = "gpt-4" # Default model
if 'modfile_contents' not in st.session_state:
    st.session_state['modfile_contents'] = ""
if 'last_bot_selection' not in st.session_state:
    st.session_state['last_bot_selection'] = ""

# Load modfile contents based on selection
if bot_selection != st.session_state['last_bot_selection']:
    if bot_selection == 'PracticeBot':
        modfile_path = "practiceBot_prompt.txt"
        st.header("Welcome to the HiBot Practice Arena 🤖")
        st.subheader("Get started by telling me about your industry and role.")
    elif bot_selection == 'CoachBot':
        modfile_path = "coachBot_prompt.txt"
        st.header("Welcome to the HiBot Coach 🤖")
        st.subheader("Tell me about your industry, role, and a challenge you would like to explore.")
    with open(modfile_path, "r") as f:
        st.session_state['modfile_contents'] = f.read()
    st.session_state['last_bot_selection'] = bot_selection

# Initialize messages with the current modfile_contents
if not st.session_state['messages']:
    st.session_state['messages'] = [{"role": "system", "content": st.session_state['modfile_contents']}]

clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [{"role": "system", "content": st.session_state['modfile_contents']}]

# Cached function for generating responses
@st.cache_data(show_spinner="Generating response...")
def generate_response(prompt, model_name):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(model=model_name, messages=st.session_state['messages'])
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})
    return response

# Container for chat history
response_container = st.container()

# Container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output = generate_response(user_input, st.session_state['model_name'])
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
