# Echo Mail - Voice-Based Email Sender with Secure Password Mapping

Echo Mail is a voice-controlled Python application that allows users to send emails securely using speech recognition and text-to-speech features. It also provides a basic character-to-number mapping system to encode and decode passwords for extra reference-level security.

## 🔧 Features

- 🎤 Voice-controlled email input: sender email, recipient email, subject, and body.
- 🔒 Secure password capture through spoken spelling.
- 🔁 Character-to-number password encoding and decoding.
- 📧 Email sending via Gmail SMTP.
- 🗣️ Real-time speech feedback with `pyttsx3`.

## 📦 Dependencies

Install the following Python libraries before running the app:

```bash
pip install SpeechRecognition pyttsx3 pyaudio
