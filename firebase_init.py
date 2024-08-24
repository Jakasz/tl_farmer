from creds import Creds
from datetime import date
import firebase_admin
from firebase_admin import credentials, db
from getmac import get_mac_address

class Fb:
    
    def init_and_check(self):
        creds = Creds()
        mac = get_mac_address()
        firebase = credentials.Certificate(creds.credentials)
        firebase_admin.initialize_app(firebase, {'databaseURL': 'https://tl-farmer-default-rtdb.europe-west1.firebasedatabase.app/'})      
        ref = db.reference('/')  
       
                
        curr_data = ref.child(creds.serial).child(str(mac.upper())).get()              
        try:
            can_access = curr_data['canAccess']
        except:
            can_access = "empty"    
        if(can_access=="empty"):            
            ref.child(creds.serial).child(str(mac).upper()).set({"mac": f"{mac.upper()}", "date_regiter":f"{str(date.today())}", "canAccess":True})           
        
        return can_access
        