import datetime
import time
import os
import pandas as pd
from plyer import notification


if __name__ == '__main__':

    df = pd.read_excel("Quotes.xlsx")
    today = datetime.datetime.now().strftime("%d-%m")
    
    for index, item in df.iterrows():
        dt = item['Date'].strftime("%d-%m")
        if(today == dt):
            #print(item['Quote'])
            quoteFound = item['Quote']
            notification.notify(
                title = "**Quote of the day!!",
                message = quoteFound,
                app_icon = r"C:\Users\kulkarna4029\OneDrive - ARCADIS\Studies\Python\Data-Apps\Reminder App\icon.ico",
                timeout= 12            
            ) 
            time.sleep(10)
            
        else:
            pass


