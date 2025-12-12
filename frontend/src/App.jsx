// frontend/src/App.jsx
import React, { useState, useRef } from 'react'; // ADD useRef here
import VoiceRecorder from './components/VoiceRecorder';
import './App.css';

function App() {
  const [translation, setTranslation] = useState('');
  const [originalText, setOriginalText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [targetLang, setTargetLang] = useState('en');
  const fileInputRef = useRef(null); 
  
  const API_URL = 'http://127.0.0.1:8000';
  
  const handleVoiceTranslate = async (audioBlob) => {
    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.webm');
      formData.append('target_language', targetLang);
      
      const response = await fetch(`${API_URL}/translate/voice`, {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      
      if (data.success) {
        setOriginalText(data.original_text);
        setTranslation(data.translated_text);
      } else {
        setError(data.error || 'Translation failed');
      }
    } catch (err) {
      setError('Connection error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };
  
  const handleTextTranslate = async () => {
    const text = prompt('Enter text to translate:');
    if (!text) return;
    
    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('text', text);
      formData.append('target_language', targetLang);
      
      const response = await fetch(`${API_URL}/translate/text`, {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      
      if (data.success) {
        setOriginalText(data.original_text);
        setTranslation(data.translated_text);
      } else {
        setError(data.error || 'Translation failed');
      }
    } catch (err) {
      setError('Connection error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };
  
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    
    // Check if it's an audio file
    if (!file.type.startsWith('audio/')) {
      setError('Please select an audio file (MP3, WAV, etc.)');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('audio', file);
      formData.append('target_language', targetLang);
      
      const response = await fetch(`${API_URL}/translate/voice`, {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      
      if (data.success) {
        setOriginalText(data.original_text);
        setTranslation(data.translated_text);
      } else {
        setError(data.error || 'Translation failed');
      }
    } catch (err) {
      setError('Connection error: ' + err.message);
    } finally {
      setLoading(false);
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };
  
  return (
    <div className="app">
      <header>
        <h1>🎤 Voice Translator</h1>
        <p>Speak any language, get instant translation</p>
      </header>
      
      <main>
        <div className="controls">
          
// In your App.jsx, update the language selector options:
<div className="language-select">
  <label htmlFor="language-select">Translate to: </label>
  <select 
    id="language-select"
    value={targetLang} 
    onChange={(e) => setTargetLang(e.target.value)}
  >
    <option value="en">English 🇺🇸</option>
    <option value="es">Spanish 🇪🇸</option>
    <option value="fr">French 🇫🇷</option>
    <option value="de">German 🇩🇪</option>
    <option value="it">Italian 🇮🇹</option>
    <option value="pt">Portuguese 🇵🇹</option>
    <option value="ru">Russian 🇷🇺</option>
    <option value="ja">Japanese 🇯🇵</option>
    <option value="ko">Korean 🇰🇷</option>
    <option value="zh-cn">Chinese 🇨🇳</option>
    
    {/* Indian Languages - NEW */}
    <option value="hi">Hindi 🇮🇳</option>
    <option value="ta">Tamil 🇮🇳</option>
    <option value="te">Telugu 🇮🇳</option>
    <option value="ml">Malayalam 🇮🇳</option>
    <option value="bn">Bengali 🇮🇳</option>
    <option value="mr">Marathi 🇮🇳</option>
    <option value="gu">Gujarati 🇮🇳</option>
    <option value="kn">Kannada 🇮🇳</option>
    <option value="pa">Punjabi 🇮🇳</option>
    <option value="or">Odia 🇮🇳</option>
    
    <option value="ar">Arabic 🇸🇦</option>
    <option value="tr">Turkish 🇹🇷</option>
    <option value="nl">Dutch 🇳🇱</option>
    <option value="pl">Polish 🇵🇱</option>
    <option value="sv">Swedish 🇸🇪</option>
  </select>
</div>
          <div className="input-section">
            <div className="voice-input">
              <h3>🎤 Record Voice</h3>
              <VoiceRecorder onRecordingComplete={handleVoiceTranslate} />
            </div>
            
            {/* File Upload Section */}
            <div className="file-input">
              <h3>📁 Upload Audio File</h3>
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileUpload}
                accept="audio/*"
                style={{ display: 'none' }}
              />
              <button onClick={triggerFileInput} disabled={loading}>
                📂 Choose Audio File
              </button>
              <p className="hint">MP3, WAV, M4A, WEBM supported</p>
              
              {fileInputRef.current?.files[0] && (
                <div className="file-info">
                  <p>Selected: {fileInputRef.current.files[0].name}</p>
                  <audio 
                    src={URL.createObjectURL(fileInputRef.current.files[0])} 
                    controls 
                    style={{ width: '100%', marginTop: '10px' }}
                  />
                </div>
              )}
            </div>
            
            <div className="text-input">
              <h3>📝 Type Text</h3>
              <button onClick={handleTextTranslate} disabled={loading}>
                {loading ? 'Translating...' : 'Translate Text'}
              </button>
              <p className="hint">Click to enter text for translation</p>
            </div>
          </div>
        </div>
        
        <div className="results">
          {loading && <div className="loader">Translating...</div>}
          
          {error && <div className="error">{error}</div>}
          
          {originalText && !loading && (
            <>
              <div className="original">
                <h4>Original:</h4>
                <p>{originalText}</p>
              </div>
              
              <div className="translated">
                <h4>Translation ({getLanguageName(targetLang)}):</h4>
                <p>{translation}</p>
              </div>
            </>
          )}
          
          {!originalText && !loading && !error && (
            <p className="placeholder">
              Record your voice, upload a file, or enter text above to see translations here
            </p>
          )}
        </div>
      </main>
      
      <footer>
        <p>Backend: Python FastAPI | Frontend: React</p>
        <p>Three ways to translate: Record, Upload, or Type!</p>
      </footer>
    </div>
  );
}

// Helper function to get language name from code
function getLanguageName(code) {
  const languages = {
       'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh-cn': 'Chinese',
    
    // Indian Languages
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'ml': 'Malayalam',
    'bn': 'Bengali',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'pa': 'Punjabi',
    'or': 'Odia',
    
    'ar': 'Arabic',
    'tr': 'Turkish',
    'nl': 'Dutch',
    'pl': 'Polish',
    'sv': 'Swedish'
  };
  return languages[code] || code;
}

export default App;