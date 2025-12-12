
import os
import tempfile
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import speech_recognition as sr
from googletrans import Translator
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Voice Translator API",
    description="Translate audio files or text to different languages",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

translator = Translator()


@app.get("/")
async def root():
    return {
        "message": "Voice Translator API",
        "status": "running",
        "endpoints": {
            "GET /": "API information (this page)",
            "GET /health": "Health check",
            "GET /languages": "Get available languages",
            "POST /translate/voice": "Upload audio file for translation",
            "POST /translate/text": "Send text for translation"
        },
        "supported_audio_formats": ["wav", "mp3", "m4a", "webm", "ogg", "flac"]
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "voice-translator"}


@app.get("/languages")
async def get_languages():
    languages = [
        
        {"code": "en", "name": "English", "flag": "🇺🇸"},
        {"code": "es", "name": "Spanish", "flag": "🇪🇸"},
        {"code": "fr", "name": "French", "flag": "🇫🇷"},
        {"code": "de", "name": "German", "flag": "🇩🇪"},
        {"code": "it", "name": "Italian", "flag": "🇮🇹"},
        {"code": "pt", "name": "Portuguese", "flag": "🇵🇹"},
        {"code": "ru", "name": "Russian", "flag": "🇷🇺"},
        {"code": "ja", "name": "Japanese", "flag": "🇯🇵"},
        {"code": "ko", "name": "Korean", "flag": "🇰🇷"},
        {"code": "zh-cn", "name": "Chinese", "flag": "🇨🇳"},
        
       
        {"code": "hi", "name": "Hindi", "flag": "🇮🇳"},
        {"code": "ta", "name": "Tamil", "flag": "🇮🇳"},
        {"code": "te", "name": "Telugu", "flag": "🇮🇳"},
        {"code": "ml", "name": "Malayalam", "flag": "🇮🇳"},
        {"code": "bn", "name": "Bengali", "flag": "🇮🇳"},
        {"code": "mr", "name": "Marathi", "flag": "🇮🇳"},
        {"code": "gu", "name": "Gujarati", "flag": "🇮🇳"},
        {"code": "kn", "name": "Kannada", "flag": "🇮🇳"},
        {"code": "pa", "name": "Punjabi", "flag": "🇮🇳"},
        {"code": "or", "name": "Odia", "flag": "🇮🇳"},
        
       
        {"code": "ar", "name": "Arabic", "flag": "🇸🇦"},
        {"code": "tr", "name": "Turkish", "flag": "🇹🇷"},
        {"code": "nl", "name": "Dutch", "flag": "🇳🇱"},
        {"code": "pl", "name": "Polish", "flag": "🇵🇱"},
        {"code": "sv", "name": "Swedish", "flag": "🇸🇪"},
        {"code": "da", "name": "Danish", "flag": "🇩🇰"},
        {"code": "fi", "name": "Finnish", "flag": "🇫🇮"},
        {"code": "no", "name": "Norwegian", "flag": "🇳🇴"},
        {"code": "el", "name": "Greek", "flag": "🇬🇷"},
        {"code": "he", "name": "Hebrew", "flag": "🇮🇱"},
        {"code": "id", "name": "Indonesian", "flag": "🇮🇩"},
        {"code": "th", "name": "Thai", "flag": "🇹🇭"},
        {"code": "vi", "name": "Vietnamese", "flag": "🇻🇳"},
    ]
    return {"languages": languages}


