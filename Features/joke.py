from pyjokes import get_joke
from random import randint

'''
returns  a joke in string format
you can also add custom jokes in the list
'''
joke_list=[]

def startJoke():
    try:
        joke=get_joke()
    except:
        joke="I don't know any jokes"
    joke_list.append(joke)
    return (joke_list[randint(0,len(joke_list)-1)])

