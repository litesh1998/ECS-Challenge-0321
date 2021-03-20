"""Routines associated with the application data.
"""
import json
courses = {}

def load_data():
    """Load the data from the json file.
    """
    f=open('json/course.json', 'r')
    temp=json.load(f)
    # print (temp[0])
    for i in temp:
        courses[i['id']]=i
    # print(courses[1])


if __name__=='__main__':
    load_data()


