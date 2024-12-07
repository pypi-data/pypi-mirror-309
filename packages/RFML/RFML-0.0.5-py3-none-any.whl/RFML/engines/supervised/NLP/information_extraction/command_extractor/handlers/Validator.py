import re

from RFML.interface.IPromptValidator import IPromptValidator
from RFML.libs.utils import rf
from RFML.prompt.PromptCash import PromptCash
from RFML.prompt.PromptQuery import PromptQuery


class Validator(IPromptValidator):
    # configure prompt_queries for validation check
    def configure_prompt_queries(self, prompt_query_list: list[PromptQuery]):
        prompt_query_list.append(
            PromptQuery("Action", {
                "Q1": "Could you specify the transport type?",
                "Q2": "Please specify the transport"
            })
        )
        prompt_query_list.append(
            PromptQuery("Origin", {
                "Q1": "Could you specify the source location?",
                "Q2": "Please mention source location."
            })
        )
        prompt_query_list.append(
            PromptQuery("Destination", {
                "Q1": "Could you specify the destination location?",
                "Q2": "Please mention destination location."
            })
        )
        prompt_query_list.append(
            PromptQuery("Date", {
                "Q1": "Could you specify the journey date?",
                "Q2": "Please mention the the journey date."
            })
        )
        prompt_query_list.append(
            PromptQuery("Time", {
                "Q1": "Could you specify the journey time?",
                "Q2": "Please mention the the journey time."
            })
        )

    # process input and store in prompt_queries for validation check
    def process_prompt_queries(self, pc: PromptCash, user_input: str):
        # normalize
        if pc:
            # rf.nlp.prompt.is_cancel_text(user_input)
            if user_input == "cancel":
                pc.cancel_prompt()
            elif len(user_input) > 15:
                pc.pass_prompt()
            else:
                pc.validator_cash[pc.missing_validator_attribute] = user_input

    def format_prompt_queries(self, pc: PromptCash, user_input: str):
        # msg = f"Please book a flight from {pc.validator_cash['Origin']} to " \
        #       f"{pc.validator_cash['Destination']} on {pc.validator_cash['Date']} at " \
        #       f"{pc.validator_cash['Time']}."
        msg = ""

        # normalize
        # if pc.not_passed(pc.validator_cash['Origin']):
        #     msg += f"Please book a flight from {pc.validator_cash['Origin']} to "

        if pc.validator_cash['Origin'] != "__passed__":
            msg += f"Please book a flight from {pc.validator_cash['Origin']} to "
        if pc.validator_cash['Destination'] != "__passed__":
            msg += f"{pc.validator_cash['Destination']} on "
        if pc.validator_cash['Date'] != "__passed__":
            msg += f"{pc.validator_cash['Date']} at "
        if pc.validator_cash['Time'] != "__passed__":
            msg += f"{pc.validator_cash['Time']}."
        return msg
