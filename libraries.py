import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlsxwriter
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import base64
from selenium.common.exceptions import NoSuchElementException
import sys
import os
from threading import Thread
import requests
import ttkbootstrap as tb
from tkinter import messagebox
import subprocess
from create_excel import create_excel_file
from create_html_table import modify_html_table
from emailBody import generate_email_body, image1_base64, image2_base64
from dotenv import load_dotenv
load_dotenv()

