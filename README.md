# Offline AI Assistant 🤖  
**Privacy-First Offline Voice Assistant**  

**G-drive link for images of Robot**
https://drive.google.com/drive/folders/1mtayP0xOgwxrxPYqi9GHUKjvEISW_vXs?usp=sharing

## 🚀 Features  
- **100% Offline** - No internet required, no data leaves your device  
- **Secure & Private** - Built for sensitive environments (healthcare, finance, etc.)  
- **Accurate Transcription** - OpenAI's Whisper (base.en) for speech-to-text  
- **Smart Responses** - Ollama's Deepseek-R1 1.5B local LLM  
- **Modern GUI** - Tkinter interface with dark theme and real-time logging  

---

## ⚙️ Installation  

### Requirements  
- Python 3.9+  
- [Ollama](https://ollama.ai/) installed locally  
- FFmpeg (for Whisper)  


# Clone repo
git clone https://github.com/yourusername/contanglimitation-ai.git
cd contanglimitation-ai

# Install Python dependencies
pip install -r requirements.txt

# Download Whisper model (base.en)
python -c "import whisper; whisper.load_model('base.en')"

# Download Ollama model
ollama pull deepseek-r1:1.5b
