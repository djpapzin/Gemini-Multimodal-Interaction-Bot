import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variables if running locally
if os.path.exists('.env'):
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
else:
    api_key = st.secrets.get("GOOGLE_API_KEY")

# Set up the Streamlit app
st.set_page_config(page_title="Multimodal Chatbot with Gemini Flash", layout="wide")
st.title("Multimodal Chatbot with Gemini Flash ⚡")
st.caption("Chat with Google's Gemini Flash model using image and text input to get lightning-fast results.⚡")

# Get Google API key from environment variable or user input
if not api_key:
    api_key = st.text_input("Enter Google API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
        st.success("Gemini model configured successfully")
    except Exception as e:
        st.error(f"Failed to configure Gemini model: {e}")
        st.stop()

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

            if "image_summary" not in st.session_state:
                with st.spinner("Generating image summary..."):
                    try:
                        # Generate image summary using the Gemini model
                        image_summary = model.generate_content([image]).text
                        st.session_state.image_summary = image_summary
                        st.write(f"**{image_summary}**")

                        # Generate suggested questions
                        suggested_questions = model.generate_content(
                            [f"Generate three one-sentence questions about the following image: {image_summary}"]
                        ).text.split('\n')

                        st.session_state.suggested_questions = suggested_questions
                    except Exception as e:
                        st.error(f"Failed to generate image summary or suggested questions: {e}")
                        st.stop()
            else:
                st.write(f"**{st.session_state.image_summary}**")

    chat_placeholder = st.container()

    # Display the chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Function to update suggested questions based on previous interaction
    def update_suggested_questions(previous_question):
        try:
            new_suggestions = model.generate_content(
                [f"Based on the previous question '{previous_question}', generate three similar one-sentence questions."]
            ).text.split('\n')
            st.session_state.suggested_questions = new_suggestions
        except Exception as e:
            st.error(f"Failed to update suggested questions: {e}")

    # Show suggested questions if image is uploaded
    if uploaded_file and "suggested_questions" in st.session_state:
        st.title("Suggested Questions")
        for question in st.session_state.suggested_questions:
            if question.strip():
                if st.button(f"➡ {question.strip()}", key=question.strip()):
                    st.session_state.prompt = question.strip()
                    update_suggested_questions(question.strip())

    # User input area at the bottom
    if 'prompt' in st.session_state:
        prompt = st.session_state.prompt
    else:
        prompt = st.chat_input("What do you want to know?")

    if prompt:
        inputs = [prompt]
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_placeholder:
            with st.chat_message("user"):
                st.markdown(prompt)

        if uploaded_file:
            inputs.append(image)

        with st.spinner("Generating response..."):
            try:
                # Generate response
                response = model.generate_content(inputs)
                response_text = response.text.split('\n', 1)[-1].strip()  # Remove any numbering
                # Display assistant response in chat message container
                with chat_placeholder:
                    with st.chat_message("assistant"):
                        st.markdown(response_text)

                # Add assistant message to chat history
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                st.session_state.prompt = None
            except Exception as e:
                st.error(f"Failed to generate response: {e}")

        if uploaded_file and not prompt:
            st.warning("Please enter a text query to accompany the image.")
else:
    st.warning("Please enter your Google API key to use the app.")
    print("API key not entered")
