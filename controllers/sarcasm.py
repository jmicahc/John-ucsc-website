import json
from datetime import date
import ConfigParser
import gluon.contrib.simplejson
import random

def preview():
    description = P('Rate the sarcsasm level of short video clips.')

    studyname = "sarcasm"

    return dict(description=description, studyname=studyname)

def savedata():
    data = gluon.contrib.simplejson.loads(request.body.read())
    
    #condition = request.vars['condition']
    #workercode = request.vars['workercode']
    #wid = request.vars['worder_id'] or random.randint(1000000, 9999999)
    #studyname = request.vars['study_name'] or 'Sarcasm'

    def flatten(x):
        '''
        Flattens an n-dimentional list and returns a·
        one dimentional list composed of all the elements
        in the orgiginal list.
        '''
        result = []
        for el in x:
            if hasattr(el, "__iter__") and not isinstance(el, basestring) and not type(el)==dict:
                result.extend(flatten(el))
            else:
                result.append(el)
        return result

    data = flatten(data)
    #for entry in data:
    #    db.sarcasm.bulk_insert([entry])

    return dict()

def dashboard():
    response.title = "Experiment dashboard"

    form = SQLFORM.grid(db.sarcasm.trial_index == 3,
            [db.sarcasm.workercode,
            db.sarcasm.cond,
            db.sarcasm.rt,
            db.sarcasm.Q0,
            db.sarcasm.Q1],
            editable=True, deletable=True,
            paginate=10
            )

    return dict(form=form)


def index():
    response.title = None

    condition = "even_audio_video"

    request.vars['condition'] = condition
    
    instructions = P('In this study you will make judgements about the sarcasm level of a sequence\
            of video clips. It will take about 10 minutes to complete. Press enter to continue.\
            Please note that this study is in development and may not work on all browsers.')
    return dict(instructions=instructions)
