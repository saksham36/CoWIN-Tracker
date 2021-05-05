# CoWIN-Tracker

This is a simple email service to send a mail to you when there is an open vaccination slot in India. It works with the CoWIN API by checking constantly if there is any slot available
When there is an avaibility, a mail will be sent with the details of the vaccination centre.

Currently it is set to search for spots in Jaipur I and Jaipur II. You can change this by updating the district codes. To find your district code, run the following code snippet:
```
for state_code in range(1,40):
    print("State code: ", state_code)
    response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_code))
    json_data = json.loads(response.text)
    for i in json_data["districts"]:
        print(i["district_id"],'\t', i["district_name"])
    print("\n")
```

The app checks for a vacancy every 30 seconds and will send a mail wuith the vacancy to the email specified.

<br>
Using this app is fairly simple. You can host it on a free heroku server.

**You need to initialize the config vars** to include the sender **__gmail__** username and password. Also you will have to specify the username of the recipient email. Here are the keys to be set:
```
SEBDER_ID
SENDER_PWD
REC_ID
```

You will have to allow 3rd party applications from accessing your email for the SMTP service to be granted access. TO do so, please update your settings [here]( https://www.google.com/settings/security/lesssecureapps).

Finally after hosting the app, run the following command:

`heroku ps:scale worker=1`