@app.post("/translate/voice")
async def translate_voice(
    audio: UploadFile = File(..., description="Audio file to translate"),
    target_language: str = Form("en", description="Target language code (e.g., 'es' for Spanish)")
):
    logger.info(f"Processing audio file: {audio.filename}, target language: {target_language}")
    
    try:
        
        if not audio.content_type or not audio.content_type.startswith('audio/'):
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": f"File must be an audio file. Received type: {audio.content_type}"
                }
            )
        
        filename = audio.filename.lower()
        valid_extensions = ['.wav', '.mp3', '.m4a', '.webm', '.ogg', '.flac', '.aac', '.amr']
        
        file_extension = os.path.splitext(filename)[1]
        if file_extension not in valid_extensions:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": f"Unsupported file format: {file_extension}. Supported formats: {', '.join(valid_extensions)}"
                }
            )
       
        file_size = 0
        temp_file_path = None
        
        try:
           
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
                content = await audio.read()
                file_size = len(content)
                
                
                if file_size > 10 * 1024 * 1024:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "success": False,
                            "error": "File too large. Maximum size is 10MB"
                        }
                    )
                
                tmp.write(content)
                temp_file_path = tmp.name
           
            recognizer = sr.Recognizer()
            text = ""
            
            try:
              
                with sr.AudioFile(temp_file_path) as source:
                    
                    logger.info("Adjusting for ambient noise...")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                   
                    logger.info("Recording audio...")
                    audio_data = recognizer.record(source)
                    
                 
                    logger.info("Converting speech to text...")
                    text = recognizer.recognize_google(
                        audio_data, 
                        language='auto'  
                    )
                    
                    logger.info(f"Recognized text: {text}")
                    
            except sr.UnknownValueError:
                return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "error": "Speech recognition could not understand the audio. Please ensure the audio is clear and try again."
                    }
                )
            except sr.RequestError as e:
                return JSONResponse(
                    status_code=503,
                    content={
                        "success": False,
                        "error": f"Speech recognition service error: {str(e)}. Please check your internet connection."
                    }
                )
            except Exception as e:
                logger.error(f"Speech recognition error: {str(e)}")
                return JSONResponse(
                    status_code=500,
                    content={
                        "success": False,
                        "error": f"Error processing audio: {str(e)}"
                    }
                )
            
           
            try:
                logger.info(f"Translating text to {target_language}...")
                translation = translator.translate(text, dest=target_language)
                
               
                logger.info(f"Translation complete. Source: {translation.src}, Target: {target_language}")
                
                return {
                    "success": True,
                    "original_text": text,
                    "translated_text": translation.text,
                    "target_language": target_language,
                    "source_language": translation.src,
                    "pronunciation": translation.pronunciation if hasattr(translation, 'pronunciation') else None,
                    "file_info": {
                        "filename": audio.filename,
                        "content_type": audio.content_type,
                        "size": file_size,
                        "duration": "N/A"
                    }
                }
                
            except Exception as e:
                logger.error(f"Translation error: {str(e)}")
                return JSONResponse(
                    status_code=500,
                    content={
                        "success": False,
                        "error": f"Translation failed: {str(e)}"
                    }
                )
                
        finally:
           
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                    logger.info(f"Cleaned up temp file: {temp_file_path}")
                except Exception as e:
                    logger.warning(f"Failed to delete temp file: {str(e)}")
                    
    except Exception as e:
        logger.error(f"Unexpected error in translate_voice: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Internal server error: {str(e)}"
            }
        )


@app.post("/translate/text")
async def translate_text(
    text: str = Form(..., description="Text to translate"),
    target_language: str = Form("en", description="Target language code")
):
    logger.info(f"Translating text: '{text[:50]}...' to {target_language}")
    
    try:
      
        if not text or not text.strip():
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Text cannot be empty"
                }
            )
        
        if len(text.strip()) > 5000:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Text too long. Maximum 5000 characters"
                }
            )
        
      
        translation = translator.translate(text, dest=target_language)
        
        return {
            "success": True,
            "original_text": text,
            "translated_text": translation.text,
            "target_language": target_language,
            "source_language": translation.src,
            "pronunciation": translation.pronunciation if hasattr(translation, 'pronunciation') else None,
            "characters": len(text)
        }
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Translation failed: {str(e)}"
            }
        )


@app.post("/test/upload")
async def test_upload(audio: UploadFile = File(...)):
    """Test endpoint to check file upload functionality"""
    return {
        "filename": audio.filename,
        "content_type": audio.content_type,
        "size": len(await audio.read())
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )