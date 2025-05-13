from shlex import quote
import sqlite3
import struct
import subprocess
import time
import hugchat
from playsound import playsound
import eel
import os
import pvporcupine
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME, YOUR_ACCESS_KEY
import pywhatkit as kit
import webbrowser
import sqlite3
from engine.helper import extract_yt_term, remove_words

#playsound assistant function 
@eel.expose
def platAssistantSound():
    music_dir="www//assets//audio//start_sound.mp3"
    playsound(music_dir)

# opening tabs
def openCommand(query):
    connection = sqlite3.connect("database/edith.db")
    # using cursor we can execuite quires
    cursor= connection.cursor()

    query = query.replace(ASSISTANT_NAME,"")
    query = query.replace("open","")
    query = query.strip().lower()
    app_name  = query

    if  app_name !="":
        try:
            cursor.execute(
                'SELECT path from sys_command WHERE name IN (?)',(app_name,)
            )
            results = cursor.fetchall()
            if len(results) !=0:
                speak(f"Opening {query}")
                os.system(f'open -a "{results[0][0]}"')
            elif len(results) == 0:
                cursor.execute(
                    'SELECT url FROM web_command WHERE name IN (?)', (app_name,)
                )
                results = cursor.fetchall()
                if len(results) != 0:
                    speak(f"Opening {query}")
                    webbrowser.open(results[0][0])
                else:
                    speak(f"Opening {query}")
                    os.system(f'open -a "{query}"')
                    print(f"open {query}")
        except sqlite3.Error as e:
            speak(f"Database error: {e}")
        except FileNotFoundError:
            speak(f"Sorry, I couldn't find the file or application named {query}")
        except Exception as e:
            speak(f"An unexpected error occurred: {e}")
        finally:
            connection.close()
    
    
def playYoutube(query):
    search_term = extract_yt_term(query)
    print(f"Extracted search term: {search_term}")  # Debugging

    if search_term:
        speak(f"Playing {search_term} on YouTube")
        kit.playonyt(search_term)
        return
    else:
        speak("Sorry, I couldn't understand what to play on YouTube.")
        return

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try: 
        # pre trained keywords    
        # Use pre-trained keywords with access key
        porcupine = pvporcupine.create(
            access_key=YOUR_ACCESS_KEY,  # Replace with your Picovoice access key
            keywords=["jarvis"]
        )
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length*2)
        
        # loop for streaming
        while True:
            try:
                keyword = audio_stream.read(porcupine.frame_length)
                keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
                keyword_index = porcupine.process(keyword)
                modifier = 'ctrl'  

                if keyword_index == 0:  # "jarvis" detected
                    print("Hotword 'jarvis' detected")
                    speak("Yes, how can I assist you?")
                    import pyautogui as autogui
                    time.sleep(1)
                    autogui.hotkey(modifier, 'e')
                    # autogui.keyDown("command")
                    # autogui.press("e")
                    # time.sleep(2)
                    # autogui.keyUp("command")
                    
            except OSError:
                continue
            # keyword=audio_stream.read(porcupine.frame_length)
            # keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)
            # # Debugging: Check if audio is being captured
            # # print("Audio captured:", keyword[:10])  # Print the first 10 samples

            # # processing keyword comes from mic 
            # keyword_index=porcupine.process(keyword)
            # # Debugging: Check if a keyword is detected
            # # print("Keyword index:", keyword_index)

            # # checking first keyword detetcted for not
            # if keyword_index>=0:
            #     print("hotword 'jarvis' detected")
            #     speak("Yes, how can I assist you?")
            #     # pressing shorcut key win+j
            #     import pyautogui as autogui
            #     # autogui.keyDown("meta")
            #     autogui.press("e")
            #     time.sleep(2)
            #     # autogui.keyUp("meta")
                      
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


#finding contacts
def findContact(query):
    words_to_remove = [ASSISTANT_NAME,'make','a','to','phone','call','send','message','whatsapp','video']
    query= remove_words(query,words_to_remove)
    try:
        query = query.strip().lower()
        connection = sqlite3.connect("database/edith.db")
        # using cursor we can execuite quires
        cursor= connection.cursor()
        cursor.execute('SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?',("%"+query+"%",query+ '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str ='+91' + mobile_number_str
        return mobile_number_str,query
    except:
        speak('not exit in  contacts')
        return 0,0

def whatsApp(mobile_no,message,flag,name):
    if flag == 'message':
        target_tab = 12
        jarvis_message = f'message sent successfully to {name}'

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = f'calling to {name}' 
    else:
        target_tab = 6
        message = ''
        jarvis_message = f'starting video call with {name}'

    #encode the message for url
    encoded_message = quote(message)
    #construvct the URL
    whatsApp_url = f'whatsapp://send?phone={mobile_no}&text={encoded_message}'
    # Open WhatsApp with the constructed URL using the macOS `open` command
    
    # Wait for WhatsApp to open
    
    #construct the full command
    full_command = f'open "" "{whatsApp_url}"'

    #open whatsapp with the constructed url using cmd.exe
    try:
        subprocess.run(full_command,shell= True)
        time.sleep(5)
        subprocess.run(full_command,shell= True)
        pyautogui.hotkey('command','f')
        for i in range(1,target_tab):
            pyautogui.hotkey('tab')
        pyautogui.hotkey('return')
        speak(jarvis_message)

    except subprocess.  CalledProcessError:
        speak("Failed to open WhatsApp. Please ensure it is installed.")
    except Exception as e:
        speak(f"An unexpected error occurred: {e}")

def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response