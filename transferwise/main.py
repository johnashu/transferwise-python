# Routine to find the best rates.. A new transfer wil be created and the old one deleted.

import uuid
import time
from transferwise_api import TransferWiseApi
from config import *
from setup_rates import *
import logging as log

# Set Log configurations
log.basicConfig(
    format="%(asctime)s  ::  [%(levelname)s]  ::  %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    filename="rates.log",
    filemode="a",
    level=log.INFO,
)

logger = log.getLogger()
handler = log.StreamHandler()
logger.addHandler(handler)

t = {"targetAmount": TARGET_AMOUNT}
s = {"sourceAmount": SOURCE_AMOUNT}

RATES = RATES.format(FROM, TO)
tw = TransferWiseApi(TOKEN)

# Long Polling
log.info(f"\nPolling Started...\tChecking Every {DELAY} seconds\n")
if HIGHEST_RATE:
    log.info(
        f"""\t**START** HIGHEST_RATE  ::  {HIGHEST_RATE}\n\tAmount in {FROM}  ::  {SOURCE_AMOUNT} \n\tConversion to {TO}  ::  {HIGHEST_RATE*(SOURCE_AMOUNT-FEE):0.5f}\n\tFEE  =  {FEE}"""
    )
lines = "-" * 200
while True:
    # get current rates for currency selected above
    r, c = tw.connect_to_api("payload", _get=True, URL=BASE_URL, ENDPOINT=RATES)
    rate = c[0]["rate"]

    log.debug(f"\tNew Rate  ::      {rate}")
    log.debug(f"\tHighest Rate  ::  {HIGHEST_RATE}")
    # check if current rate is more than the starting exchange rate
    if rate > HIGHEST_RATE:
        log.info(lines)
        log.info(f"\tNEW HIGH RATE!!! BUY BUY BUY!! ... :: {rate}")
        log.info(
            f"\tAmount {SOURCE_AMOUNT} in {FROM}  ::  Conversion to {TO} = {rate*(SOURCE_AMOUNT-FEE):0.5f}"
        )
        log.info(
            f"\tYou have gained {TO}  ::  {(rate*(SOURCE_AMOUNT-FEE))-(HIGHEST_RATE*(SOURCE_AMOUNT-FEE)):0.5f}"
        )
        # Step 1: Create a quote
        # Quote Payload base
        quote_payload = {
            "profile": profileId,
            "source": FROM,
            "target": TO,
            "rateType": "FIXED",
            "type": "REGULAR",
        }
        # Add Target or source amounts depending on above
        quote_payload.update(s if SOURCE_AMOUNT else t)
        # request the quote
        quote_res, quote = tw.connect_to_api(
            quote_payload, _post=True, URL=BASE_URL, ENDPOINT=QUOTE
        )
        log.debug(f"Quote  ::  {quote_res}")

        if quote_res == 200:
            # Step 3: Create a transfer
            transfer = {
                "targetAccount": TARGET_ACCOUNT,
                "quote": quote["id"],
                "customerTransactionId": str(uuid.uuid1()),
                "details": {
                    "reference": REFERENCE,
                    "transferPurpose": "verification.transfers.purpose.pay.bills",
                    "sourceOfFunds": "verification.source.of.funds.other",
                },
            }
            # add transfer
            transfer_res, transfer_json = tw.connect_to_api(
                transfer, _post=True, URL=BASE_URL, ENDPOINT=TRANSFERS
            )
            log.debug(f"Transfer  Result  ::  {transfer_res}")
            log.debug(transfer_json)

            if transfer_res == 200:
                # Change highest rate to rate
                HIGHEST_RATE = rate

                # Cancel old transfer
                if HIGHEST_TRANSFER_ID:

                    CANCEL_TRANSFER_URL = CANCEL_TRANSFER.format(HIGHEST_TRANSFER_ID)

                    cancel_res, cancel = tw.connect_to_api(
                        "payload", _put=True, URL=BASE_URL, ENDPOINT=CANCEL_TRANSFER_URL
                    )
                    log.debug(
                        f"Cancel Status Code  ::  {cancel_res}  ::   Cancel  Result  ::  {cancel}"
                    )

                    if cancel_res == 200:
                        # Change highest transfer id
                        log.info(f"\tTRANSFER CANCELLED  ::  {HIGHEST_TRANSFER_ID}")
                        HIGHEST_TRANSFER_ID = transfer_json["id"]
                        log.info(
                            f"\t*NEW* HIGHEST_TRANSFER_ID  ::  {HIGHEST_TRANSFER_ID}"
                        )
                    else:
                        log.error(
                            f"\tProblem with Cancelling a TRANSFER:\t{BASE_URL+CANCEL_TRANSFER_URL}\tresponse code  ::  {cancel_res}\tMessage  ::  {cancel}"
                        )
                else:
                    HIGHEST_TRANSFER_ID = transfer_json["id"]
                    log.info(
                        f"\t**FIRST** HIGHEST_TRANSFER_ID  ::  {HIGHEST_TRANSFER_ID}"
                    )
            else:
                log.error(
                    f"\tProblem with creating a TRANSFER:\tresponse code  ::  {transfer_res}\tMessage  ::  {transfer}"
                )
        else:
            log.error(
                f"\tProblem with creating a QUOTE:\tresponse code  ::  {quote_res}\tMessage  ::  {quote}"
            )

    time.sleep(DELAY)
