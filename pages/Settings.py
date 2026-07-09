import streamlit as st

st.set_page_config(page_title="Settings", page_icon="⚙️")

st.title("⚙️ CineCraze Hindi AI Settings")

st.write("अपनी AI सेटिंग्स यहाँ मैनेज करें।")

api_key = st.text_input("Gemini API Key", type="password")

language = st.selectbox(
    "Script Language",
    ["Hindi", "English"]
)

style = st.selectbox(
    "Script Style",
    [
        "Movie Explained",
        "Storytelling",
        "Emotional",
        "Funny",
        "Suspense"
    ]
)

length = st.slider(
    "Script Length (Minutes)",
    5,
    30,
    10
)

if st.button("Save Settings"):
    st.success("Settings Saved Successfully ✅")
