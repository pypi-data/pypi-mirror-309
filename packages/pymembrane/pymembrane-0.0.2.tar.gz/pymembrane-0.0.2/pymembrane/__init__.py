# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 19:04:25 2023

@author: Hedi
"""

from cryptography.fernet import Fernet, InvalidToken
import json
import os
#from sys import exec_prefix

fernet = Fernet(b'HnVQRprOj83uHNI3dCX9Vt58dYjP4BcbnTYwHZ-qOz0=')
schema = __name__+'.json'