from Features.speak import speak
from inference.video_classifier import face_recongizer
from Features.main_face import create_training_image_folder
import os

def train_new_face():
    speak("Please provide a name")
    name = input('Enter your name \n')
    name_final = name.replace(" ", "_")
    create_training_image_folder(name_final, 10)
    #Training the new images(will look for time constraints)
    os.system('start cmd /k start\\face_training.cmd')
    return  name

def FaceRecognition():
    try:
        person, confidence =  face_recongizer()
        print("Person: ", person)
        print("Confidence: ", confidence)
    except Exception as e:
        print("Exception: ", e)
    try:
        if int(confidence) > 50:
            if person == 'OTHERS':
                speak('You seem new to me')
                speak('Do you want to save your face?')
                user_choice = input('say "YES" or "NO"\n')
                if user_choice.lower() == 'yes':
                    try:
                        train_new_face()
                        speak( f'Thankyou {name}')
                    except Exception as e:
                        print('Exception: ', e)
            else:
                speak(person)
        elif int(confidence) < 50 and int(confidence) > 25:
            if person == 'OTHERS':
                speak('You seem new to me')
                speak('Do you want to save your face?')
                user_choice = input('say "YES" or "NO" \n')
                if user_choice.lower() == 'yes':
                    name =  train_new_face()
                    speak(f'Thankyou {name.lower().capitalize()}')
            else:
                speak('You look similar to ' + person.lower().capitalize() + ' Though I am not much sure')
                speak('Please tell me weather I am correct?')
                choice = input('Say "YES" or "NO"')
                if choice.lower() == 'YES':
                    speak( f'Thankyou {person.lower().capitalize()}')
                    #we can run an reinforcement model here
                else:
                    name =  train_new_face()
                    speak(f'Thankyou {name.lower().capitalize()}')
                    
            
        else:
            ('Unable to detect faces clearly')
    except Exception as e:
        print("Exception: ", e)