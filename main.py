
import requests
from Features.wishme import wishMe
from Features.csv_writer import append_data
from Features.speak import speak
from Features.listen import listen



sender = "Prajwal"

bot_message = ""
speak(wishMe())
append_data("logs/chat_logs.csv","entered", "entered")
print("Hello, Welcome to the department of Artificial Intelligence and Data Science")
choice = input("Would you like to continue?")
if choice == "yes":
    while bot_message != "bye":
        
        user_message = listen()
        print("Sending message now....")
        r = requests.post("http://localhost:5005/webhooks/rest/webhook", json={"sender": sender, "message": user_message})
        print("Bot: ", end = ' ')
        
        for i in r.json():
            bot_message = i["text"]
            speak(bot_message)
            append_data("logs/chat_logs.csv", user_message,bot_message )   
    
