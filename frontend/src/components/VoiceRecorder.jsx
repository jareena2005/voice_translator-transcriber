// frontend/src/components/VoiceRecorder.jsx
import React, { useState, useRef } from 'react';

const VoiceRecorder = ({ onRecordingComplete }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState('');
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const url = URL.createObjectURL(audioBlob);
        setAudioURL(url);
        onRecordingComplete(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      alert('Please allow microphone access');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  return (
    <div className="voice-recorder">
      <div className="buttons">
        <button 
          onClick={startRecording} 
          disabled={isRecording}
          className={isRecording ? 'recording' : ''}
        >
          {isRecording ? '● Recording...' : '🎤 Start'}
        </button>
        
        <button 
          onClick={stopRecording} 
          disabled={!isRecording}
        >
          ⏹️ Stop
        </button>
      </div>
      
      {audioURL && (
        <div className="preview">
          <audio src={audioURL} controls />
        </div>
      )}
      
      <p className="hint">
        {isRecording ? 'Speak now...' : 'Click Start to record your voice'}
      </p>
    </div>
  );
};

export default VoiceRecorder;