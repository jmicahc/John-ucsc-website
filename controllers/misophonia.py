import json
from datetime import date
import ConfigParser
import gluon.contrib.simplejson
import random


@auth.requires_login()
def add():
    """Add a post."""
    form = SQLFORM(db.misophonia_stim)
    if form.process().accepted:
        # Successful processing.
        session.flash = T("inserted")
        redirect(URL('misophonia', 'showstimuli'))
    return dict(form=form)

def view():
    """View a post."""
    # p = db(db.misophonia_stim.id == request.args(0)).select().first()
    p = db.misophonia_stim(request.args(0)) or redirect(URL('misophonia', 'showstimuli'))
    form = SQLFORM(db.misophonia_stim, record=p, readonly=True)
    # p.name would contain the name of the poster.
    return dict(form=form)

@auth.requires_login()
def edit():
    """View a post."""
    # p = db(db.misophonia_stim.id == request.args(0)).select().first()
    p = db.misophonia_stim(request.args(0)) or redirect(URL('misophonia', 'showstimuli'))
    if p.user_id != auth.user_id:
        session.flash = T('Not authorized.')
        redirect(URL('misophoniam', 'index'))
    form = SQLFORM(db.misophonia_stim, record=p)
    if form.process().accepted:
        session.flash = T('Updated')
        redirect(URL('misophonia', 'view', args=[p.id]))
    # p.name would contain the name of the poster.
    return dict(form=form)

@auth.requires_login()
def delete():
    """Deletes a post."""
    p = db.misophonia_stim(request.args(0)) or redirect(URL('misophonia', 'showstimuli'))
    if p.user_id != auth.user_id:
        session.flash = T('Not authorized.')
        redirect(URL('misophonia', 'showstimuli'))
    db(db.misophonia_stim.id == p.id).delete()
    redirect(URL('misophonia', 'showstimuli'))

def getstimuli():
  filters = []
  audio_stim = []
  stim_A = []
  stim_B = []

  for row in db(db.misophonia_stim.id > 0).select():
      if 'filter' in row.cond:
          filters.append({
            "file": '<video autoplay><source src=/init/misophonia/download/' + row.video + ' ></video>',
            "cond": row.cond + "_filter"})
      elif "A" in row.cond:
          stim_A.append({
            "file": '<video autoplay><source src=/init/misophonia/download/' + row.video + ' ></video>',
            "cond": row.cond + "_video"})
      elif "B" in row.cond:
          stim_B.append({
            "file": '<video autoplay><source src=/init/misophonia/download/' + row.video + ' ></video>',
            "cond": row.cond + "_video"})
          audio_stim.append({
            "file": '<video autoplay style="display:none"><source src=/init/misophonia/download/' + row.video + ' ></video>',
            "cond": row.cond + "_audio"})

  indices = range(8)
  random.shuffle(indices)
  video_stim = [stim_A[i] for i in indices[:4]] + [stim_B[i] for i in indices[4:]]
  random.shuffle(video_stim)

  random.shuffle(audio_stim)
  block_1 = [item for item in audio_stim]
  block_2 = video_stim
  random.shuffle(audio_stim)

  block_3 = [item for item in audio_stim]

  if int(block_1[-1]["cond"].split("_")[0]) == int(block_1[0]["cond"].split("_")[0]):
      temp = block_2[0]
      index = random.choice(range(1, len(block_2)))
      block_2[0] = block_2[index]
      block_2[index] = temp
  if int(block_2[-1]["cond"].split("_")[0]) == int(block_3[0]["cond"].split("_")[0]):
      temp = block_3[0]
      index = random.choice(range(1, len(block_3)))
      block_3[0] = block_3[index]
      block_3[index] = temp

  trials = filters + block_1 + block_2 + block_3

  return gluon.contrib.simplejson.dumps(trials)

