import streamlit as st

st.set_page_config(
    page_title="AI Script Generator",
    page_icon="🤖"
)

st.title("🤖 AI Movie Script Generator")

movie_name = st.text_input("🎬 Enter Movie Name")

language = st.selectbox(
    "Language",
    ["Hindi", "English"]
)

style = st.selectbox(
    "Style",
    [
        "Movie Explained",
        "Emotional",
        "Suspense",
        "Funny"
    ]
)

duration = st.slider(
    "Video Duration (Minutes)",
    5,
    20,
    10
)

if st.button("Generate Script"):

    if movie_name == "":
        st.warning("Please Enter Movie Name")
    else:

        script = f"""
Movie : {movie_name}

Language : {language}

Style : {style}

Duration : {duration} Minutes

⚠️ AI Script Generator अभी API से Connect नहीं हुआ है।

जल्द ही यहाँ AI द्वारा बनाई गई Script दिखाई देगी।
"""

        st.text_area(
            "Generated Script",
            script,
            height=350
        )

        st.download_button(
            "📥 Download Script",
            script,
            file_name=f"{movie_name}.txt"
        )
