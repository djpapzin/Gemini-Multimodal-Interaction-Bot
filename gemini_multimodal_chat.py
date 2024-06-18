import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Set up the Streamlit app
st.set_page_config(page_title="Multimodal Chatbot with Gemini Flash", layout="wide")
st.title("Multimodal Chatbot with Gemini Flash ⚡")
st.caption("Chat with Google's Gemini Flash model using image and text input to get lightning-fast results.⚡")

# Get Google API key from user
api_key = st.text_input("Enter Google API Key", type="password")

# Set up the Gemini model
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
    
    # Initialize the chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar for image upload and analysis
    with st.sidebar:
        st.title("Chat with Images")
        uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            
            with st.spinner("Generating image summary..."):
                # Generate image summary using the Gemini model
                image_summary = model.generate_content([image]).text
                st.write(image_summary)
                st.session_state.image_summary = image_summary

                # Generate suggested questions
                suggested_questions = model.generate_content(
                    [f"Generate three one-sentence questions about the following image: {image_summary}"]
                ).text.split('\n')

                st.session_state.suggested_questions = suggested_questions
    
    chat_placeholder = st.container()
    
    # Display the chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Show suggested questions if image is uploaded
    if "suggested_questions" in st.session_state:
        st.write("Here are three one-sentence questions about the image:")
        for question in st.session_state.suggested_questions:
            if question.strip():
                st.write(f"➡ {question.strip()}")
    
    # User input area at the bottom
    prompt = st.chat_input("What do you want to know?")
    if prompt or uploaded_file:
        inputs = []
        if prompt:
            inputs.append(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
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
else:
    st.warning("Please enter your Google API key to use the app.")
