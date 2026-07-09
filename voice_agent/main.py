import speech_recognition as sr

def main():
    r=sr.Recognizer()   #Speech to text

    with sr.Microphone() as source: #Mic Access
        r.adjust_for_ambient_noise(source)
        r.pause_threshold=3

        print("Speak something........")
        audio=r.listen(source)

        print("Processing Audio...(STT)")
        stt=r.recognize_google(audio)

        print("You said:", stt)

main()