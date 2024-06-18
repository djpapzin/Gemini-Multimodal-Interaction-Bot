# Gemini Multimodal Chatbot

This project is a Streamlit web application that uses Google's Gemini Flash model to create a multimodal chatbot. Users can input text and upload images, and the chatbot generates responses based on the provided inputs.

## Features

- Accepts text input from the user
- Allows users to upload images
- Generates responses using the Gemini Flash model
- Maintains chat history within the session

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/gemini_multimodal_chatbot.git
    cd gemini_multimodal_chatbot
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:
    ```bash
    streamlit run gemini_multimodal_chatbot.py
    ```

2. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Enter your Google API key, input text, and/or upload images to interact with the chatbot.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

