# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

import json
from datetime import date
import ConfigParser
import gluon.contrib.simplejson
import random

def preview():
    description = P("This study is a study about how the brain represents faces. \
            You will rate various attrbutes of faces.")
    studyname = "adaptation"
    return dict(description=description, studyname=studyname)


def savedata():
    data = gluon.contrib.simplejson.loads(request.body.read())
    logger.info(data)
    condition = request.vars['condition']
    workercode = request.vars['workercode']
    wid = request.vars['worder_id'] or random.randint(1000000, 9999999)
    studyname = request.vars['study_name'] or 'Sarcasm'

    def flatten(x):
        '''
        Flattens an n-dimentional list and returns a 
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

    logger.info("data %s" %(flatten(data)))
    data = flatten(data)
    for entry in data:
        entry.update( 
        {
            'worker_id': wid,
            'cond' : condition,
            'study_name' : studyname,
            'workercode' : workercode
        })


        logger.info('entry %s' %(entry))
        db.Adaptation.bulk_insert([entry])

    return dict()

def dashboard():
    response.title = 'Experiment Dashboard'

    form = SQLFORM.grid(db.Adaptation.trial_index > 0,
            [db.Adaptation.workercode,
            db.Adaptation.cond,
            db.Adaptation.rt,
            db.Adaptation.Q0],
        editable=True, deletable=True,
        paginate=10
        )
    return dict(form=form)

def getdata():
    conditions = [
            'mf-ns',
            'fef-ns',
            'mf-nf',
            'fef-nf',
            'ms-nf',
            'fes-nf',
            'ms-ns',
            'fes-ns',
            'ns',
            'nf',
            ]


    queries = [
            db.Adaptation.cond == 'male_front_neutral_sil',
            db.Adaptation.cond == 'female_front_neutral_sil',
            db.Adaptation.cond == 'male_front_neutral_front',
            db.Adaptation.cond == 'female_front_neutral_front',
            db.Adaptation.cond == 'male_sil_neutral_front',
            db.Adaptation.cond == 'female_sil_neutral_front',
            db.Adaptation.cond == 'male_sil_neutral_sil',
            db.Adaptation.cond == 'female_sil_neutral_sil',
            db.Adaptation.cond == 'male_sil_neutral_front',
            db.Adaptation.cond == 'female_front_neutral_sil'
            ]

    neutral_rating = (db.Adaptation.trial_index == 3) # & (db.Adaptation.rt < 5000)
    neutral_rating2 = (db.Adaptation.trial_index == 0) & \
           (db.Adaptation.trial_type == 'survey-likert') & \
           (db.Adaptation.id > (1344 - 120))

    d = []
    for j, q in enumerate(queries):
        if j < 8:
            ratings = [int(r.Q0) for r in db(q & neutral_rating).select('Q0')]
        else:
            ratings = [int(r.Q0) for r in db(q & neutral_rating2).select('Q0')]
        obj = {}
        obj['Male'] = sum([1 for i in ratings if i == 1])
        obj['Female'] = sum([1 for i in ratings if i == 3])
        obj['Unsure'] = sum([1 for i in ratings if i == 2])
        obj['Condition'] = conditions[j]
        d.append(obj)

    return gluon.contrib.simplejson.dumps(d)

def consent():
    response.title = None

    return dict()

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """


    filepath = 'applications/Adaptation/config.cfg'
    config = ConfigParser.ConfigParser()
    config.read(filepath)

    ptr = config.getint('Pointer', 'current_condition')
    all_conds = config.items('Condition')

    if ptr >= len(all_conds):
        ptr = 0
        config.set('Pointer', 'current_condition', '0')

    condition = all_conds[ptr]
    config.set('Pointer', 'current_condition', str(ptr+1))

    request.vars['study_name'] = 'Adaptation'

    with open(filepath, 'wb') as configfile:
        config.write(configfile)

    pic1 = condition[0]
    pic2 = condition[1]
    request.vars['condition'] = pic1[:pic1.index('.')] + '_' + pic2[:pic2.index('.')]


    response.title = None
    test = request.vars
    logger.info('test %s:' %(test))

    return dict(pic1=pic1, pic2=pic2)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
