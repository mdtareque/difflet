# -*- coding: utf-8 -*-

#db.define_table('student', Field('name') )
db.define_table('category'
                ,Field('name', 'string', length=255, required=True, unique=True, comment='higher level category names')
                ,auth.signature)

db.category.name.represent = lambda name, row : name.capitalize()


db.define_table('thing'
                ,Field('category', 'reference category')
                ,Field('name', 'string', length=255, required=True, unique=True, comment='name of thing/entity')
                ,auth.signature)

db.thing.name.represent = lambda name, row : name.capitalize()


db.define_table('point'
                ,Field('property', 'string', length=255, required=True, unique=True, comment='property-name e.g. capital, currency')
                ,auth.signature)


db.define_table('description'
                ,Field('body', 'text', length=255, required=True, comment='data for corresponding property/key')
                ,auth.signature)


db.define_table('listings'
                ,Field('thing', 'reference thing')
                ,Field('point', 'reference point')
                ,Field('description', 'reference description')
                ,auth.signature)


# stores recent difflets for past 10 days
# or minimum of 10
db.define_table('recents'
                ,Field('thing1', 'reference thing')
                ,Field('thing2', 'reference thing')
                ,Field('last_accessed', 'datetime', default=request.now)
                ,auth.signature)


# stores difflets with hitcount > 10
# to be checked every day once
db.define_table('popular'
                ,Field('thing1', 'reference thing')
                ,Field('thing2', 'reference thing')
                ,Field('hits', 'integer', default=1)
                ,Field('last_accessed', 'datetime', default=request.now)
                ,auth.signature)
'''
'''






