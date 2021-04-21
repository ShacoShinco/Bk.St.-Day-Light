import csv
import pickle
from grabber import ChatBoxGrabber

#to CSV
fields = ['id', 'user', 'hour', 'minute', 'second', 'message']

a = pickle.load(open('data.pickle', 'rb'))
#user_names = ['Mor', 'max23', 'Mobina', 'تمام', 'The Consulting Criminal', 'دوست جمجمه ای', '^_^', 'Percy -2', 'Sherlocka1985', 'Barney', 'Meshkat', 'Alishia', 'yellownarcissus', 'فازی - ری', 'arsha', 'Lestrade', 'omid.rph', 'nika', 'Rosita', 'liosa', 'شرل', '.Yasaman.', 'RON!N', '♥♥♥♥', 'Lili Stark', 'Milad', 'Ἄτλας', 'Harry', 'DarkGuy', 'Dazai', 'sheiza', 'شرلوک\u200cهلمز', 'Nila', 'Louis', 'Rend', 'hyeya', 'Cripher']

rows = [
    [id, data.user, data.time.hour, data.time.minute, data.time.second, data.message] for id, data in a.items()
    ]

pickle.dump([fields, *rows], open("data.pc", 'wb'))