from enum import Enum


class LearningType(Enum):
    Supervised = 0
    Unsupervised = 1
    Semi_Supervised = 2
    Reinforcement = 3


class Algorithm(Enum):
    Liner_Regression = 0


class NN(Enum):
    FFN = 0


class Intelligence(Enum):
    Understanding_Interaction = 0
    Knowledge_Discovery = 1
    Decision_Making = 2
    Generation = 3


class CognitiveSkills(Enum):
    Information_Extraction = 0
    Clustering = 0
    Classification = 0
    Conversation_and_Dialogue_Systems = 0
    Regression = 0
    Anomaly_Detection = 0
    Recommendation_Systems = 0
    Dimensionality_Reduction = 0
    Natural_Language_Processing = 0
    Speech_Recognition_and_Synthesis = 0
    Object_Detection_and_Image_Recognition = 0
    Generative_Models = 0
    Reinforcement_Learning = 0
    Time_Series_Forecasting = 0
    Transfer_Learning = 0
    Data_Generation_and_Augmentation = 0


class Meta:
    def __init__(self, learning_type, algorithm, NN, intelligence, cognitive_skills):
        self.LearningType: learning_type
        self.Algorithm: algorithm
        self.NN: NN
        self.Intelligence: intelligence
        self.CognitiveSkills: cognitive_skills
