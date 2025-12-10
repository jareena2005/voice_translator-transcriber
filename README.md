 Voice Translator & Transcriber:
A powerful web application that converts speech to text and translates it across multiple languages with three input methods: voice recording, file upload, and direct text input.
---------------
 Features:
 Three Input Methods:
*Voice Recording - Start/Stop recording with real-time transcription

*File Upload - Supports WAV, MP3, and other audio formats

*Text Input - Direct text entry for instant translation
-------------------------
Language Support:
Indian Languages: Hindi, Bengali, Telugu, Marathi, Tamil, Gujarati, Kannada, Malayalam, Punjabi

Global Languages: English, Spanish, French, German, Chinese, Japanese, Arabic, Russian, Portuguese, Italian

*Regional Languages: Multiple Indian dialects and accents
-----------------------
Output Display:
*Original Transcription - Raw converted text from speech
*Translated Text - Translated version in target language
*Side-by-Side Comparison - View both original and translated text
*Audio Playback - Listen to original recording
----------------
Tech Stack:
Frontend :
*React.js with Vite
*Tailwind CSS / Material-UI
*Web Audio API for recording
*File handling with React Dropzone

Backend:
*Python FastAPI / Flask
*Speech Recognition (Google Speech-to-Text, Whisper, Vosk)
*Translation APIs (Google Translate, LibreTranslate)
*Audio processing with librosa, pydub
