from flask import render_template , jsonify , abort # type: ignore
from data import get_data , Enrollment_logs
from resizeimage import resizeimage  # type: ignore
from pymongo import MongoClient # type: ignore
from flask_caching import Cache # type: ignore
from flask import request # type: ignore
from PIL import Image # type: ignore
from functions import *
from flask_cors import CORS # type: ignore
from flask import * # type: ignore
import random 
import glob
from datetime import datetime ,timezone
import timeago # type: ignore
from time import time
import csv
import os
import re
import requests
from bson import ObjectId # type: ignore
from flask_mail import Mail ,  Message # type: ignore
import smtplib
from flask_socketio import SocketIO, emit , send , Namespace #type: ignore
import uuid
import razorpay