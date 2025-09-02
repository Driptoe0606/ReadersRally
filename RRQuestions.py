
import streamlit as st
import pandas as pd
import re
import random
import time
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = 'AIzaSyDpNBBrdp32QWNWkv6XHRls0WaKORmmYCQ'
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

# Function to convert Google Sheets URL to CSV export link
def convert_to_csv_export_url(sheet_url):
    # Try to extract the sheet ID and gid even if URL is in different formats
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', sheet_url)
    gid_match = re.search(r'gid=(\d+)', sheet_url)

    if match:
        sheet_id = match.group(1)
        gid = gid_match.group(1) if gid_match else "0"  # Default to first sheet if no gid
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    else:
        raise ValueError("Invalid Google Sheets URL. Make sure it's a valid Google Sheet link.")


# Function to fetch questions from a Google Sheet
def fetch_questions(sheet_url):
    csv_url = convert_to_csv_export_url(sheet_url)
    try:
        df = pd.read_csv(csv_url)
        questions = df.iloc[:, :2].values.tolist()
        return questions
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return []

# Function to get Gertrude's status
def get_gertrude_status():
    try:
        prompt = ("Imagine I had a pet rock named Gertrude, who is pretty boring. "
                  "Tell me the current status of Gertrude in 1 sentence. Occasionally, "
                  "make it crazy or adventurous. Include interactions with people: Shadipto, Jessie, Charvi, Mrs. Tran, Nailah, Olivia, Andrew, Ronald, Archi, Jowayne, Bryce, Damola, Grace.")
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Unable to fetch Gertrude's status."

# Streamlit app
st.title("Quiz Game with Gertrude's Adventures")

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current" not in st.session_state:
    st.session_state.current = {"spreadsheet": "", "question": "", "answer": ""}

# Add Google Sheet
sheet_url = st.text_input("Enter Google Sheet URL")
spreadsheet_name = st.text_input("Enter Spreadsheet Name")
if st.button("Add Questions"):
    if sheet_url and spreadsheet_name:
        questions = fetch_questions(sheet_url)
        for q, a in questions:
            st.session_state.questions.append((spreadsheet_name, q, a))
        st.success(f"Added questions from {spreadsheet_name}!")

# Next Question
if st.button("Next Question"):
    if st.session_state.questions:
        spreadsheet, q, a = random.choice(st.session_state.questions)
        st.session_state.current = {"spreadsheet": spreadsheet, "question": q, "answer": a}
    else:
        st.warning("No questions available!")

# Display Current Question
if st.session_state.current["question"]:
    st.subheader(f"Spreadsheet: {st.session_state.current['spreadsheet']}")
    st.write(f"**Question:** {st.session_state.current['question']}")

# Show Answer
if st.button("Show Answer"):
    st.info(f"Answer: {st.session_state.current['answer']}")

# Gertrude's Status
if st.button("Check Gertrude's Status"):
    status = get_gertrude_status()
    st.success(status)
