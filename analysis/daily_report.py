import os
import glob
from datetime import datetime
import pandas as pd




if __name__ == '__main__':
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today_time = datetime.today().strftime('%Y-%m-%d')  


