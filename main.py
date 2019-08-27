#!/usr/bin/env python3

from FYN import app 

def launch():
    fl =app.run(host="0.0.0.0")
    return fl

if __name__ == '__main__':
    launch()
