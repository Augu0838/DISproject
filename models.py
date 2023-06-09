# write all your SQL queries in this file.
import os
import psycopg2
from datetime import datetime
from flask_login import UserMixin
from psycopg2 import sql


class Users(tuple, UserMixin):
    def __init__(self, user_data):
        self.userid = user_data[0]
        self.user_name = user_data[1]
        self.password = user_data[2]
        self.fav_station = user_data[3]

    def get_id(self):
       return (self.userid)
