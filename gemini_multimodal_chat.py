import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
import speech_recognition as sr
from textblob import TextBlob
import spacy

# Load the SpaCy model for natural language processing
nlp = spacy.load("en_core_web_sm")

# Set up the Streamlit app
st.set_page_config(page_title="Multimodal Chatbot with Gemini Flash", layout="wide")
st.title("Multimodal Chatbot with Gemini Flash ⚡")
st.caption("Chat with Google's Gemini Flash model using image, text, and voice input to get lightning fast results.⚡")

# Get OpenAI API key from user
api_key = st.text_input("Enter Google API Key", type="password")

# Set up the Gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

if api_key:
    # Initialize the chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar for image upload and voice input
    with st.sidebar:
        st.title("Chat with Images and Voice")
        uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)

        st.title("Voice Input")
        voice_input = st.button("Record Voice")
        if voice_input:
            with st.spinner("Recording..."):
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    audio = r.listen(source)
                try:
                    text = r.recognize_google(audio)
                    st.success(f"You said: {text}")
                    prompt = text
                except sr.UnknownValueError:
                    st.error("Could not understand audio")
                except sr.RequestError as e:
                    st.error(f"Error: {e}")

    chat_placeholder = st.container()

    # Display the chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input area at the bottom
    if not voice_input:
        prompt = st.chat_input("What do you want to know?")

    if prompt:
        inputs = [prompt]

        # Sentiment analysis
        blob = TextBlob(prompt)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            sentiment_label = "Positive"
        elif sentiment < 0:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"
        st.write(f"Sentiment: {sentiment_label}")

        # Natural language processing
        doc = nlp(prompt)
        entities = [ent.text for ent in doc.ents]
        st.write(f"Entities: {', '.join(entities)}")

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with chat_placeholder:
            with st.chat_message("user"):
                st.markdown(prompt)

        if uploaded_file:
            inputs.append(image)

        with st.spinner("Generating response..."):
            # Generate response
            response = model.generate_content(inputs)
            # Display assistant response in chat message container
            with chat_placeholder:
                with st.chat_message("assistant"):
                    st.markdown(response.text)

            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": response.text})

        if uploaded_file and not prompt:
            st.warning("Please enter a text query to accompany the image.")