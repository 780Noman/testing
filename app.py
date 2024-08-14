import streamlit as st
from audio_recorder_streamlit import audio_recorder
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
import tempfile
import os
import re

from utils import *

# Load the API key from Streamlit secrets
api_key = st.secrets['secrets']["API_KEY"]

# Initialize the Groq client
client = Groq(api_key=api_key)

# Initialize the Groq model for LLM responses
llm = ChatGroq(model="llama-3.1-70b-versatile", api_key=api_key, max_tokens=500)  # Limit tokens to 100

def main():
    st.set_page_config(page_title='Audio-based Multimodal Chatbot')
    st.title("🎤 :blue[Urdu Voice Chatbot] 💬🤖")

    # Initialize chat history if not already present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "chat_histories" not in st.session_state:
        st.session_state.chat_histories = []

    # Handle the initial chat history setup
    if len(st.session_state.chat_history) == 0:
        welcome_audio_path = create_welcome_message()
        st.session_state.chat_history = [
            AIMessage(content='ہیلو، میں آپ کی چیٹ بوٹ اسسٹنٹ ہوں۔ میں آپ کی کس طرح مدد کر سکتی ہوں؟', audio_file=welcome_audio_path)  # Urdu greeting with female pronoun
        ]

    # Sidebar with mic button on top
    with st.sidebar:
        audio_bytes = audio_recorder(
            text="Record your voice message",
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_name="microphone",
            icon_size="2x"  # Adjust the icon size
        )
        
        if audio_bytes:
            # Save the user input audio file
            temp_audio_path = audio_bytes_to_wav(audio_bytes)
            if temp_audio_path:
                # Transcribe the audio and update chat history
                user_input = speech_to_text(audio_bytes)
                st.session_state.chat_history.append(HumanMessage(content=user_input, audio_file=temp_audio_path))
                
                # Generate AI response
                response = get_llm_response(user_input, st.session_state.chat_history)
                
                # Convert the response to audio
                audio_response = text_to_speech(response)

                # Create an in-memory BytesIO stream
                audio_stream = BytesIO()
                audio_response.export(audio_stream, format="mp3")
                audio_stream.seek(0)  # Rewind the stream to the beginning

                # Save the AI response audio file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_response:
                    audio_stream.seek(0)
                    temp_audio_response.write(audio_stream.read())
                    audio_response_file_path = temp_audio_response.name

                # Append AI response text and audio to history
                st.session_state.chat_history.append(AIMessage(content=response, audio_file=audio_response_file_path))
        
        if st.button("New Chat"):
            # Save the current chat history to the chat_histories list
            st.session_state.chat_histories.append(st.session_state.chat_history)
            # Initialize a new chat history with the default welcome message
            welcome_audio_path = create_welcome_message()
            st.session_state.chat_history = [
                AIMessage(content='ہیلو، میں آپ کی چیٹ بوٹ اسسٹنٹ ہوں۔ میں آپ کی کس طرح مدد کر سکتی ہوں؟', audio_file=welcome_audio_path)  # Urdu greeting with female pronoun
            ]
    
        if st.session_state.chat_histories:
            st.subheader("Chat History")
            for i, hist in enumerate(st.session_state.chat_histories):
                if st.button(f"Chat {i + 1}", key=f"chat_{i}"):
                    st.session_state.chat_history = hist
    
    # Display the conversation history in the main area
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
                if hasattr(message, 'audio_file'):
                    st.audio(message.audio_file, format="audio/mp3", autoplay=False)  # Do not autoplay the audio response
        elif isinstance(message, HumanMessage):
            with st.chat_message('Human'):
                st.write(message.content)
                if hasattr(message, 'audio_file'):
                    st.audio(message.audio_file, format="audio/wav")

if __name__ == "__main__":
    main()
