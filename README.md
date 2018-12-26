# Mobifix

#### Main dependencies: ####
1. Python 3.5
2. Django 1.11.7
3. Django Rest Framework 3.9
### Quick Start ###
1. git clone [git@github.com:Stanislav-Rybonka/mobifix.git]
2. cd to /your_project_folder
3. cp env.example mobifix/.env
4. Create virtualenv: python3 -m venv .venv
5. Activate it: source .venv/bin/activate
6. Install project dependencies: pip install -r requirements.txt
7. Configure you interpreter in IDE (optional)
8. Load fixtures: ./manage.py loaddata services
9. Run application: ./manage.py runserver 127.0.0.1:8000
#### Related dependencies ####
1. Add Twilio data to .env:
- TWILIO_ACCOUNT_SID
- TWILIO_AUTH_TOKEN
- TWILIO_TEST_PHONE_NUMBER

More details about Twilio integration here: [https://www.twilio.com/docs/libraries/python]



