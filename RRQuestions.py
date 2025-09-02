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

rock_images = [
    "https://miro.medium.com/v2/resize:fit:1100/format:webp/1*vAyRxujFRIBk_P9WvIk_oQ.jpeg",
    "https://external-preview.redd.it/RWmE-Yf6koCDxnmEVNaa06RZqcRNUa6gj-aD2eggMkk.jpg?auto=webp&s=48281aaf067b8b979be5dccbc03edf86c21e18cb",
    "data:image/jpeg;base64,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",
    "https://i.etsystatic.com/18052430/r/il/1dd187/4699785550/il_fullxfull.4699785550_tkrb.jpg",
    "https://jclovely.com/cdn/shop/files/Stage_Rock_1b.png?v=1691085897",
    "https://www.shutterstock.com/shutterstock/photos/1544828072/display_1500/stock-photo-pet-rock-dressed-with-a-bowtie-as-a-person-1544828072.jpg",
    "https://www.reddit.com/media?url=https%3A%2F%2Fi.redd.it%2Fn3nsob8t0v9b1.jpg",
    "https://www.reddit.com/media?url=https%3A%2F%2Fexternal-preview.redd.it%2FRWmE-Yf6koCDxnmEVNaa06RZqcRNUa6gj-aD2eggMkk.jpg%3Fauto%3Dwebp%26s%3D48281aaf067b8b979be5dccbc03edf86c21e18cb"
]

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
        models = genai.list_models()
        # Pick a model that supports generateContent
        model_name = next(
            (m.name for m in models if "generateContent" in m.supported_generation_methods),
            None
        )
        if not model_name:
            return "No available models support generateContent."

        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        prompt = ("Imagine I had a pet rock named Gertrude, who is pretty boring. Tell me the current status of Gertrude in 1 sentence. Occasionally, make it crazy or adventurous. Include interactions with people: Shadipto, Jessie, Charvi, Mrs. Tran, Nailah, Olivia, Andrew, Ronald, Archi, Jowayne, Bryce, Damola, Grace")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error fetching Gertrude's status: {e}"

# Streamlit app
st.title("Readers Rally Practice Hub 📚📝 ")
st.subheader("Tutorial")
st.image("tutorial.gif.gif", use_container_width=True)

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
    loading_text = st.text("Loading Gertrude's status... ⏳")
    
    # Get status
    status = get_gertrude_status()
    
    # Update loading text to success
    loading_text.text("Done! ✅")
    st.success(status)

    # Display a random rock image with googly eyes
    rock_image = random.choice(rock_images)
    st.image(rock_image, caption="Gertrude's new friend", use_column_width=True)

