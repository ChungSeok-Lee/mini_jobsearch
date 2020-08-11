from background_task import background
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

from pymongo import MongoClient
import pymysql
from pymongo import MongoClient

# --예시--#
@background()
def task_hello(schedule= 10, repeat=60):
    time_tuple = time.localtime()
    time_str = time.strftime("%m/%d/%Y, %H:%M:%S", time_tuple)
    print("task ...Hello World!", time_str)

