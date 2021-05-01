import datetime
import json

import requests

import function as f

req_state = "Uttar Pradesh"
req_district = "Aligarh"

state_api_response = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states').json()
# print(json.dumps(state_api_response))
states = state_api_response['states']

for state_obj in states:
    if state_obj['state_name'] == req_state:
        stateId = state_obj['state_id']
        break

district_api_response = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/' + str(stateId)).json()

districts = district_api_response['districts']

for district_obj in districts:
    if district_obj['district_name'] == req_district:
        district_ip = district_obj['district_id']
        break

date_now = datetime.datetime.now().strftime("%d-%m-%Y")
date_1week = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%d-%m-%Y")
date_2week = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime("%d-%m-%Y")

results = f.get_appointment_data(date_now, district_ip) + f.get_appointment_data(date_1week,
                                                                                 district_ip) + f.get_appointment_data(
    date_2week, district_ip)

if len(results) > 0:
    results.sort(key=lambda x: datetime.datetime.strptime(x['date'], '%d-%m-%Y'))

    body = ""
    for result in results:
        resultBody = "Date : {} -- Name: {}. Slots : {} \n"
        body = body + (
            resultBody.format(result['date'], result['name'], result['available_capacity']))

    f.send_email(['email1@email.com', 'email2@email.com'], body)
    # print(body)
