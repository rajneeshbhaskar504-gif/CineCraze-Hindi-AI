import streamlit as st

st.set_page_config(page_title="Thumbnail Generator")

st.title("🖼️ AI Thumbnail Generator")

movie = st.text_input("🎬 Movie Name")

style = st.selectbox(
    "Thumbnail Style",
    [
        "Cinematic",
        "Action",
        "Horror",
        "Sci-Fi",
        "Dark",
        "YouTube Viral"
    ]
)

if st.button("Generate Thumbnail Prompt"):
    prompt = f"""
Create a {style} YouTube thumbnail for the movie "{movie}".
Ultra realistic, cinematic lighting,
dramatic background,
high quality,
4K,
bold Hindi title,
viral YouTube style.
"""
    st.code(prompt)
