# Sample TRAIN_DATA in spaCy 3.0+ format
        # TRAIN_DATA = [
        #     (
        #         "Please book a flight from New York to London on October 30, 2024 at 10:00 AM.",
        #         {"entities": [(14, 20, "FLIGHT"), (26, 34, "SOURCE"), (38, 44, "DESTINATION"), (48, 64, "DATE"), (68, 76, "TIME")]}
        #     ),
        #     (
        #         "Please book a flight from Joypurhat to London on October 30, 2024 at 10:00 AM.",
        #         {"entities": [(14, 20, "FLIGHT"), (26, 35, "SOURCE"), (38, 44, "DESTINATION"), (48, 64, "DATE"), (68, 76, "TIME")]}
        #     ),
        #     # (
        #     #     "Can you book a flight from Los Angeles to Paris on November 15 at 8:30 PM?",
        #     #     {"entities": [(23, 34, "SOURCE"), (38, 43, "DESTINATION"), (47, 58, "DATE"), (62, 70, "TIME")]}
        #     # ),
        #     # Add more examples here
        # ]
        # ner_map = {
        #     "entities": [
        #         "(14, 20, 'FLIGHT')",
        #         "(26, 34, 'SOURCE')",
        #         "(38, 44, 'DESTINATION')",
        #         "(48, 63, 'DATE')",
        #         "(67, 75, 'TIME')"
        #     ]
        # }
        # ner_map_ = {
        #     "book": "action",
        #     "transport": "flight",
        #     "source": "New York",
        #     "destination": "London",
        #     "date": "October 30 2024",
        #     "time": "10:00 AM",
        # }
        # ner_map__ = {
        #     "text": "Please book a flight from New York to London on October 30 2024 at 10:00 AM.",
        #     "ner_map": ner_map_
        # }
        #
        # data = []
        # ner = ("Please book a flight from New York to London on October 30 2024 at 10:00 AM.", ner_map)
        # data.append(ner)

        # TRAIN_DATA = [
        #     (
        #         'Please book a flight from New York to London on October 30 2024 at 10:00 AM.',
        #         {'entities': ["(15, 20, \'FLIGHT\')", "(26, 34, \'SOURCE\')", "(38, 44, \'DESTINATION\')",
        #                       "(48, 63, \'DATE\')", "(67, 75, \'TIME\')"]}
        #     )
        # ]




#vad = 0
        # TRAIN_DATA = [
        #     (
        #         "Please book a flight from New York to London on October 30 2024 at 10:00 AM.",
        #         {
        #             "entities": [
        #                 (13, 18, "FLIGHT"),  # "New York" as ORIGIN location
        #                 (24, 32, "SOURCE"),  # "New York" as ORIGIN location
        #                 (36, 42, "DESTINATION"),  # "London" as DESTINATION location
        #                 (46, 58, "DATE"),  # "October 30 2024" as DATE
        #                 (62, 70, "TIME")  # "10:00 AM" as TIME
        #             ]
        #         }
        #     )
        # ]