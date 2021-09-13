import tensorflow_hub as hub
import numpy as np


class Embeddings:

    def __init__(self):
        self.model_path = "C:\\Users\\Administrator\\PycharmProjects\\ELearning\\graphs\\063d866c06683311b44b4992fd46003be952409c"
        self.model = hub.load(self.model_path)
        print("model loaded")

    def cosine_similarity(self, u, v):
        return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

    def get_similarity(self, doc1, doc2):
        v1 = self.model([doc1])[0]
        v2 = self.model([doc2])[0]

        cosim = self.cosine_similarity(v1, v2)
        return round(cosim, 2)
