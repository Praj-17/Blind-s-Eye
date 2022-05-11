
import datetime
from word2number import w2n
def set_alarm():
    try:
        alarmH=w2n.word_to_num()
    except Exception as e:
        print(e)
    
        alarmH=w2n.word_to_num()            
    alarmM = w2n.word_to_num()        
    ampm = str()      

    if(ampm=='pm'):
        alarmH=alarmH+12
        f =1;
        while f:
            if (alarmH== datetime.datetime.now().hour and alarmM==datetime.datetime.now().minute):
                pass
        return []
             
                    
                
