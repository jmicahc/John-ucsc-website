# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

import gluon.contrib.simplejson
import json

def preview():
    description = "Help 'code' faces by creating polygons around important\
            facial features."
    studyname= 'facecoding2'
    return dict(description=description, studyname=studyname)

@auth.requires_login()
def add():
    """Add a post."""
    form = SQLFORM(db.codingimages)
    if form.process().accepted:
        # Successful processing.
        session.flash = T("inserted")
        redirect(URL('default', 'index'))
    return dict(form=form)


def dashboard():
    response.title = "Face Coding Dashboard"
    form = SQLFORM.grid(db.polygons,
            [
                db.facecoding.date_created,
                db.facecoding.user_name,
                db.facecoding.polygon_name,
                db.facecoding.x_verts,
                db.facecoding.y_verts

            ])
    return dict(form=form)

@auth.requires_login()
def savedata():
    img_struct = gluon.contrib.simplejson.loads(request.body.read())
    q = (db.facecoding.user_id == auth.user.id) & (db.facecoding.name == img_struct["name"])
    s = db(q).select()
    r = s.first()
    if r:
        #del r["file"]
        r.update_record(left_eye=img_struct["left_eye"],
                right_eye=img_struct["right_eye"],
                eyebrow_left=img_struct["eyebrow_left"],
                eyebrow_right=img_struct["eyebrow_right"],
                lip_top=img_struct["lip_top"],
                lip_bottom=img_struct["lip_bottom"])
    else:
        db.facecoding.insert(name=img_struct["name"],
                             user_id=img_struct["user_id"],
                             eyebrow_left=img_struct["eyebrow_left"],
                             eyebrow_right=img_struct["eyebrow_right"],
                             lip_top=img_struct["lip_top"],
                             lip_bottom=img_struct["lip_bottom"],
                             left_eye=img_struct["left_eye"],
                             right_eye=img_struct["right_eye"])

@auth.requires_login()
def getimages():
    images = []
    for row in db(db.codingimages.id > 0).select():
        img_struct = {
                "name": row.imagename,
                "file": row.image,
                "user_id": auth.user.id,
                "eyebrow_left": [],
                "eyebrow_right": [],
                "left_eye": [],
                "right_eye": [],
                "lip_top": [],
                "lip_bottom": []
                }
        name = img_struct["name"]
        q = (db.facecoding.user_id == auth.user.id) & (db.facecoding.name == name)
        s = db(q).select()
        r = s.first()
        if r:
            img_struct.update({
                "eyebrow_left": r["eyebrow_left"] or [],
                "eyebrow_right": r["eyebrow_right"] or [],
                "left_eye": r["left_eye"] or [],
                "right_eye": r["right_eye"] or [],
                "lip_top": r["lip_top"] or [],
                "lip_bottom": r["lip_bottom"] or []
                })
        images.append(img_struct)
    return gluon.contrib.simplejson.dumps(images)

@auth.requires_login()
def index():
    user_name = auth.user.first_name + "_" + auth.user.last_name
    if len(request.args)==0:
        request.args.append(1)

    response.title = None

    form = SQLFORM(db.facecoding,
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
    return dict(form=form, user_name=user_name)



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
