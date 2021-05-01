import smtplib

import requests

gmail_user = 'user@gmail.com'
gmail_password = 'hshhhfd' #add app password and not login for (slightly) better security
sent_from = 'user@gmail.com'
subject = 'Vaccination Slots available for 18+'


def send_email(emails, body):
    to = emails
    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print('Email sent!')
    except:
        print('Something went wrong...')


def get_appointment_data(date, district_id):
    appointment_api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + str(
        district_id) + "&date=" + str(date)
    appointment_api_resp = requests.get(appointment_api).json()
    centers = appointment_api_resp['centers']
    # print(json.dumps(centers))
    result_data = []
    found = False
    for center in centers:
        for session in center['sessions']:
            if session['min_age_limit'] < 45 and session['available_capacity'] > 0:
                # print(json.dumps(session))
                found = True
                data = {'name': center['name'], 'date': session['date'], 'vaccine': session['vaccine'],
                        'available_capacity': session['available_capacity']}
                result_data.append(data)
    if found:
        return result_data
    else:
        return []
