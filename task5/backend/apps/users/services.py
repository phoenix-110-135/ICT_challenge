import random
import requests 
from decouple import config
def generate_otp():

    return str(
        random.randint(
            100000,
            999999
        )
    )


def send_sms(phone_number, code):
    try:
        data = {'bodyId': config('BODY_ID'), 'to': f'{phone_number}', 'args': [f'{code}']}
        response = requests.post('https://console.melipayamak.com/api/send/shared/86216f4b127b45d9964cf7a8beba5fb4', json=data)
        print(

            f"\notp for {phone_number} == {code}\n\n\n{response.json()}"
        )

        return True
    except:
        return False