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

# Load the API key from Streamlit secrets
api_key = st.secrets['secrets']["API_KEY"]

# Initialize the Groq client
client = Groq(api_key=api_key)

# Initialize the Groq model for LLM responses
llm = ChatGroq(model="llama-3.1-70b-versatile", api_key=api_key, max_tokens=500)  # Limit tokens to 100

def audio_bytes_to_wav(audio_bytes):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            with open(temp_wav.name, "wb") as f:
                f.write(audio_bytes)
            return temp_wav.name
    except Exception as e:
        st.error(f"Error during WAV file conversion: {e}")
        return None

def speech_to_text(audio_bytes):
    try:
        temp_wav_path = audio_bytes_to_wav(audio_bytes)
        
        if temp_wav_path is None:
            return "Error"
        
        # Use Groq's Whisper API for transcription
        with open(temp_wav_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(temp_wav_path, file.read()),
                model="whisper-large-v3",
                response_format="text",  # Other options: "json", "verbose_json"
                language="ur",  # Set language to Urdu
                temperature=0.0  # Optional, controls the variability of the output
            )
    except Exception as e:
        st.error(f"Error during speech-to-text conversion: {e}")
        transcription = "Error"
    # Do not clean up the temp file
    
    return transcription

def text_to_speech(text):
    try:
        # Use gTTS to convert text to speech in Urdu
        tts = gTTS(text=text, lang='ur')  # Set language to Urdu
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            tts.save(f.name)
            audio = AudioSegment.from_mp3(f.name)
    except Exception as e:
        st.error(f"Error during text-to-speech conversion: {e}")
        audio = AudioSegment.silent(duration=1000)  # Return silent audio in case of error
    # Do not clean up the temp file
    
    return audio

def remove_punctuation(text):
    # Remove punctuation from the text
    return re.sub(r'[^\w\s]', '', text)

def get_llm_response(query, chat_history):
    try:
        # Updated template with detailed guidelines
        template = """
                You are a highly qualified female psychiatrist with extensive experience in Pakistani mental health, specializing in Pakistan. Provide professional, empathetic, and culturally authentic advice and answers to the user's questions. Use everyday language, incorporating local idioms and expressions. Avoid using loanwords from other languages. **Keep your response within [token_limit] tokens.**

                    **Key Considerations:**
                    * **Professionalism:** Maintain a high level of expertise and ethical standards.
                    * **Cultural Authenticity:** Deeply understand and reflect the values, beliefs, and customs of Pakistan.
                    * **Empathy:** Show genuine compassion and support for the user's emotional well-being.

                    **Chat History:** {chat_history}

                    **User:** {user_query}

        """

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm | StrOutputParser()

        response_gen = chain.stream({
            "chat_history": chat_history,
            "user_query": query
        })

        # Combine all parts of the response and apply text clean-up
        response_text = ''.join(list(response_gen))
        response_text = remove_punctuation(response_text)

        # Remove repeated text
        response_lines = response_text.split('\n')
        unique_lines = list(dict.fromkeys(response_lines))  # Remove duplicates while preserving order
        cleaned_response = '\n'.join(unique_lines)

        return cleaned_response
    except Exception as e:
        st.error(f"Error during LLM response generation: {e}")
        return "Error"

def create_welcome_message():
    welcome_text = "ہیلو، میں آپ کی چیٹ بوٹ اسسٹنٹ ہوں۔ میں آپ کی کس طرح مدد کر سکتی ہوں؟"  # Urdu greeting with female pronoun
    tts = gTTS(text=welcome_text, lang='ur')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
        tts.save(f.name)
        return f.name
