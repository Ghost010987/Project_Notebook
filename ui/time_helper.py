# Below function requires datetime module hence imported
from datetime import datetime

# Function defination to get current date & time. 
def get_current_timestamp():
    now = datetime.now()

# iso format its the international standard format.
    iso_format = now.isoformat()  
     
    return iso_format




    
