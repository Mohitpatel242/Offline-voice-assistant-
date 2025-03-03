import re
import tkinter as tk
from tkinter import ttk, scrolledtext, font
import sounddevice as sd
import numpy as np
import whisper
import ollama
import threading


class EnhancedVoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Contanglimitation AI")
        self.root.geometry("1000x720")
        self.root.configure(bg='#2D2D2D')
        self.setup_styles()
        self.setup_audio()
        self.create_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Color palette
        self.colors = {
            'primary': '#3A3A3A',
            'secondary': '#4A4A4A',
            'accent': '#5B8C5A',
            'text': '#FFFFFF',
            'highlight': '#6DA66D'
        }

        # Configure styles
        self.style.configure('TFrame', background=self.colors['primary'])
        self.style.configure('TLabel', background=self.colors['primary'], foreground=self.colors['text'])
        self.style.configure('TButton',
                             background=self.colors['accent'],
                             foreground=self.colors['text'],
                             borderwidth=0,
                             font=('Helvetica', 10, 'bold'))
        self.style.map('TButton',
                       background=[('active', self.colors['highlight'])])

        self.style.configure('Header.TLabel',
                             font=('Helvetica', 16, 'bold'),
                             foreground=self.colors['accent'])

        self.style.configure('Status.TLabel',
                             font=('Helvetica', 10),
                             foreground='#AAAAAA')

    def setup_audio(self):
        self.samplerate = 16000
        self.channels = 1
        self.is_recording = False
        self.audio_data = []
        self.whisper_model = whisper.load_model("base.en")

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(header_frame,
                  text="Contanglimitation AI Assistant",
                  style='Header.TLabel').pack(side=tk.LEFT)

        # Recording Section
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        self.record_btn = ttk.Button(
            control_frame,
            text="🎤 Start Recording",
            command=self.toggle_recording,
            style='TButton'
        )
        self.record_btn.pack(side=tk.LEFT, padx=5)

        self.regenerate_btn = ttk.Button(
            control_frame,
            text="🔄 Regenerate Answer",
            command=self.regenerate_answer,
            style='TButton'
        )
        self.regenerate_btn.pack(side=tk.LEFT, padx=5)

        # Conversation Panel
        conv_frame = ttk.Frame(main_frame)
        conv_frame.pack(fill=tk.BOTH, expand=True)

        # Question Panel
        question_frame = ttk.LabelFrame(conv_frame, text="Your Question")
        question_frame.pack(fill=tk.X, pady=5)

        self.question_text = scrolledtext.ScrolledText(
            question_frame,
            height=4,
            wrap=tk.WORD,
            bg=self.colors['secondary'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            font=('Helvetica', 11)
        )
        self.question_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Answer Panel
        answer_frame = ttk.LabelFrame(conv_frame, text="AI Response")
        answer_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.answer_text = scrolledtext.ScrolledText(
            answer_frame,
            height=10,
            wrap=tk.WORD,
            bg=self.colors['secondary'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            font=('Helvetica', 11)
        )
        self.answer_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Status Bar
        self.status_bar = ttk.Label(
            main_frame,
            text="Ready",
            style='Status.TLabel'
        )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
            self.update_status("Recording...")
            self.record_btn.config(text="⏹ Stop Recording")
        else:
            self.stop_recording()
            self.update_status("Processing...")
            self.record_btn.config(text="🎤 Start Recording")

    def start_recording(self):
        self.is_recording = True
        self.audio_data = []
        self.recording_thread = threading.Thread(
            target=self.record_audio,
            daemon=True
        )
        self.recording_thread.start()

    def stop_recording(self):
        self.is_recording = False
        audio_array = np.concatenate(self.audio_data, axis=0)
        transcript = self.transcribe_audio(audio_array)
        self.question_text.insert(tk.END, transcript + "\n")
        self.get_answer(transcript)

    def record_audio(self):
        with sd.InputStream(
                samplerate=self.samplerate,
                channels=self.channels,
                callback=self.audio_callback
        ):
            while self.is_recording:
                sd.sleep(100)

    def audio_callback(self, indata, frames, time, status):
        self.audio_data.append(indata.copy())

    def transcribe_audio(self, audio):
        audio = audio.flatten().astype(np.float32)
        result = self.whisper_model.transcribe(audio, fp16=False)
        return result["text"].strip()

    def regenerate_answer(self):
        last_question = self.question_text.get("end-2l linestart", "end-1c")
        if last_question.strip():
            self.get_answer(last_question.strip())

    def get_answer(self, prompt):
        try:
            self.answer_text.insert(tk.END, "Thinking...\n")
            self.root.update_idletasks()

            response = ollama.generate(
                model='deepseek-r1:1.5b',
                prompt=prompt
            ).response

            clean_response = re.sub(
                r'(<think>.*?</think>|\\[\(\)\[\]{}]|[\*\`]|context=.*?|\w+=[\'\\dTZ:\.-]+)',
                '',
                response,
                flags=re.DOTALL
            ).strip()

            self.answer_text.delete('end-2l', tk.END)
            self.answer_text.insert(tk.END, f"{clean_response}\n\n")
            self.update_status("Ready")

        except Exception as e:
            self.answer_text.insert(tk.END, f"Error: {str(e)}\n")
            self.update_status("Error occurred")

    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedVoiceAssistant(root)
    root.mainloop()