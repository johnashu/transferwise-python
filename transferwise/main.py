# Routine to find the best rates.. A new transfer wil be created and the old one deleted.

import uuid
import time
from transferwise_api import TransferWiseApi
from config import *
from setup_rates import data
from logga import _logger

log = _logger("info")

lines = "-" * 200


class TransferWise(TransferWiseApi):

    def __init__(self, **kw):
        for k, v in kw.items():
            exec(f'self.{k} = kw["{k}"]')

        self.t = {"targetAmount": self.TARGET_AMOUNT}
        self.s = {"sourceAmount": self.SOURCE_AMOUNT}

        self._RATES = RATES.format(self.FROM, self.TO)

    def display_start_message(self):
        log.info(f"\nPolling Started...   Checking Every {self.DELAY} seconds\n")
        if self.HIGHEST_RATE:
            log.info(
                f"""\t**START** self.HIGHEST_RATE  ::  {self.HIGHEST_RATE}\n\tAmount in {self.FROM}  ::  {self.SOURCE_AMOUNT} \n\tConversion to {self.TO}  ::  {self.HIGHEST_RATE*(self.SOURCE_AMOUNT-self.FEE):0.5f}\n\tself.FEE  =  {self.FEE}"""
            )

    def display_rate_info(self, rate):
        log.debug(
            f"""
    \tNew Rate  ::      {rate}
    \tHighest Rate  ::  {self.HIGHEST_RATE}
    """
        )

        log.info(lines)

        log.info(
            f"""
    \tNEW HIGH RATE!!! BUY BUY BUY!! ... :: {rate}
    \tAmount {self.SOURCE_AMOUNT} in {self.FROM}  ::  Conversion to {self.TO} = {rate*(self.SOURCE_AMOUNT-self.FEE):0.5f}
    \tYou have gained {self.TO}  ::  {(rate*(self.SOURCE_AMOUNT-self.FEE))-(self.HIGHEST_RATE*(self.SOURCE_AMOUNT-self.FEE)):0.5f}
    """
        )

    def get_rate(self):
        # get current rates for currency selected above
        try:
            r, c = self.connect_to_api(
                "payload", _get=True, URL=BASE_URL, ENDPOINT=self._RATES
            )
            rate = c[0]["rate"]
        except TypeError:
            rate = False
        return rate

    def get_quote(self):
        # Quote Payload base
        quote_payload = {
            "profile": profileId,
            "source": self.FROM,
            "target": self.TO,
            "rateType": "FIXED",
            "type": "REGULAR",
        }
        # Add Target or source amounts depending on above
        quote_payload.update(self.s if self.SOURCE_AMOUNT else self.t)

        # request the quote
        quote_res, quote = self.connect_to_api(
            quote_payload, _post=True, URL=BASE_URL, ENDPOINT=QUOTE
        )
        log.debug(f"Quote  ::  {quote_res}")
        return quote_res, quote

    def create_transfer(self, quote):
        transfer = {
            "targetAccount": TARGET_ACCOUNT,
            "quote": quote["id"],
            "customerTransactionId": str(uuid.uuid1()),
            "details": {
                "reference": self.REFERENCE,
                "transferPurpose": "verification.transfers.purpose.pay.bills",
                "sourceOfFunds": "verification.source.of.funds.other",
            },
        }
        # add transfer
        transfer_res, transfer_json = self.connect_to_api(
            transfer, _post=True, URL=BASE_URL, ENDPOINT=TRANSFERS
        )

        log.debug(f"Transfer  Result  ::  {transfer_res}")
        log.debug(transfer_json)

        return transfer_res, transfer_json

    def cancel_order(self, transfer_json):
        cancel_res, cancel = self.connect_to_api(
            "payload",
            _put=True,
            URL=BASE_URL,
            ENDPOINT=CANCEL_TRANSFER.format(self.HIGHEST_TRANSFER_ID),
        )
        log.debug(
            f"Cancel Status Code  ::  {cancel_res}  ::   Cancel  Result  ::  {cancel}"
        )

        if cancel_res == 200:
            # Change highest transfer id
            log.info(f"\tTRANSFER CANCELLED  ::  {self.HIGHEST_TRANSFER_ID}")

            self.HIGHEST_TRANSFER_ID = transfer_json["id"]

            log.info(
                f"\t*NEW* self.HIGHEST_TRANSFER_ID  ::  {self.HIGHEST_TRANSFER_ID}"
            )
        else:
            log.error(
                f"\tProblem with Cancelling a TRANSFER:\tresponse code  ::  {cancel_res}\tMessage  ::  {cancel}"
            )

    def long_polling(self):
        while True:
            rate = self.get_rate()
            # Check if current rate is more than the starting exchange rate.
            if rate and (rate > self.HIGHEST_RATE):
                self.display_rate_info(rate)
                # Step 1: Create a quote
                quote_res, quote = self.get_quote()

                if quote_res == 200:
                    # Step 3: Create a transfer
                    transfer_res, transfer_json = self.create_transfer(quote)

                    if transfer_res == 200:
                        # Change highest rate to rate
                        self.HIGHEST_RATE = rate

                        # Cancel old transfer
                        if self.HIGHEST_TRANSFER_ID:
                            self.cancel_order(transfer_json)

                        else:
                            # set new HIGHEST_TRANSFER_ID.
                            self.HIGHEST_TRANSFER_ID = transfer_json["id"]
                            log.info(
                                f"\t**FIRST** self.HIGHEST_TRANSFER_ID  ::  {self.HIGHEST_TRANSFER_ID}"
                            )
                    else:
                        log.error(
                            f"\tProblem with creating a TRANSFER:\tresponse code  ::  {transfer_res}\tMessage  ::  {transfer_json}"
                        )
                else:
                    log.error(
                        f"\tProblem with creating a QUOTE:\tresponse code  ::  {quote_res}\tMessage  ::  {quote}"
                    )

            time.sleep(self.DELAY)


if __name__ == "__main__":
    tw = TransferWise(**data)
    tw.display_start_message()
    tw.long_polling()
