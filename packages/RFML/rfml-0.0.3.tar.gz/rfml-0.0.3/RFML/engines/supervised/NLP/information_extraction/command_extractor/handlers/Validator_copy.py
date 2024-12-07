# import re
#
# from RFML.interface.IPromptValidator import IPromptValidator
# from RFML.libs.utils import rf
# from RFML.prompt.PromptCash import PromptCash
# from RFML.prompt.PromptQuery import PromptQuery
#
#
# class Validator(IPromptValidator):
#     # configure prompt_queries for validation check
#     def configure_prompt_queries(self, prompt_query_list: list[PromptQuery]):
#         prompt_query_list.append(
#             PromptQuery("FLIGHT", {
#                 "Q1": "Could you specify the transport type?",
#                 "Q2": "Please specify the transport"
#             })
#         )
#         prompt_query_list.append(
#             PromptQuery("SOURCE", {
#                 "Q1": "Could you specify the source location?",
#                 "Q2": "Please mention source location."
#             })
#         )
#         prompt_query_list.append(
#             PromptQuery("DESTINATION", {
#                 "Q1": "Could you specify the destination location?",
#                 "Q2": "Please mention destination location."
#             })
#         )
#         prompt_query_list.append(
#             PromptQuery("DATE", {
#                 "Q1": "Could you specify the journey date?",
#                 "Q2": "Please mention the the journey date."
#             })
#         )
#         prompt_query_list.append(
#             PromptQuery("TIME", {
#                 "Q1": "Could you specify the journey time?",
#                 "Q2": "Please mention the the journey time."
#             })
#         )
#
#         # prompt_query_list.append(
#         #     PromptQuery("room", {
#         #         "Q1": "Could you specify the room name?",
#         #         "Q2": "Which room would like to book?"
#         #     })
#         # )
#         # prompt_query_list.append(
#         #     PromptQuery("start", {
#         #         "Q1": "When should I book the room?",
#         #         "Q2": "At what time meeting should be book?",
#         #         "Q3": "When?",
#         #         "Q4": "What is the start time?"
#         #     })
#         # )
#         # prompt_query_list.append(
#         #     PromptQuery("end", {
#         #         "Q1": "When should I close the room?",
#         #         "Q2": "At what time meeting should be closed?",
#         #         "Q3": "When to close?",
#         #         "Q4": "What is the end time?"
#         #     })
#         # )
#
#     # process input and store in prompt_queries for validation check
#     def process_prompt_queries(self, pc: PromptCash, user_input: str):
#         if pc:
#             if pc.missing_validator_attribute == "SOURCE":
#                 pc.validator_cash["SOURCE"] = user_input.replace(' to', '')
#                 val = pc.validator_cash
#             elif pc.missing_validator_attribute == "DESTINATION":
#                 pc.validator_cash["DESTINATION"] = user_input.replace(' to', '')
#             elif pc.missing_validator_attribute == "DATE":
#                 pc.validator_cash["DATE"] = rf.datetime.regex_extract(user_input)
#             elif pc.missing_validator_attribute == "TIME":
#                 pc.validator_cash["TIME"] = user_input
#
#     def format_prompt_queries(self, pc: PromptCash, user_input: str):
#         msg = f"Please book a flight from {pc.validator_cash['SOURCE']} to " \
#               f"{pc.validator_cash['DESTINATION']} on {pc.validator_cash['DATE']} at " \
#               f"{pc.validator_cash['TIME']}."
#         return msg
