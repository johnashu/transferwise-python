# Fill in this information and rename to config.py..

BASE_URL = "https://api.transferwise.com/v1/"
PROFILE = "profiles"
RATES = "rates?source={}&target={}"
QUOTE = "quotes"
LIST_RECIPIENTS = "accounts?profile={}&currency={}"
TRANSFERS = "transfers"
CANCEL_TRANSFER = "transfers/{}/cancel"

TOKEN = ""

HEADER = {"Authorization": "Bearer" + TOKEN, "Content-Type": "application/json"}


# use the procure_information.py to obtain these details
# Profile id of transferwise
profileId = ""
# bank account to fund.
TARGET_ACCOUNT = 9999999999
