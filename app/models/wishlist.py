""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re
from datetime import datetime

NAME_REGEX = re.compile(r'^[a-zA-Z0-9,. ]{3,240}$') # Name requires at least 3 chars, allows letters/numbers/basic punctuation, upper limit of 240
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9]{3,240}$') # Name requires at least 3 chars, allows letters/numbers, upper limit of 240
ITEM_REGEX = re.compile(r'^[a-zA-Z0-9,. \-]{3,240}$') # Item requires at least 3 chars, allows letters/numbers/basic punctuation, upper limit of 240
PW_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
DATE_REGEX = re.compile(r'(^(((0[1-9]|1[012])[\/-](0[1-9]|1[0-9]|2[0-8]))|((0[13578]|1[02])[\/-](29|30|31))|((0[469]|11)[\/-](29|30)))[\/-](19|[2-9][0-9])\d\d$)|(^02[\/-]29[\/-]((0[048]|1[26]|2[048]|3[26]|4[048])(0[048]|1[26]|2[048]|3[26]|4[048]|5[26]|6[048]|7[26]|8[048]|9[26])$))|((0[1235679]|1[1345789]|2[1235679]|3[01345789]|4[1235679])(0[48]|1[26]|2[048]|3[26]|4[048]|5[26]|6[048]|7[26]|8[048]|9[26])$)')

class wishlist(Model):
    def __init__(self):
        super(wishlist, self).__init__()

    def login(self, args):
        error = []
        logingood = True
        username = args['username'].strip()
        data = { 'username': username }
        query = "SELECT users.username, users.password FROM users WHERE users.username = :username"
        check = self.db.query_db(query, data)
        if(check):
            if self.bcrypt.check_password_hash(check[0]['password'], args['password']):
                return (logingood, check)
            else:
                logingood = False
                error.append("Invalid username or password.")
            pass
        else:
            logingood = False
            error.append("That username does not exist, you must first register it if you want to use it.")
        return (logingood, error)
    
    def getUserInfoFromUsername(self, newusername):
        username = newusername.strip()
        data = { 'username': username }
        query = "SELECT users.username, users.name, users.id, users.created_at, users.date_hired FROM users WHERE users.username = :username"
        return self.db.query_db(query, data)

    def register(self, args):
        error = []
        name = args['name'].strip()
        username = args['username'].strip()
        data = { 'username': username }
        registergood = True
        # print args
        if(self.db.query_db("SELECT users.username FROM users WHERE users.username = :username", data)):
            registergood = False
            error.append("Username already exists in database!  Use a different one!")
            return (registergood,error)
        if not USERNAME_REGEX.match(username):
            registergood = False
            error.append("Username must be between 3 and 240 chars long, cannot contain anything but letters or numbers")
        if not NAME_REGEX.match(name):
            registergood = False
            error.append("Name must be between 3 and 240 chars long, cannot contain anything but letters, numbers, commas, spaces or periods")
        if not PW_REGEX.match(args['password']):
            registergood = False
            error.append("Password must be at least 8 characters long, and contain at least one letter and number.")
        elif args['password'] != args['Confirm Password']:
            registergood = False
            error.append("Password must match password Confirmation")
        daytocheck = datetime.strptime(args['date_hired'],'%Y-%m-%d')
        daytocheck = datetime.strftime(daytocheck, '%m-%d-%Y')
        if not DATE_REGEX.match(daytocheck):
            registergood = False
            error.append("That hired date doesn't exist!")
        if registergood:
            query = "INSERT INTO users (name, username, password, date_hired, created_at, updated_at) VALUES (:name, :username, :password, :date_hired, NOW(), NOW())"
            hashedPW = self.bcrypt.generate_password_hash(args['password'])
            data = {'name':name,'username':username,'password':hashedPW,'date_hired':args['date_hired']}
            self.db.query_db(query,data)
        return (registergood,error)

    def getFaves(self, newuserid):
        query = "SELECT items.name as item_name, items.id as item_id, users2.name as added_by_name, users2.id as added_by_id, items.created_at as date_added FROM users LEFT JOIN users_has_items ON users_has_items.user_id = users.id LEFT JOIN items ON users_has_items.item_id = items.id LEFT JOIN users as users2 ON users2.id = items.user_id WHERE users.id = :id AND items.name is not null"
        data = {'id':newuserid}
        return self.db.query_db(query,data)

    def getOthers(self, newuserid):
        query = "SELECT items.name as item_name, items.id as item_id, users.name as added_by_name, users.id as added_by_id, items.created_at as date_added FROM users LEFT JOIN items ON users.id = items.user_id WHERE items.name is not null AND NOT items.id IN(SELECT items.id FROM users LEFT JOIN users_has_items ON users_has_items.user_id = users.id LEFT JOIN items ON users_has_items.item_id = items.id WHERE users.id = :id and items.name is not null)"
        data = {'id':newuserid}
        return self.db.query_db(query,data)

    def addToList(self, newitemid, newuserid):
        query = "INSERT INTO users_has_items (user_id, item_id, created_at, updated_at) VALUES (:userid, :itemid, NOW(), NOW())"
        data = {'userid':newuserid,'itemid':newitemid}
        return self.db.query_db(query,data)

    def deleteFromList(self, newitemid, newuserid):
        query = "DELETE FROM users_has_items WHERE users_has_items.user_id = :userid AND users_has_items.item_id = :itemid"
        data = {'userid':newuserid,'itemid':newitemid}
        return self.db.query_db(query,data)

    def deleteInFull(self, newitemid):
        query = "DELETE FROM users_has_items WHERE users_has_items.item_id = :itemid"
        data = {'itemid':newitemid}
        self.db.query_db(query,data)
        query = "DELETE FROM items WHERE items.id = :itemid"
        return self.db.query_db(query,data)

    def getItemInfo(self, newitemid):
        query = "SELECT items.name as item_name, users.name as user_name FROM items LEFT JOIN users_has_items ON users_has_items.item_id = items.id LEFT JOIN users ON users_has_items.user_id = users.id WHERE items.id = :itemid"
        data = {'itemid':newitemid}
        return self.db.query_db(query,data)

    def addNewItem(self, args, newuserid):
        error = []
        addgood = True
        item = args['item'].strip()
        if ITEM_REGEX.match(item):
            query = "SELECT items.name FROM items WHERE items.name = :name"
            data = {'name':item}
            check = self.db.query_db(query,data)
            if check:
                addgood = False;
                error.append("Can only add unique item/descriptions to the list!")
            else:
                query = "INSERT INTO items (name, user_id, created_at, updated_at) VALUES (:name, :userid, NOW(), NOW())"
                data = {'name':item,'userid':newuserid}
                self.db.query_db(query,data)
                query = "SELECT items.id FROM items WHERE items.name = :name"
                data = {'name':item}
                newid = self.db.query_db(query,data)
                query = "INSERT INTO users_has_items (user_id, item_id, created_at, updated_at) VALUES (:userid, :itemid, NOW(), NOW())"
                data = {'userid':newuserid,'itemid':int(newid[0]['id'])}
                self.db.query_db(query,data)
        else:
            addgood = False;
            error.append("Item name/description must be between 3 and 240 chars long, cannot contain anything but letters, numbers, spaces, dashes, commas or periods")
        return (addgood, error)
    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """