from datetime import datetime


db.define_table('Adaptation',
        Field('date_created', 'datetime', default=request.now),
        Field('worker_id'),
        Field('workercode'),
        Field('cond'),
        Field('study_name'),
        Field('trial_type'),
        Field('trial_index'),
        Field('rt'),
        Field('key_press'),
        Field('Q0')
        )

db.define_table('sarcasm',
        Field('date_created', 'datetime', default=request.now),
        Field('worker_id'),
        Field('workercode'),
        Field('cond'),
        Field('study_name'),
        Field('trial_type'),
        Field('trial_index'),
        Field('rt'),
        Field('Q0'),
        Field('Q1')
        )


db.define_table('misophonia',
        Field('date_created', 'datetime', default=request.now),
        Field('study_name'),
        Field('sj_id'),
        Field('sj_initials'),
        Field('cond'),
        Field('trial_type'),
        Field('trial_index'),
        Field('rt'),
        Field('Q0'),
        Field('Q1'),
        Field('Q2')
        )

db.define_table('misophonia_stim',
        Field('date_created', 'datetime', default=request.now),
        Field('user_id', db.auth_user),
        Field('cond'),
        Field('video', 'upload')
        )



db.define_table('polygons',
        Field('date_created', 'datetime', default=request.now),
        Field('Face_Number'),
        Field('polygon_id'),
        Field('polygon_names'),
        Field('verticies')
        )


db.define_table('facecoding',
        Field('date_created', 'datetime', default=request.now),
        Field('user_id'),
        Field('name'),
        Field('left_eye', 'json'),
        Field('right_eye', 'json'),
        Field('lip_top', 'json'),
        Field('lip_bottom', 'json'),
        Field('eyebrow_left', 'json'),
        Field('eyebrow_right', 'json')
        )


db.define_table('codingimages',
                Field('imagename', label="image name"),
                Field('user_id', db.auth_user),
                Field('date_posted', 'datetime', default=request.now),
                Field('image', 'upload')
                )


db.misophonia_stim.user_id.default = auth.user_id
db.codingimages.user_id.default = auth.user_id
db.codingimages.user_id.writable = db.codingimages.user_id.readable = False
