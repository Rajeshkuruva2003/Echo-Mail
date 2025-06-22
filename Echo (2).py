import speech_recognition as sr
import smtplib
import pyttsx3
import pyaudio
from email.message import EmailMessage

engine = pyttsx3.init()

# Character-to-number secure mapping
char_to_num = {
    'A': '01', 'B': '02', 'C': '03', 'D': '04', 'E': '05',
    'F': '06', 'G': '07', 'H': '08', 'I': '09', 'J': '10',
    'K': '11', 'L': '12', 'M': '13', 'N': '14', 'O': '15',
    'P': '16', 'Q': '17', 'R': '18', 'S': '19', 'T': '20',
    'U': '21', 'V': '22', 'W': '23', 'X': '24', 'Y': '25',
    'Z': '26',
    'a': '27', 'b': '28', 'c': '29', 'd': '30', 'e': '31',
    'f': '32', 'g': '33', 'h': '34', 'i': '35', 'j': '36',
    'k': '37', 'l': '38', 'm': '39', 'n': '40', 'o': '41',
    'p': '42', 'q': '43', 'r': '44', 's': '45', 't': '46',
    'u': '47', 'v': '48', 'w': '49', 'x': '50', 'y': '51',
    'z': '52',
    '0': '60', '1': '61', '2': '62', '3': '63', '4': '64',
    '5': '65', '6': '66', '7': '67', '8': '68', '9': '69',
    '@': '70', '#': '71', '$': '72', '%': '73', '&': '74',
    '*': '75', '-': '76', '_': '77', '.': '78'
}

def password_to_code(password):
    code = ''
    for char in password:
        num = char_to_num.get(char)
        if num:
            code += num
        else:
            print(f"Character '{char}' not in map, skipped.")
    return code

def code_to_password(code):
    num_to_char = {v: k for k, v in char_to_num.items()}
    chars = [code[i:i+2] for i in range(0, len(code), 2)]
    return ''.join([num_to_char.get(c, '?') for c in chars])

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def get_audio_input(prompt):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak(prompt)
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            text = recognizer.recognize_google(audio).lower()
            print("You said:", text)
            return text
        except sr.WaitTimeoutError:
            speak("You didn’t say anything. Please try again.")
            return get_audio_input(prompt)
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please repeat.")
            return get_audio_input(prompt)
        except sr.RequestError:
            speak("Network error.")
            return None

def convert_spoken_email(spoken_email):
    email = spoken_email.replace(" at ", "@").replace(" dot ", ".")
    email = email.replace(" underscore ", "_").replace(" dash ", "-")
    email = email.replace(" ", "")
    return email

def interpret_spoken_char(spoken):
    spoken = spoken.lower().strip()
    mapping = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
        "at symbol": "@", "hash": "#", "dollar": "$", "percent": "%",
        "and": "&", "star": "*", "underscore": "_", "dash": "-", "dot": ".",
    }

    if spoken.startswith("capital "):
        return spoken[-1].upper()
    elif spoken.startswith("small "):
        return spoken[-1].lower()
    elif spoken.startswith("number "):
        return spoken.split()[-1]
    elif spoken in mapping:
        return mapping[spoken]
    elif len(spoken) == 1:
        return spoken
    return None

def get_password_by_voice():
    speak("Spell your password. Say one character or code word at a time. Say 'done' when finished.")
    chars = []
    while True:
        spoken = get_audio_input("Say next character:")
        if spoken in ["done", "end", "finish"]:
            break
        char = interpret_spoken_char(spoken)
        if char:
            chars.append(char)
            speak(f"Got {char}")
        else:
            speak(f"Sorry, I couldn't interpret '{spoken}'. Try again.")
    
    password = ''.join(chars)
    confirm = get_audio_input(f"You said: {password}. Is that correct? Say yes or no.")
    if "yes" in confirm:
        speak("Password confirmed.")
        return password
    else:
        speak("Let's try again.")
        return get_password_by_voice()

def send_email():
    speak("Welcome to Echo Mail.")

    sender_email = convert_spoken_email(get_audio_input("Say your email address."))
    speak(f"Your email is {sender_email}.")
    print("Recognized sender email:", sender_email)

    # VOICE-BASED PASSWORD INPUT
    sender_password = get_password_by_voice()

    # Password code + decode confirmation
    encoded = password_to_code(sender_password)
    print("Encoded password (for secure reference):", encoded)
    decoded = code_to_password(encoded)
    print("Decoded password (for confirmation):", decoded)
    speak(f"Your decoded password is {decoded}. Proceeding to send the email.")

    receiver_email = convert_spoken_email(get_audio_input("Say the receiver's email address."))
    speak(f"The recipient's email is {receiver_email}.")
    print("Recognized receiver email:", receiver_email)

    subject = get_audio_input("What is the subject?")
    body = get_audio_input("Say the body of your email.")

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        speak("Email sent successfully.")
    except Exception as e:
        speak("Failed to send the email.")
        print("Error:", e)

if __name__ == "__main__":
    send_email()
