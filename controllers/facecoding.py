# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

import gluon.contrib.simplejson

def preview():
    description = "Help 'code' faces by creating polygons around important\
            facial features."
    studyname= 'facecoding'
    return dict(description=description, studyname=studyname)

def dashboard():
    response.title = "Face Coding Dashboard"
    form = SQLFORM.grid(db.polygons,
            [
                db.polygons.date_created,
                db.polygons.polygon_id,
                db.polygons.polygon_names,
                db.polygons.verticies
            ])
    return dict(form=form)

def getpolys():
    polygons = [p.verticies for p in 
             list(db(db.polygons.id == 1).select('verticies'))]
    return polygons
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    if len(request.args)==0:
        request.args.append(1)

    response.title = None


    form = SQLFORM(db.polygons,
         hidden=dict(Date_Created='this is a test.')
         )

    form.Face_Number = request.args[0]
    if form.process().accepted:
        session.flash = T('Updated')
        trial = int(request.args[0])
        if trial < 6:
            redirect(URL('facecoding', 'index', args=[int(request.args[0])+1]))
        else:
            redirect(URL('shared', 'debrief', args=[trial]))
    return dict(form=form)



def user():
    """
    expmses:
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
