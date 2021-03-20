"""Routes for the course resource.
"""

from run import app
from flask import request
from http import HTTPStatus
import data
import json
import datetime


@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    # YOUR CODE HERE
    try:
        return json.dumps({'data':data.courses[id]}), 200, {'ContentType':'application/json'} 
    except KeyError:
        return json.dumps({'message':f'Course {id} not exist'}), HTTPStatus.NOT_FOUND, {'ContentType':'application/json'}


@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    # YOUR CODE HERE
    args=request.args
    pagenumber=int(args.get('page-number',1))
    pagesize=int(args.get('page-size',10))
    titlewords = args.get('title-words',None)
    
    data1=[]
    if titlewords:
        for i in data.courses.values():
            c=0
            for j in titlewords:
                if j in i['title']:
                    c+=1
            if c:
                data1.insert(c, i)
        data1=data1[::-1]
        data1=data1[(pagenumber-1)*pagesize+1: pagesize*pagenumber]
        metadata={"page_count":-(-len(data1)//pagesize),
                "page_number":pagenumber,
                "page_size":pagesize,
                'record_count':len(data1)}
    else:
        for i in range((pagenumber-1)*pagesize+1, pagesize*pagenumber):
            # print(i)
            data1.append(data.courses[i])
        metadata={"page_count":-(-len(data.courses)//pagesize),
                "page_number":pagenumber,
                "page_size":pagesize,
                'record_count':len(data.courses)}
    
    return json.dumps({'data':data1, 'metadata':metadata}), 200, {'ContentType':'application/json'} 



@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    # YOUR CODE HERE
    form=dict(request.form)
    idx=max(data.courses)
    form['id']=idx
    form['date_created'], form['date_updated']= str(datetime.datetime.now()), str(datetime.datetime.now())
    data.courses[idx]=form

    return json.dumps({'data':form}), 200, {'ContentType':'application/json'} 

    

@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    # YOUR CODE HERE
    form=dict(request.form)
    form['date_updated']=str(datetime.datetime.now())
    if id == form['id']:
        data.courses=form
        return json.dumps({'data':form}), 200, {'ContentType':'application/json'} 
    else:
        return json.dumps({'message':"The id does not matches the payload"}), 400, {'ContentType':'application/json'} 



@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE
    try:
        del data.courses[id]
        return json.dumps({'message':"The specified key was deleted"}), 200, {'ContentType':'application/json'} 
    except KeyError:
        return json.dumps({'message':f'Course {id} does not exist'}), 404, {'ContentType':'application/json'} 

