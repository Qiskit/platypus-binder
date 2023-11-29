import numpy as np
import time
import datetime
from qiskit.providers.jobstatus import JobStatus

import pickle
 
def save_object(obj, filename):
    try:
        save_name = filename +".picke"
        print(save_name)
        with open(save_name, "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)

def load_object(filename):
    try:
        save_name = filename +".picke"
        with open(save_name, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)

def check_job_status(job, filename):
    
    # Calculate the total number of seconds
    total_seconds = 4000
    update_seconds = 4
    timer = datetime.timedelta(seconds = total_seconds)
    print(timer, end="\r")
 
    while total_seconds > 0:

        time.sleep(update_seconds)
        total_seconds -= update_seconds
        timer = datetime.timedelta(seconds = total_seconds)
        print(timer, end="\r")
        
        status = job.status()
        if status == JobStatus.DONE:
            # print("in loop")
            # Build the CHSH witnesses
            values = job.result().values
            save_object(values, filename)
            break
        
        # print(job.status())
    else:
        values = load_object(filename)
            
    return values
    
