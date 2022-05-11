# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,UserUtteranceReverted, ActionReverted
from datetime import datetime, timedelta
from regex import P
import wikipedia
from Features.news import get_news
import webbrowser
from Features.alarm import set_alarm
from Features.joke import startJoke
from Features.weather import weather_from_city, weather_local
from Features.wishme import wishMe
from Features.object_detection import object_detection,get_object
from Features. navigation import navigation, get_direction
from sanic.config import Config
from Features.asia_landmarks import landmark_detection_with_address
from Features.get_image import get_image
from Features.text_detector import text_detector
from inference.video_classifier import face_recongizer
from Features.speak import speak
from Features.listen import listen
from Features.main_face import create_training_image_folder
import os
Config.KEEP_ALIVE_TIMEOUT = 60
Config.KEEP_ALIVE = False
try:
    import pywhatkit
except Exception as e:
    print("Exception: ", e)


def pywhatkit_search(query):
    query = str(query).replace("google", "").replace("search", "").replace("","").replace("what is","").replace("search about","").replace("search for","").replace("find","").replace("about","").replace("for","").replace("tell me ", "").replace("tell me something about ","").replace("tell", "")
    try:
               
                print("Going for Pywhatkit google search instead")
                pywhatkit.search(query)
    except Exception as e:
                print("Exception: ", e)
                print("Pywhatkit search failed...!!")
def dict_to_word(dict):
    word = ""
    for key, value in dict.items():
        word += key + ": " + value + " "
    return word
class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
class ActionObjectDetection(Action):

    def name(self) -> Text:
        return "action_object_detection"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            print("entered object detection")
            object_detection()
            dispatcher.utter_message(text=get_object())
            print("Object Detection Completed...")           
class ActionTime(Action):

    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            time = datetime.now().strftime("%H: %M")
            dispatcher.utter_message(text=f"Current Time: {time}")
class ActionFallBack(Action):

    def name(self) -> Text:
        return "action_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase it?")
            """
            A proper approach to implement this would be to have a fallback action by listing all the things that the bot can do. by using the buttons
            """
class ActionNavigation(Action):

    def name(self) -> Text:
        return "action_navigation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            print("Entering navigation")
            navigation()
            direction = get_direction()
            print("Direction: ", direction)
            dispatcher.utter_message(text=direction)
            print("Navigation Completed...")         
class ActionWishme(Action):

    def name(self) -> Text:
        return "action_wishme"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            print("Entered Wishme action")
            dispatcher.utter_message(text=wishMe())
class ActionFaceRecognition(Action):

    def name(self) -> Text:
        return "action_face_recognition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            print("Entered Face Recognition action")
            try:
               person, confidence =  face_recongizer()
            except Exception as e:
                print("Exception: ", e)
            if int(confidence) > 50:
                if person == 'OTHERS':
                    speak('You seem new to me')
                    speak('Do you want to save your face?')
                    user_choice = listen()
                    if user_choice.lower() == 'yes':
                        speak("Please provide a name")
                        name = listen()
                        create_training_image_folder(name, 10)
                    dispatcher.utter_message(text = 'Thankyou')
                    #Training the new images(will look for time constraints)
                    os.system('cmd /k "python -m training.train -d "images""')
                else:
                    dispatcher.utter_message(text=person)
            else:
                dispatcher.utter_message('Unable to detect faces clearly')
            
            
            
            
          
class ActionWeather(Action):

    def name(self) -> Text:
        return "action_tell_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            print("Entered weather Action")
            try:
                city_ent = tracker.latest_message['city_entities'][0]['value']                
            except:
                city_ent = "None"
                try:
                    city_slot = tracker.get_slot('city')
                    
                except:
                    city_slot = "None"
                    
            print("Extracted City entity: ", city_ent)
            print("Extracted City slot: ", city_slot)
            
            
            if city_ent == "None" and city_slot == "None":
                weather = weather_local()
                
                dispatcher.utter_message(text= weather)
            elif city_ent != "None" and city_slot == "None":
                weather = weather_from_city(city_ent)
                
                dispatcher.utter_message(text=dict_to_word(weather))
                print(weather)
            elif city_ent == "None" and city_slot != "None":
                weather = weather_from_city(city_slot)
                
                dispatcher.utter_message(text=dict_to_word(weather))
                print(weather)
            elif city_ent != "None" and city_slot != "None" and city_ent == city_slot:
                weather = weather_from_city(city_ent)
                
                dispatcher.utter_message(text=dict_to_word(weather))
                print(weather)
            else:
                weather = weather_local()
                dispatcher.utter_message(text=weather)
                print(weather)
                
          
            print("Weather Action Completed...")         
class ActionJoke(Action):

    def name(self) -> Text:
        return "action_tell_joke"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            joke = startJoke()
            print("Entered the joke action")
            dispatcher.utter_message(text="Ok..! I'll Tell you a joke....")
            dispatcher.utter_message(text=f"{joke}")            
