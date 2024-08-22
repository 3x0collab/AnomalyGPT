

import os
import sys
from django.conf import settings
import numpy as np
from sqlalchemy import text, create_engine
import pandas as pd

path = os.getcwd()
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

user = settings.USER
pwd = settings.PASSWORD
host = settings.HOST
port = settings.PORT
db = settings.DB

url = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"
cursor = create_engine(url, echo=False)

accountId = 41871
schemeId = 'D2'
