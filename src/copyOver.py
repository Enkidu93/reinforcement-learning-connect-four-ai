import json
import csv
def loadStates():
    with open('C:\\Users\\LOWRYEC17\\reinforcement-learning-connect-four-ai\\src\\states.json','r') as json_file:
        states = json.load(json_file)
    return states

def writeStates(states):
    with open('C:\\Users\\LOWRYEC17\\reinforcement-learning-connect-four-ai\\src\\states2.json','w') as outfile:
        json.dump(states, outfile)

states = loadStates()
writeStates(states)

with open('states2.csv', 'w') as f:
    for key in states.keys():
        f.write("%s, %s\n" % (key, states[key]))
