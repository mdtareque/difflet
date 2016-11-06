# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

def _thingId(ename):
    return db(db.thing.name==ename).select(db.thing.id)[0]['id']

def _thingName(id):
    return db(db.thing.id==id).select(db.thing.name)[0]['name']

def index():
    redirect(URL('default', 'search'))
    response.flash = T("Hello World")
    return dict(message=T('Difflet App Loaded!'))

def search():
    recents = db(db.recents).select(db.recents.thing1, db.recents.thing2, orderby = ~db.recents.last_accessed, limitby=(0,5))
    recent_searches = []
    try:
        for r in recents:
            recent_searches.append( (_thingName(r['thing1']), _thingName(r['thing2']))  )
    except:
        pass
    return locals()

def saveSearch(e1, e2): # save to recents
    from datetime import datetime as dt
    now = dt.today()
    e1id, e2id = _thingId(e1), _thingId(e2)
    e1id, e2id = min(e1id, e2id), max(e1id, e2id)
    q = (db.recents.thing1 == e1id) & (db.recents.thing2 == e2id)
    myset = db(q).select(db.recents.ALL, limitby=(0,1))
    if myset:
        db(q).update(last_accessed=now)
    else:
        db.recents.insert(thing1 =e1id, thing2= e2id, last_accessed=now)
    print "saved recents %s vs %s" % (e1, e2)
    q2 = (db.popular.thing1 == e1id) & (db.popular.thing2 == e2id)
    myset = db(q2).select(db.popular.ALL, limitby=(0,1))
    if myset:
        oldcount = myset[0]['hits']
        db(q2).update(hits = oldcount + 1, last_accessed=now)
    else:
        db.popular.insert(thing1 =e1id, thing2= e2id, hits=1, last_accessed=now)
    print "update hit %s vs %s" % (e1, e2)
    return

def random():
    # 'country', animal and company
    data = [
     ['india', 'australia', 'egypt'],
     ['lion', 'deer'],
     ['apple co.', 'google', 'ibm']
    ]
    import random as rand_
    r1 = rand_.randrange(0, len(data))
    r11 = data[r1][rand_.randrange(0, len(data[r1]))]
    r12 = r11
    while r11 == r12:
        r12 = data[r1][rand_.randrange(0, len(data[r1]))]
    redirect(URL('default', 'difflet', vars={'e1': r11, 'e2': r12} ))

def difflet():
    e1, e2 = request.vars['e1'],request.vars['e2']
    e1 = "india"
    e2 = "indonesia"
    e1, e2 = e1.lower(), e2.lower()
    #e1id=(db(db.thing.name==e1).select())[0]['id']
    #e2id=(db(db.thing.name==e2).select())[0]['id']

    """
    q1 = (db.listings.thing == db.thing.id) & (db.listings.point == db.point.id) & (db.listings.description == db.description.id) & (db.thing.name == e1)
    q2 = (db.listings.thing == db.thing.id) & (db.listings.point == db.point.id) & (db.listings.description == db.description.id) & (db.thing.name == e2)

    e1rows = db(q1).select(db.point.property, db.description.body, db.point.id)
    e2rows = db(q2).select(db.point.property, db.description.body, db.point.id)
    #e2rows = db(db.listing.entity==e2id).select(join = db.diff_point.on(db.listing.diff_point == db.diff_point.id))


    #if not e1rows: # populate e1rows


    e1_dp_id = []
    for i in range(0, len(e1rows)):
        e1_dp_id.append(e1rows[i]['point']['id'])
        #e1_dp_id.append(e1rows[i]['diff_point.id'] )
    e2_dp_id = []
    for i in range(0, len(e2rows)):
        e2_dp_id.append(e2rows[i]['point']['id'])
        #e2_dp_id.append(e2rows[i]['diff_point.id'] )

    # {  diff_point : (e1, e2)}
    common=[]
    for i in e1_dp_id:
        if i in e2_dp_id:
            common.append(i)
    output={}

    for r in e1rows:
        if r['point']['id'] in common:
            output[r['point']['property']] = (r['description']['body'] , '')

    for r in e2rows:
        if r['point']['id'] in common:
            old_tuple = output[r['point']['property']]
            output[r['point']['property']] = (old_tuple[0], r['description']['body'])
#        if r['diff_point.id'] in common:
#            old_tuple = output[r['diff_point.name']]
#            output[r['diff_point.name']] =  ( old_tuple[0],  r['listing.summary'])
    saveSearch(e1, e2)
    """

    diffvideo = request.vars['v'] == '2'
    from searchpy import getdata
    indexpath = request.folder + "private/index"
    one = getdata(indexpath, e1)
    two = getdata(indexpath, e2)
    common=[]
    e1_dp_id = sorted(one.keys())
    e2_dp_id = sorted(two.keys())
    for i in e1_dp_id:
        if i in e2_dp_id:
            common.append(i)
    output={}
    output = {}
    for k,v in one.items() :
        if k in common:
            output[k] = (v, '')
    for k,v in two.items() :
        if k in common:
            old_tuple = output[k]
            output[k] = (old_tuple[0], v)

    if diffvideo == True:
        from ytSearchpy import find_video
        urls = find_video(e1, e2)
        print "URLS>>>>>>>>>>>>>>>"
        print urls
        v1url = urls[0][1]
        v2url = urls[1][1]

    return locals()


def create():
    e = request.args[0]
    if e == 'category':
        category = SQLFORM(db.category).process()
    if e == 'thing':
        thing = SQLFORM(db.thing).process()
    if e == 'point':
        point = SQLFORM(db.point).process()
    if e == 'description':
        description = SQLFORM(db.description).process()
    if e == 'listing':
        listing = SQLFORM(db.listings).process()
    if e == 'recent':
        recent = SQLFORM(db.recents).process()
    if e == 'popular':
        popular = SQLFORM(db.popular).process()
    return locals()

def managething():
    thing = SQLFORM.smartgrid(db.thing)
    return locals()

def manage():
    e = request.args(0)
    if e == 'category' or e is None:
        #category = SQLFORM.grid(db.category)
        category = SQLFORM.smartgrid(db.category)
    if e == 'thing' or e is None:
        thing = SQLFORM.smartgrid(db.thing)
    if e == 'point' or e is None:
        point = SQLFORM.smartgrid(db.point)
    if e == 'description' or e is None:
        description = SQLFORM.smartgrid(db.description)
    if e == 'listing' or e is None:
        listing = SQLFORM.smartgrid(db.listings)
    if e == 'recent' or e is None:
        recent = SQLFORM.smartgrid(db.recents)
    if e == 'popular' or e is None:
        popular = SQLFORM.smartgrid(db.popular)
    return locals()


def template():
    response.view = 'default/difflet_template.html'
    return locals()




def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

def about():
    return locals()


@cache.action()
def download():
    """]
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename
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



def html():
    from diffpy import getCheck
    a=getCheck(6)
    print a
    return locals()
