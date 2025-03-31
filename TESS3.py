import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import cv2

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am TESS. How may I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except Exception:
        print("Say that again please...")
        return None  # Return None if no valid command
    
def play_song(song_name):
    try:
        if song_name:
            song_name = song_name.strip().replace(" ", "+")  # Format for URL
            url = f"https://open.spotify.com/search/{song_name}"
            webbrowser.open(url)
            print(f"Opening Spotify and searching for: {song_name}")
        else:
            print('no song name provided')
    except Exception as e:
        print("No song is played.")
        speak("Sorry, No song is played.")  
    
def open_camera():
    camera = cv2.VideoCapture(0)  # Open the default camera (0)
    
    if not camera.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        cam, frame = camera.read()  # Read frame from camera
        if not cam:
            print("Failed to capture image")
            break

        cv2.imshow("Camera", frame)  # Display the camera feed

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break

    camera.release()  # Release the camera
    cv2.destroyAllWindows()  # Close the window

def close_camera():
    camera=cv2.VideoCapture(0)
    camera.release()

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        
        sender_email = "your-email-id"
        sender_password = "your-app-password"

        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to, content)
        server.close()
        print("Email sent successfully!")
        speak("Email has been sent!")
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I am not able to send this email.")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()
        if query is None:
            continue  # Skip processing if no valid command

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'pu website' in query or 'wifi login' in query:
            webbrowser.open("puchd.ac.in")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"The time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\hp\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'play music' in query or 'play song' in query or 'song' in query:
            try:
                speak("What song you wanna play?")
                s_name=takeCommand().lower()
                if s_name!="none":
                    play_song(s_name)
                else:   
                    speak("No song name provided.")
            except Exception as e:
                speak("Sorry i am not able to do so.") 

        elif 'email' in query or 'gmail' in query or 'mail' in query:
            try:
                speak("Whom should I send the email to?")
                name = takeCommand()
                email_dic = {'dhiman': 'shriyadhiman08@gmail.com',
                     'lavanya': 'lavanyakapoor1808@gmail.com',
                     'dilreet': 'topazchrysanthemum045@gmail.com'}
                if name in email_dic:
                    to = email_dic[name]
                    speak("What should I say?")
                    content = takeCommand()
                    sendEmail(to, content)
                else:
                    speak("Sorry, I don't have this person's email.")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email.")

        elif 'who is tes' in query or 'who are you' in query or 'tell about yourself' in query:
            speak("I am Tess, an AI voice assistant developed by Shriya Dhiman. I am currently a basic prototype. I am capable of few small tasks.")

        elif 'open camera' in query or 'camera' in query:
            print("Press q to stop camera.")
            open_camera()
            
        
        
        elif 'exit' in query or 'stop' in query or 'bye' in query :
            speak("Goodbye! Have a nice day.")
            break  # Stop the loop and exit
