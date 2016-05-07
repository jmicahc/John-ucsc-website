# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the codingimages action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

@auth.requires_login()
def add():
    """Add a post."""
    form = SQLFORM(db.codingimages)
    if form.process().accepted:
        # Successful processing.
        session.flash = T("inserted")
        redirect(URL('codingimages', 'index'))
    return dict(form=form)

def view():
    """View a post."""
    # p = db(db.codingimages.id == request.args(0)).select().first()
    p = db.codingimages(request.args(0)) or redirect(URL('codingimages', 'index'))
    form = SQLFORM(db.codingimages, record=p, readonly=True)
    # p.name would contain the name of the poster.
    return dict(form=form)

@auth.requires_login()
def edit():
    """View a post."""
    # p = db(db.codingimages.id == request.args(0)).select().first()
    p = db.codingimages(request.args(0)) or redirect(URL('codingimages', 'index'))
    if p.user_id != auth.user_id:
        session.flash = T('Not authorized.')
        redirect(URL('codingimages', 'index'))
    form = SQLFORM(db.codingimages, record=p)
    if form.process().accepted:
        session.flash = T('Updated')
        redirect(URL('codingimages', 'view', args=[p.id]))
    # p.name would contain the name of the poster.
    return dict(form=form)

@auth.requires_login()
def delete():
    """Deletes a post."""
    p = db.codingimages(request.args(0)) or redirect(URL('codingimages', 'index'))
    if p.user_id != auth.user_id:
        session.flash = T('Not authorized.')
        redirect(URL('codingimages', 'index'))
    db(db.codingimages.id == p.id).delete()
    redirect(URL('codingimages', 'index'))
    
def index():
    """Better index."""
    # Let's get all data.
    q = db.codingimages
    response.title = "Image Database"
    
    def generate_del_button(row):
        # If the record is ours, we can delete it.
        b = ''
        if auth.user_id == row.user_id:
            b = A('Delete', _class='btn', _href=URL('codingimages', 'delete', args=[row.id]))
        return b
    
    def generate_edit_button(row):
        # If the record is ours, we can delete it.
        b = ''
        if auth.user_id == row.user_id:
            b = A('Edit', _class='btn', _href=URL('codingimages', 'edit', args=[row.id]))
        return b
    
    # Creates extra buttons.
    
    links = [
        dict(header='', body = generate_del_button),
        dict(header='', body = generate_edit_button),
        ]

    #if len(request.args) == 0:
    #    # We are in the main index.
    #    links.append(dict(header='Post', body = shorten_post))
    
    form = SQLFORM.grid(q,
        fields=[db.codingimages.user_id,
                db.codingimages.imagename,
                db.codingimages.date_posted],
        editable=False, deletable=False,
        links=links,
        paginate=10,
        csv = False,
        )
    return dict(form=form)

def user():
    """
    exposes:
    http://..../[app]/codingimages/user/login
    http://..../[app]/codingimages/user/logout
    http://..../[app]/codingimages/user/register
    http://..../[app]/codingimages/user/profile
    http://..../[app]/codingimages/user/retrieve_password
    http://..../[app]/codingimages/user/change_password
    http://..../[app]/codingimages/user/manage_users (requires membership in
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
    http://..../[app]/codingimages/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/codingimages/call/jsonrpc
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