class ActionSetAlarm(Action):

    def name(self) -> Text:
        return "action_set_alarm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            # time = tracker.latest_message['entities'][0]['value']
            print(tracker.latest_message['entities'])
            print(type(tracker.latest_message['entities']))
            entities = []
            for index, entity in enumerate(tracker.latest_message['entities']):
                print(tracker.latest_message['entities'][index]['value'])
                entities.append(tracker.latest_message['entities'][index]['value'])
            print(entities)
            # time_zone = tracker.latest_message['entities'][1]['value']
            # print("Time: ", time)
            # print("Time Zone: ", time_zone)
            # # set_alarm()
            return []         
class ActionPlayYoutube(Action):

    def name(self) -> Text:
        return "action_play_on_youtube"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            try:
                ent = tracker.latest_message['entities'][0]['value']
            except:
                ent = "None"
            print("Extracted Keyword: ", ent)
            if ent == "None":
                webbrowser.open("https://www.youtube.com/")
                dispatcher.utter_message(text="Ok..! Playing Youtube")
            else:
                try:
                    pywhatkit.playonyt(ent)
                    dispatcher.utter_message(text=f" Playing {ent} on youtube") 
                    dispatcher.utter_message(text="Please check your browser, Enjoy the video!!")

                except Exception as e:
                    print("Exception: ", e)
                    print("Youtube search failed...!!")
class ActionNews(Action):

    def name(self) -> Text:
        return "action_tell_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            print("Entered the news action")
            news = get_news()
            for index , news in enumerate(news):  
                dispatcher.utter_message(text=f"\n{index+1}. {news}\n")     
class ActionGoogle(Action):

    def name(self) -> Text:
        return "action_google_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # It might gove error if there is no entity extracted
            ent = tracker.latest_message['entities'][0]['value']
                     
        except:
            ent = "None" # defining one default entity
        print("Keyword: ", ent)
        if ent != "None":
            pywhatkit_search(ent)
            dispatcher.utter_message(text=f"Searching for {ent}, Check Your Browser")
        else:
            query = tracker.latest_message['text']
            pywhatkit_search(query)
            return[]         
class ActionWikipedia(Action):

    def name(self) -> Text:
        return "action_search_wikipedia"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            try:
                try:
                    # It might gove error if there is no entity extracted
                     ent = tracker.latest_message['entities'][0]['value']
                     
                except:
                    ent = "None" # defining one default entity
                print("Keyword:",ent)
                if ent == "None":
                    query = tracker.latest_message['text']
                    query = str(query).replace("google", "").replace("search", "").replace("","").replace("what is","").replace("search about","").replace("search for","").replace("find","").replace("about","").replace("for","").replace("tell me ", "").replace("tell me something about ","").replace("tell", "")
                    try:
                        #we will try wikipedia search first and if it fails we will try google search
                        print("Searching for:",ent)
                        result = wikipedia.summary(query, sentences=3)
                        dispatcher.utter_message(text=result)
                    except Exception as e :
                        print("Wikipedia with no entity failed...", "Exception: ", e)
                    
                        pywhatkit_search(query)
                      
                    
                    dispatcher.utter_message(text="Check your browser for the results")
                    return []
                else:
                    print("Searching for:",ent)
                    result = wikipedia.summary(ent, sentences=3)
                    dispatcher.utter_message(text=result)
                    return []
            except Exception as e:
                print("Exception: ", e)
                print("Wikipedia search failed...!!")
            pywhatkit_search(ent)
class ActionDate(Action):

    def name(self) -> Text:
        return "action_tell_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            try:
                ent = tracker.latest_message['entities'][0]['value']
            except:
                ent = "None"
            print("The entity found is: ", ent)
            presentday = datetime.now().strftime("%A")
            yesterday = (datetime.now()- timedelta(1)).strftime("%A")
            tomorrow = (datetime.now()+ timedelta(1)).strftime("%A")
            
            if ent == "yesterday":
                date = datetime.today() - timedelta(days=1)
                dispatcher.utter_message(text=f"Yesterday's Date: {yesterday}, {date}")
                
            elif ent == "tomorrow":
                date = datetime.today() + timedelta(days=1)
                dispatcher.utter_message(text=f"Tomorrow's Date: {tomorrow}, {date}")
            else:
                date = datetime.today() 
                dispatcher.utter_message(text=f"Today's Date: {presentday}, {date}")              
class ActionLandmark(Action):

    def name(self) -> Text:
        return "action_tell_landmark_with_address"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Entered the landmark action")
        try:
            landmark = landmark_detection_with_address(get_image())['landmark']
            address = landmark_detection_with_address(get_image())['address']
        except Exception as e:
            print("Exception: ", e)
            print("Landmark detection failed...!!")
        dispatcher.utter_message(text=f"Landmark: {landmark} \nAddress: {address}")
        print("Landmark detection Completed")
class ActionText(Action):

    def name(self) -> Text:
        return "action_detect_text"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Entered the Text action")
        try:
            text = text_detector(get_image())
        except Exception as e:
            text = "None"
            print("Exception: ", e)
            print("Landmark detection failed...!!")
        dispatcher.utter_message(text=f"Text: {text}")
        print("Text detection Completed")
            
            
        

               
            
                
            
            
            



























# class YourResidence(Action):

#     def name(self) -> Text:
#         return "action_your_residence"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(template="utter_your_residence")

#         return [UserUtteranceReverted(), ActionReverted()] # By doing this we are basically asking our bot to forgot the last user utterance and to revert the last action. Basiscally we are making it forget that any such thing happened.

