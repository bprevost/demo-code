#!/usr/bin/python

import json

DATAFILE = 'hp_guesser.json'

with open(DATAFILE, 'r') as fp:
    data = json.load(fp)

question = "Is it magical?" # Starting question
while True:
    response = raw_input(question + " (yes/no) ")
    if isinstance(data[question], dict):
        prior_question = question
        prior_response = response
        result = data[question][response]
        question = result
    elif response == "yes":
        print "I got it!"
        break
    elif response == "no":
        print "You stumped me!"
        answer = raw_input("OK, who is it then? ")
        new_question = raw_input("Give me a 'yes' question that would help identify " + answer + ".\n")
        answer = "Is it " + answer + "?"
        data[answer] = 0
        data[new_question] = {'yes': answer, 'no': question}
        data[prior_question][prior_response] = new_question
        print "Thanks!"
        break

with open(DATAFILE, 'w') as fp:
    json.dump(data, fp, sort_keys=True, indent=4)
