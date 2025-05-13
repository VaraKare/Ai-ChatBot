import pyttsx3
import speech_recognition as sr
import eel
import time
def speak(text):
    text = str(text)
    print(f"speak() called with text: {text}")  # Debugging
    engine = pyttsx3.init('nsss') # we can pass the voice in this init 
    # voices=engine.getProperty('voices')
    engine.setProperty('rate', 190)  # Set speech rate (default is ~200, lower is slower)
    engine.setProperty('volume', 1.0)  # Set volume (1.0 is max, 0.0 is min)
    try:
        eel.sleep(1)  # Wait for the frontend to initialize
        print("Attempting to call DisplayMessage...")
        eel.DisplayMessage(text)  # Send the message to the frontend
        print("DisplayMessage called successfully.")
    except AttributeError:
        print("Error: DisplayMessage is not defined in the frontend.")
    except Exception as e:
        print(f"Unexpected error: {e}")

    engine.say(text)
    try:
        time.sleep(2)
        eel.receiverText(text)
    except AttributeError:
        print("Error: receiverText is not defined in the frontend.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage('Listening...')
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source,15,10)

    try:
            # audio = r.listen(source, timeout=10, phrase_time_limit=6)
            print("Audio captured, recognizing...")
            eel.DisplayMessage('recognizing...')
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            eel.DisplayMessage(query)
            # speak(query)
            time.sleep(3 )
            return query.lower()
    except sr.WaitTimeoutError:
        print("Listening timed out. No speech detected.")
        return None
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    
@eel.expose
def allCommands(message =1):
    if message == 1:
        query = takeCommand()
        print(query) 
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    
    try:
        if 'play' in query and 'on youtube' in query:
            from engine.features import playYoutube
            playYoutube(query)
            
        elif 'open' in query:
            from engine.features import openCommand
            openCommand(query)
            
        elif "send message" in query or "phone call" in  query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takeCommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("what message to send")
                        message = takeCommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                            makeCall(name, contact_no)
                    else:
                            speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takeCommand()
                                            
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                            
                    whatsApp(contact_no, query, message, name)
        else:
            from engine.features import chatBot
            chatBot(query)
    except Exception as e:
        print(f"An error occurred: {e}")
        
    # If no valid command is found, execute this block
    # speak("Sorry, I couldn't understand your command.")
    eel.ShowHood()
