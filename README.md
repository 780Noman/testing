
# Urdu اردو ماہر نفسیات Voice Chatbot - Streamlit

Welcome to the Urdu اردو ماہر نفسیات Voice Chatbot project! collabration with [ aibytech ](https://www.aibytech.com/) This repository showcases a Streamlit application that allows users to interact with a chatbot using Urdu voice input and receive responses in Urdu.
The Urdu Voice Chatbot is designed to The Urdu Voice Chatbot is designed to provide a voice-interactive, AI-powered conversational assistant specializing in mental health advice. The chatbot can transcribe spoken Urdu into text, generate appropriate AI responses in Urdu, and convert the generated text back into speech for a seamless voice-based interaction.:
## 🚀 **Models Used Groq LLM:**

## llama-3.1-70b-versatile
Purpose: The LLM (Large Language Model) is responsible for generating AI responses based on user queries. It is fine-tuned for conversational tasks, with a focus on providing mental health advice in Urdu.
## Whisper:

Purpose: Whisper is used for converting spoken Urdu into text with high accuracy. It handles the transcription of user audio inputs into text, even for long and complex sentences.
## 🛠️ **Technologies Used**

- **Streamlit**: Used for creating the interactive web interface.
- **gTTS (Google Text-to-Speech)**: Converts text into speech in Urdu.
- **Pydub**: Handles audio processing tasks, including splitting and format conversion.
- **Whisper**: Transcribes Urdu speech to text, especially effective with complex audio inputs.
- **Groq API**: Provides LLM and Whisper model functionalities for natural language understanding and transcription.
- **Langchain**: Facilitates integration of language models and manages chat prompts, output parsing, and message handling.
- **audio_recorder_streamlit**: Enables recording of user audio input directly within the Streamlit interface.


## 📦 **Project Structure**

```
└── 📁Urdu_voice_chatbot
    └── 📁.streamlit
        └── secrets.toml            # API keys and other sensitive information
    └── .gitignore                  # Git ignore file
    └── app.py                      # Main Streamlit application file
    └── logo.jpg                    # Logo used in the application
    └── packages.txt                # List of system packages required
    └── requirements.txt            # List of Python dependencies
    └── utils.py                    # Utility functions for speech processing and LLM interaction

```
## 📦 **Installation & Usage**

1. **Clone the Repository**
    ```bash
    git clone https://github.com/Rizwanali324/Urdu_voice_chatbot.git
    cd Urdu_voice_chatbot
    ```

2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Secrets**
    Create a `.streamlit/secrets.toml` file and add your API keys:
    ```toml
    [secrets]
    api_key = "YOUR_API_KEY_HERE"
    ```

5. **Run the App**
    ```bash
    streamlit run app.py
    ```

## 📈 **Deployment**

This application is also deployed on Streamlit Cloud. You can access the live app here: [ App ](https://urdu-chatbot.streamlit.app/)

## 🔍 **Contributing**

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

Conclusion:
This Urdu Voice Chatbot leverages advanced language models and speech processing tools like Whisper and the Groq LLM to create an interactive, culturally relevant, and empathetic conversational assistant. The project demonstrates the integration of LLMs with state-of-the-art speech recognition and synthesis technologies to build a specialized chatbot for mental health assistance.
