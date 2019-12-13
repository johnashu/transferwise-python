BASE_URL = "https://api.transferwise.com/v1/"
PROFILE = "profiles"
RATES = "rates?source={}&target={}"
QUOTE = "quotes"
LIST_RECIPIENTS = "accounts?profile={}&currency={}"
TRANSFERS = "transfers"
CANCEL_TRANSFER = "transfers/{}/cancel"

TOKEN = ""

HEADER = {"Authorization": "Bearer" + TOKEN, "Content-Type": "application/json"}

profileId = ""

# bank account id to fund.
TARGET_ACCOUNT = 999999999
