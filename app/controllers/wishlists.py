"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *
import time

class wishlists(Controller):
    def __init__(self, action):
        super(wishlists, self).__init__(action)
        """
            This is an example of loading a model.
            Every controller has access to the load_model method.
        """
        self.load_model('wishlist')
        self.db = self._app.db

        """
        
        This is an example of a controller method that will load a view for the client 

        """
   
    def index(self):
        try:
            error = session['error']
        except:
            pass
        try:
            if session['loggedin_id'] is not None:
                faves = self.models['wishlist'].getFaves(session['loggedin_id'])
                others = self.models['wishlist'].getOthers(session['loggedin_id'])
                return self.load_view('welcomeView.html',faves=faves, others=others)
        except:
            pass
        today = time.strftime("%Y-%m-%d")
        aday = today
        name = ''
        username = ''
        regusername = ''
        error = False
        try:
            username = session['username'].strip()
        except:
            pass
        try:
            name = session['name'].strip()
            regusername = session['regusername'].strip()
            if session['date_hired'] != '':
                aday = session['date_hired']
        except:
            pass
        return self.load_view('loginView.html',aday=aday,today=today,name=name,username=username,regusername=regusername,error=error)

    def register(self):
        session.clear()
        session['name'] = request.form['name']
        session['regusername'] = request.form['username']
        session['date_hired'] = request.form['date_hired']
        print request.form
        tryreg = self.models['wishlist'].register(request.form)
        print tryreg[0]
        print 'sexytime'
        print tryreg[1]
        if not(tryreg[0]):
            session['error'] = True
            for error in tryreg[1]:
                flash(error)
        else:
            session['error'] = False
            return self.logThemIn(request.form['username'])
        return redirect('/')

    #builder@mail.com, buildstuff1
    def wishlist(self):
        session.clear()
        session['username'] = request.form['username']
        check = self.models['wishlist'].login(request.form)
        if check[0]:
            session['error'] = False
            return self.login(request.form['username'])
        else:
            session['error'] = True
            for error in check[1]:
                flash(error)
        return redirect('/')

    def login(self):
        session.clear()
        session['username'] = request.form['username']
        check = self.models['wishlist'].login(request.form)
        if check[0]:
            session['error'] = False
            return self.logThemIn(request.form['username'])
        else:
            session['error'] = True
            for error in check[1]:
                flash(error)
        return redirect('/')

    def logThemIn(self,newusername):
        getinfo = self.models['wishlist'].getUserInfoFromUsername(newusername)
        session['loggedin_username'] = getinfo[0]['username']
        session['loggedin_name'] = getinfo[0]['name']
        session['loggedin_id'] = getinfo[0]['id']
        session['loggedin_date_hired'] = getinfo[0]['date_hired']
        session['loggedin_created_at'] = getinfo[0]['created_at']
        return redirect('/')

    def addToList(self, itemid):
        self.models['wishlist'].addToList(itemid, session['loggedin_id'])
        return redirect('/')

    def deleteFromList(self, itemid):
        self.models['wishlist'].deleteFromList(itemid, session['loggedin_id'])
        return redirect('/')

    def deleteInFull(self, itemid):
        self.models['wishlist'].deleteInFull(itemid)
        return redirect('/')

    def addItemView(self):
        return self.load_view('addView.html')

    def viewItem(self, itemid):
        iteminfo = self.models['wishlist'].getItemInfo(itemid)
        return self.load_view('itemView.html', iteminfo=iteminfo)

    def addNewItem(self):
        olditemname = request.form['item']
        check = self.models['wishlist'].addNewItem(request.form, session['loggedin_id'])
        if check[0]:
            session['error'] = False
            return redirect('/')
        else:
            session['error'] = True
            for error in check[1]:
                flash(error)
            return self.load_view('addView.html', error=error, item=olditemname)

    def logout(self):
        session.clear()
        session['error'] = False
        return redirect('/')