#@auth.requirs(lambda: auth.user.name == "john")
def showstimuli():
    """Better index."""
    # Let's get all data.
    q = db.misophonia_stim
    response.title = "Image Database"
    
    def generate_del_button(row):
        # If the record is ours, we can delete it.
        b = ''
        if auth.user_id == row.user_id:
            b = A('Delete', _class='btn', _href=URL('misophonia', 'delete', args=[row.id]))
        return b
    
    def generate_edit_button(row):
        # If the record is ours, we can delete it.
        b = ''
        if auth.user_id == row.user_id:
            b = A('Edit', _class='btn', _href=URL('misophonia', 'edit', args=[row.id]))
        return b
    
    # Creates extra buttons.
    
    links = [
        dict(header='', body = generate_del_button),
        dict(header='', body = generate_edit_button),
        ]

    form = SQLFORM.grid(q,
        fields=[db.misophonia_stim.user_id,
                db.misophonia_stim.cond,
                db.misophonia_stim.video],
        editable=False, deletable=False,
        links=links,
        paginate=20,
        csv = False,
        )
    return dict(form=form)



def preview():
    description = P('Give your emotional response to different sounds.')
    studyname = "misophonia"

    return dict(description=description, studyname=studyname)

def savedata():
    data = gluon.contrib.simplejson.loads(request.body.read())
    studyname = "misophonia"

    def flatten(x):
        '''
        Flattens an n-dimentional list and returns a·
        one dimentional list composed of all the base elements
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
    sj_initials = request.vars['initials']
    sjid = 0
    if len(db(db.misophonia.id >= 0).select()) > 0:
        sjid = int(db(db.misophonia.id >= 0).select().last().sj_id) + 1

    for entry in data:
        if entry["trial_type"] != "survey-likert": continue
        db.misophonia.insert(
                   study_name=studyname,
                   sj_id=sjid,
                   sj_initials=sj_initials,
                   rt=entry["rt"],
                   cond=entry["cond"],
                   trial_type=entry["trial_type"],
                   trial_index=entry["trial_index"],
                   Q0=entry["Q0"],
                   Q1=entry["Q1"],
                   Q2=entry["Q2"])

def dashboard(): 
    response.title = "Experiment dashboard"

    def generate_del_button(row):
        # If the record is ours, we can delete it.
        b = A('Delete', _class='btn', _href=URL('misophonia', 'delete', args=[row.id]))
        return b


    links = [dict(header='', body = generate_del_button)]

    form = SQLFORM.grid(db.misophonia.id > 0,
            [db.misophonia.sj_id,
            db.misophonia.sj_initials,
            db.misophonia.cond,
            db.misophonia.rt,
            db.misophonia.Q0,
            db.misophonia.Q1,
            db.misophonia.Q2],
            headers= {
                'misophonia.Q0': "Comfort rating",
                'misophonia.Q1': "Pleasant rating",
                'misophonia.Q2': "Sensation rating"
                },
            editable=True, deletable=True,
            paginate=20
            )

    return dict(form=form)


def getinitials():
    response.title = None
    description = P('Please enter your initials.')
    form = SQLFORM.factory(
            Field('initials', requires=IS_NOT_EMPTY())
            )
    if form.process().accepted:
        initials = form.vars.initials
        redirect(URL('misophonia', 'index', vars={"initials": initials}))
    elif form.errors:
        response.flash = 'please enter initials.'
    return dict(description=description, form=form)


def index():
    response.title = None

    if not request.vars['initials']:
        redirect(URL('misophonia', 'getinitials'))

    condition = "even_audio_video"

    request.vars['condition'] = condition
    instructions = []
    instructions.append( P('In this study, you will be asked to make judgements about sounds and videos \
            that you hear. This expriment may take 15 minutes to complete. You may \
            discontinue this experiment at any time should you feel uncomfortable.') )
    
    instructions.append( P('You will now rate three training trials so you know how to use the \
            scales. Press enter to continue') )

    instructions.append( P('You will now begin the experiment. Do you have any questions? \
            If not, please press enter to continue.') )


    return dict(instructions=instructions)

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
