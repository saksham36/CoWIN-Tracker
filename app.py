import requests
import datetime
import json
import pandas as pd
import smtplib
from email.message import EmailMessage
import time
import os

# Rajasthan state_code = 29
# District code: 
# Jaipur I: 505
# Jaipur II: 506

DIST_IDS = {505: 'Jaipur I', 506: 'Jaipur II'}
numdays = 20
age = 23

SENDER_EMAIL = os.environ['SENDER_ID']
SENDER_PASSWORD = os.environ["SENDER_PWD"]
REC_EMAIL = os.environ["REC_ID"]


if __name__ == "__main__":

	server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
	server.login(SENDER_EMAIL, SENDER_PASSWORD)
	i = 0
	while True:
	    print(f"Checking! {i}")
	    if i % 100 == 0:
	    	server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
			server.login(SENDER_EMAIL, SENDER_PASSWORD)
		    base = datetime.datetime.today()
			date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
			date_str = [x.strftime("%d-%m-%Y") for x in date_list]
	    for DIST_ID in DIST_IDS:
	        for INP_DATE in date_str:
	    #             flag = False
	                URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(DIST_ID, INP_DATE)
	                response = requests.get(URL)
	                if response.ok:
	                    resp_json = response.json()
	                    if resp_json["centers"]:
	                            for center in resp_json["centers"]:
	                                for session in center["sessions"]:
	                                    if session["min_age_limit"] <= age:
	                                        if session["available_capacity"] > 0:   
	                                            text =  center["name"] + "\n Price:" + center["fee_type"] + "\n Available Capacity: "  + str(session["available_capacity"]) + "\nVaccine:" + session["vaccine"]
	                                            message = 'Subject: {}\n\n{}'.format("Availabie Vaccine!", text)
	                                            server.sendmail(SENDER_EMAIL, 
	                                                            REC_EMAIL, 
	                                                            message
	                                                           )
	    #                                         flag = True
	                                            print("\t", center["name"])
	                                            print("\t", center["block_name"])
	                                            print("\t Price: ", center["fee_type"])
	                                            print("\t Available Capacity: ", session["available_capacity"])
	                                            print(type(session["available_capacity"]))
	                                            if(session["vaccine"] != ''):
	                                                print("\t Vaccine: ", session["vaccine"])
	                                            print("\n\n")
	    #                 if not flag:
	    #                     print("No availability on {}".format(INP_DATE))
	    i += 1
	    time.sleep(30)
	    if i % 100 == 0:
			server.quit()

