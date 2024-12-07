import spacy

from RFML.core.Results import PredictResult, ResultType
from RFML.libs.utils import rf


# vector_data_path = rf"C:\RFMLModels"


class IEBOT:
    def __init__(self, model: str, vector_db_path: str):
        # Load the trained model
        # self.nlp = spacy.load(rf"{vector_data_path}\{model}")
        try:
            self.nlp = spacy.load(rf"{vector_db_path}\{model}")
        except Exception as e:
            print(e)

    def predict(self, sentence: str):
        # sentence = "Please book a flight from Joypurhat to London on October 30, 2024 at 10:00 AM."
        # sentence = "Please book a flight from Joypurhat to London on 11/15/2024 at 10:20 am."
        if sentence == "book" or sentence == "book a":
            msg = "Please specify what do you want to book?"
            return PredictResult(
                result_type=ResultType.do_not_understand,
                label="book",
                probability=1.0,
                message=msg
            )

        doc = self.nlp(sentence)
        # Extract and print the entities
        data = {
            "Action": "",
            "Origin": "",
            "Destination": "",
            "Date": "",
            "Time": ""
        }
        for ent in doc.ents:
            # print(f"Entity: {ent.text}, Label: {ent.label_}")
            data[ent.label_] = ent.text

        if len(doc.ents) > 0:
            return PredictResult(
                label="flight_booking",
                probability=1.0,
                message=data,
                route=""
            )
        else:
            return PredictResult(
                result_type=ResultType.do_not_understand,
                label="book",
                probability=1.0,
                message="Booking information are not clear!"
            )
