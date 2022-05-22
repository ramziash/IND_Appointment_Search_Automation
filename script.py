import json
from common_utilities.api.api_call import RESTAPI
from datetime import datetime

rest = RESTAPI()
# DH for Den Haag
result = rest.api_call(method='GET', url="https://oap.ind.nl/oap/api/desks/DH/slots/?productKey=DOC&persons=1")
schedule = json.loads(result[5:])['data']

add_days = [(datetime.strptime(x['date'], '%Y-%m-%d').strftime('%A'), x) for x in schedule[:10]]

start = datetime.strptime("2022-06-08", "%Y-%m-%d")
date_generated = pd.date_range(start, periods=30)
date_required=date_generated.strftime("%Y-%m-%d")

# Choose the dates you want the automation to look for
#date_required = ['2022-03-30', '2022-04-04', '2022-04-06']

if any(datee in str(add_days) for datee in date_required):
    print('Option Available')

    # Hold the appointment
    choose = rest.api_call(method='POST', url=f"https://oap.ind.nl/oap/api/desks/DH/slots/{schedule[0]['key']}",
                           data=json.dumps(schedule[0]))
    print(choose)

    if "OK" in str(choose):

        # Make the booking
        body = {
            "bookableSlot": {**schedule[0],
                             "booked": 'false'},
            "appointment":
            {"productKey": "DOC", **schedule[0],
             "email": "--", "phone": "--", "language": "nl",
             "customers": [{"vNumber": "--", "firstName": "--", "lastName": "--"}]}}
        body['appointment'].pop('key')
        body['appointment'].pop('parts')

        book = rest.api_call(method='POST', url="https://oap.ind.nl/oap/api/desks/DH/appointments/",
                             data=json.dumps(body))
        print(book)
    else:
        print('retry holding the booking')
else:
    print('Not Available, soonest available is:')
    print(add_days[:2])
