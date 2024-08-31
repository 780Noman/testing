import tempfile
import re
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from utils import audio_bytes_to_wav, speech_to_text, text_to_speech, get_llm_response, create_welcome_message

def main():
    st.set_page_config(page_title='آڈیو پر مبنی چیٹ بوٹ')
    st.title("🎤 :blue[اردو ماہر نفسیات وائس چیٹ بوٹ] 💬🤖")
    st.sidebar.markdown("# Aibytec")
    st.sidebar.image('logo.jpg', width=20, use_column_width=True)

    # Initialize chat history if not already present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "chat_histories" not in st.session_state:
        st.session_state.chat_histories = []

    if "played_audios" not in st.session_state:
        st.session_state.played_audios = {}  # To track if an audio file has been played

    # Handle the initial chat history setup
    if len(st.session_state.chat_history) == 0:
        welcome_audio_path = create_welcome_message()
        st.session_state.chat_history = [
            AIMessage(content="السلام علیکم میں آپ کی چیٹ بوٹ اسسٹنٹ ہوں۔ میں آپ کی کس طرح مدد کر سکتی ہوں؟", audio_file=welcome_audio_path)  # Urdu greeting with female pronoun
        ]
        st.session_state.played_audios[welcome_audio_path] = False

    # Sidebar with mic button on top
    with st.sidebar:
        # Show "Speaking..." message during recording
        audio_bytes = audio_recorder(
            energy_threshold=0.01,
            pause_threshold=0.8,
            text="Speak now...max 5 min",
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_name="microphone",
            icon_size="2x"  # Adjust the icon size
        )
        st.info("")  # Clear the "Speaking..." message after recording

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
                st.session_state.played_audios[audio_response_file_path] = False  # Mark the new response as not played

        if st.button("New Chat"):
            # Save the current chat history to the chat_histories list
            st.session_state.chat_histories.append(st.session_state.chat_history)
            # Initialize a new chat history with the default welcome message
            welcome_audio_path = create_welcome_message()
            st.session_state.chat_history = [
                 AIMessage(content="السلام علیکم میں آپ کی چیٹ بوٹ اسسٹنٹ ہوں۔ میں آپ کی کس طرح مدد کر سکتی ہوں؟", audio_file=welcome_audio_path)  # Urdu greeting with female pronoun
            ]
            st.session_state.played_audios[welcome_audio_path] = False

        if st.session_state.chat_histories:
            st.subheader("Chat History")
            for i, hist in enumerate(st.session_state.chat_histories):
                if st.button(f"Chat {i + 1}", key=f"chat_{i}"):
                    st.session_state.chat_history = hist

    # Display the conversation history in the main area
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                # Check if the audio file has already been played
                if hasattr(message, 'audio_file'):
                    if not st.session_state.played_audios.get(message.audio_file, False):
                        st.audio(message.audio_file, format="audio/mp3", autoplay=True)
                        st.session_state.played_audios[message.audio_file] = True  # Mark as played
                    else:
                        st.audio(message.audio_file, format="audio/mp3", autoplay=False)
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                if hasattr(message, 'audio_file'):
                    st.audio(message.audio_file, format="audio/wav", autoplay=False)

if __name__ == "__main__":
    main()
