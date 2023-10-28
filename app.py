import sqlite3
import openai
import streamlit as st
import datetime

# Set your OpenAI API key
openai.api_key = ''

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS tax_prompts_and_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_input TEXT NOT NULL,
    chatbot_response TEXT NOT NULL,
    created_at DATETIME NOT NULL
)
"""

def save_tax_prompt_and_response(user_input, chatbot_response):
    conn = sqlite3.connect("tax_prompts_and_responses.db")
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    now = datetime.datetime.now()
    cursor.execute("INSERT INTO tax_prompts_and_responses (user_input, chatbot_response, created_at) VALUES (?, ?, ?)",
                   (user_input, chatbot_response, now))
    conn.commit()

def generate_chatbot_response(user_input):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="I have a tax question: " + user_input,
        max_tokens=150  # Adjust token limit as needed
    )
    return response.choices[0].text.strip()

def main():
    st.markdown('<div class="title-container" style="font-size:x-large;"><b>Deloitte Auditor Enterprise Chat UI</b></div>', unsafe_allow_html=True)
    user_input = st.text_input("Enter your Tax Prompt here:", key="user_input", value="", placeholder="Tax Prompt", help="Tax prompt")
    col1, col2 = st.columns(2)
    button_clicked = col1.button("Send", key="get-answer-button")
    save_button = col2.button("Save to SQL", key="save-button")
    response_text = st.empty()
    saved_message = st.empty()

    if button_clicked and user_input:
        chatbot_response = generate_chatbot_response(user_input)
        response_text.markdown('<div class="response-box">' + chatbot_response + '</div>', unsafe_allow_html=True)

    if save_button and user_input:
        if button_clicked:  # If the "Send" button was clicked, use the generated response
            save_tax_prompt_and_response(user_input, chatbot_response)
        else:  # Otherwise, generate a new response for the current user input
            chatbot_response = generate_chatbot_response(user_input)
            save_tax_prompt_and_response(user_input, chatbot_response)
        saved_message.markdown('<div class="saved-message">Prompt and response saved to SQL!</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
