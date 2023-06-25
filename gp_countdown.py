import time
import datetime
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)

# Set the phone number that we will receive texts on and respond from.
TWILIO_NUMBER = "18338651764"

# Set the start times of the Hungarian and Belgian GPs.
HUNGARIAN_GP_START_TIME = datetime.datetime(2023, 7, 23, 15, 0, 0, 0)
BELGIAN_GP_START_TIME = datetime.datetime(2023, 8, 27, 15, 0, 0, 0)

# Set your Twilio account SID and auth token.
ACCOUNT_SID = "AC3bdbacb774a18bafcadee7de52e844bd"
AUTH_TOKEN = "442d7e43248ea72ae517fb242ab31f69"

def get_time_remaining(event_start_time):
    """Returns the time remaining until the given event."""
    now = datetime.datetime.now()
    return (event_start_time - now).total_seconds() * 1000

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Get the incoming message body
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    if "Hungarian GP" in body or "Belgian GP" in body:
        time_remaining = get_time_remaining(HUNGARIAN_GP_START_TIME)
        resp.message("The Hungarian GP starts in {} seconds.".format(time_remaining))
    else:
        resp.message("Sorry, I don't understand your request.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)