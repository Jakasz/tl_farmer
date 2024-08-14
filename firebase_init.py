from firebase import firebase
import pyrebase
from creds import Creds
from getmac import get_mac_address
from datetime import date

class Fb:

    def init_and_check(self):
        creds = Creds()
        firebase = pyrebase.initialize_app(creds.firebaseConfig)
        db = firebase.database()
        mac = get_mac_address() 
        
        curr_data = db.child("/").child(creds.serial).child(str(mac).upper()).get()

        try:
            can_access = curr_data.val()['canAccess']
        except:
            can_access = "empty"    

        if(can_access=="empty"):              
            db.child("/").child(creds.serial).child(str(mac).upper()).set({"mac": f"{mac.upper()}", "date_regiter":f"{str(date.today())}", "canAccess":True})            
        
        return can_access


        # cred_firestore = credentials.ApplicationDefault()
        # firebase_admin.initialize_app(cred_firestore)
        # db1 = firestore.client()
    # def write_to_db(self):
    #     refw = db.reference("/")
    #     refw.update({"2":"ss"})
        