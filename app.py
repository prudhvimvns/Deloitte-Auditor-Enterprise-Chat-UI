import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = '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'

# Add custom CSS to set the background to white
st.markdown(
    """
    <style>
    body {
        background-color: white;
    }
    .title-container {
        background-color: blue;
        padding: 10px;
        color:white;
    }
    .get-answer-button {
        background-color: blue;
        color: white;
    }
    .cancel-button {
        background-color: purple;
        color: white;
    }
    .response-box {
        padding: 20px;
        background-color: lightgray;
        display: block;
        max-height: 100px;
        color: gray;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title-container" style="font-size:x-large;"><b>Deloitte Auditor Enterprise Chat UI</b></div>', unsafe_allow_html=True)

# Input box for user's question with a placeholder
user_input = st.text_input("Enter your Tax Prompt here:", key="user_input", value="", placeholder="Tax Prompt", help="Tax prompt")

# Create a row with two columns for buttons
col1, col2 = st.columns(2)

# Flag to track if the "Get Answer" button is clicked
button_clicked = col1.button("Send", key="get-answer-button")

# "Cancel" button to clear input
cancel_button = col2.button("Cancel", key="cancel-button")

# Text area for response
# response_text = st.markdown('<div class="response-box"></div>', unsafe_allow_html=True)
response_text = st.markdown('<div class="response-box">Response</div>', unsafe_allow_html=True)

if button_clicked and user_input:
    # Use OpenAI to generate a response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="I have a tax question: " + user_input,
        max_tokens=150  # Adjust token limit as needed
    )

    # Extract the response text
    chatbot_response = response.choices[0].text

    # Display the response
    response_text = st.markdown('<div class="response-box">' + chatbot_response + '</div>', unsafe_allow_html=True)
