import re
from flask import *
# from interface.IPrompt import IPrompt

from RFML.core.Interaction import Interaction, TaskType
from RFML.interface.IPrompt import IPrompt


class HTTPHost:
    def __init__(self, prompt: IPrompt, request_process_callback):
        app = Flask(__name__)

        @app.route("/interact/")
        def interact():
            session_id = request.headers.get("X-Session-ID")

            model = request.json['model']
            task = request.json['task']
            user_input = request.json['input']

            interaction = Interaction(
                session_id=session_id,
                model=model,
                task=task,
                user_input=user_input
            )

            prompt_in_input = prompt.on_prompt_in(interaction.input)
            interaction.input = prompt_in_input or interaction.input
            result = request_process_callback(interaction)
            prompt_in_output = prompt.on_prompt_out(result)

            return prompt_in_output  # in JSON format

        #   if __name__ == "__main__":
        app.run()

        print("HTTP Host is up and running")


class CLIHost:
    def __init__(self, prompt: IPrompt, request_process_callback):
        print("Let's chat! (type 'quit' to exit)")
        while True:
            sentence = input("You: ")  # sentence = "do you use credit cards?"
            if sentence == "quit": break

            cmd = re.search(r"rf\s(train|gen|reload)(?:\s(\S+))?", sentence)
            tasks = {"train": TaskType.Train, "gen": TaskType.Generate, "reload": TaskType.Reload}

            interaction = Interaction(
                session_id="99",
                model=cmd.group(2) if cmd else "",
                task=tasks.get(cmd.group(1) if cmd else "", TaskType.Predict),
                user_input=sentence
            )

            if prompt:
                prompt_in_input = prompt.on_prompt_in(interaction.input)
                interaction.input = prompt_in_input or interaction.input
                result = request_process_callback(interaction)
                prompt_in_output = prompt.on_prompt_out(result)
                # print(prompt_in_output)

                # interaction.input = prompt.on_prompt_in(sentence)
                # result = request_process_callback(interaction)
                # prompt.on_prompt_out(result)
            else:
                result = request_process_callback(interaction)
                print(result)

# train_cmd = re.search(r"rf\strain", sentence)
# gen_cmd = re.search(r"rf\sgen", sentence)
# reload_cmd = re.search(r"rf\sreload", sentence)

# interaction = Interaction
# if cmd.group(1) == "train":
#     toks = sentence.split(' ')
#     interaction = Interaction(session_id="", model=cmd.group(2), task=tasks.get(cmd.group(1)),
#                               user_input="")
# elif cmd.group(1) == "gen":
#     interaction = Interaction(session_id="", model="", task=TaskType.Generate, user_input="")
# elif cmd.group(1) == "reload":
#     toks = sentence.split(' ')
#     interaction = Interaction(session_id="", model=toks[2], task=TaskType.Reload, user_input="")
# else:
#     interaction = Interaction(session_id="", model="", task=TaskType.Predict, user_input="")
# interaction.session_id = "99"
