# from RFML.interface.IPromptValidator import IPromptValidator
# from RFML.prompt.PromptCash import PromptCash
# from RFML.prompt.PromptQuery import PromptQuery
#
#
# class Validator(IPromptValidator):
#     # configure prompt_queries for validation check
#     def configure_prompt_queries(self, prompt_queries_list: list[PromptQuery]):
#         prompt_queries_list.append(PromptQuery("room", {
#             "Q1": "Could you specify the room name?",
#             "Q2": "Which room would like to book"
#         }))
#         prompt_queries_list.append(PromptQuery("start_time", {
#             "Q1": "When should I book the room?",
#             "Q2": "At what time meeting should be book?",
#             "Q3": "When?",
#             "Q4": "What is the start time?"
#         }))
#
#     # process input and store in prompt_queries for validation check
#     def process_prompt_queries(self, pc: PromptCash, user_input: str):
#         if pc.last_prompt_query == "Q1" & pc.last_attribute == "room":
#             form = user_input.split(' ')[0]
#             to = user_input.split(' ')[1]
#             pc.validator_cash["asdas"] = form  # update hard cash
#             pc.validator_cash["to"] = to
#
#         elif pc.last_prompt_query == "Q1" & pc.last_attribute == "from":
#             form = user_input.split(' ')[0]
#             pc.validator_cash["from"] = form
#
#         return f"Book the room from {pc.validator_cash['from']}"
