import uuid
import time
from transferwise_api import TransferWiseApi
from config import *

tw = TransferWiseApi(TOKEN)

HIGHEST_RATE = 1.09940

SOURCE_AMOUNT = 6000
TARGET_AMOUNT = None

t = {"targetAmount": TARGET_AMOUNT}
s = {"sourceAmount": SOURCE_AMOUNT}

FROM = "GBP"
TO = "EUR"
RATES = RATES.format(FROM, TO)

REFERENCE = "Bills-Programmatically"

HIGHEST_TRANSFER_ID = 0

# Long Polling
while True:
    # get current rates for currency selectede above
    r, c = tw.connect_to_api("payload", _get=True, URL=BASE_URL, ENDPOINT=RATES)
    rate = c[0]["rate"]
    # check if current rate is more than the starting exchange rate
    if rate > HIGHEST_RATE:
        print(f"NEW HIGH RATE!!! BUY BUY BUY!! Etc.... :: {rate}")
        # Step 1: Create a quote
        # Quote Payload base
        quote_payload = {
            "profile": profile,
            "source": "GBP",
            "target": "EUR",
            "rateType": "FIXED",
            "type": "REGULAR",
        }
        # Add Target or source amounts depending on above
        quote_payload.update(s if SOURCE_AMOUNT else t)
        # request the quote
        res, quote = tw.connect_to_api(
            quote_payload, _post=True, URL=BASE_URL, ENDPOINT=QUOTE
        )
        print("Quote  :: ", res)

        if res == 200:
            # Step 3: Create a transfer
            transfer = {
                "targetAccount": 7533897,  # rabo personal
                "quote": quote["id"],
                "customerTransactionId": str(uuid.uuid1()),
                "details": {
                    "reference": REFERENCE,
                    "transferPurpose": "verification.transfers.purpose.pay.bills",
                    "sourceOfFunds": "verification.source.of.funds.other",
                },
            }
            # add transfer
            res, transfer = tw.connect_to_api(
                transfer, _post=True, URL=BASE_URL, ENDPOINT=TRANSFERS
            )
            print(res, transfer)

            if res == 200:
                # Change highest rate to rate
                HIGHEST_RATE = rate

                # Cancel old transfer
                CANCEL_TRANSFER = CANCEL_TRANSFER.format(HIGHEST_TRANSFER_ID)
                res, cancel = tw.connect_to_api(
                    "payload", _put=True, URL=BASE_URL, ENDPOINT=CANCEL_TRANSFER
                )
                print(res, cancel)

                if res == 200:
                    # C change highest transfer id
                    HIGHEST_TRANSFER_ID = transfer["id"]
                    print(HIGHEST_TRANSFER_ID)
                else:
                    print(
                        f"\n\tProblem with Cancelling a TRANSFER:\n\tresponse code  ::  {res}\n\tMessage  ::  {cancel}\n"
                    )
            else:
                print(
                    f"\n\tProblem with creating a TRANSFER:\n\tresponse code  ::  {res}\n\tMessage  ::  {transfer}\n"
                )
        else:
            print(
                f"\n\tProblem with creating a QUOTE:\n\tresponse code  ::  {res}\n\tMessage  ::  {quote}\n"
            )

    time.sleep(5)
