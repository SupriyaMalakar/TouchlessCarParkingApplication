# -*- coding: utf-8 -*-
"""
Created on Mon May  4 00:10:30 2020

@author: SupriyaMalakar
"""
import os
from CarParkingApp import app

if __name__ == '__main__':
    
    osPort = os.getenv("PORT")
    if osPort == None:
        port = 5020
    else:
        port = int(osPort)
    app.run(host='0.0.0.0', port=port)
    
    
    #app.run(debug=True)