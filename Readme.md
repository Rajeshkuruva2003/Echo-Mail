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

How It Works
The user speaks their email address.

The system prompts the user to spell their password one character at a time.

The password is encoded and decoded for reference.

The user speaks the recipient’s email, subject, and body.

The email is sent securely using SMTP over SSL.

📢 Usage
bash
Copy
Edit
python echo_mail.py
Follow the voice instructions to:

Enter your email

Spell your password

Enter recipient email

Dictate subject and body

Send the email

🛡️ Disclaimer
This is a demonstration project. Do not use with sensitive email accounts.

Password encoding here is not encryption. It's for voice-to-character clarity only.