import random



class Agent:
    def __init__(self, agent_id):
        self._ID = agent_id
        self.name = "baseName"
        self._reputation = 0
        self._trustScores = random.randint(0, 100)
        self._interactions = []

    def get_ID(self):
        return self._ID

    def set_ID(self, ID):
        self._ID = ID

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_reputation(self):
        return self._reputation

    def set_reputation(self, reputation):
        self._reputation = reputation

    def get_trust_scores(self):
        return self._trustScores

    def add_trust_score(self, agent_id, score):
        self._trustScores[agent_id] = score

    def get_interactions(self):
        return self._interactions

    def add_interaction(self, interaction):
        self._interactions.append(interaction)


class Interaction:
    def __init__(self, agent1, agent2, polarity, subjectivity, timestamp):
        self._agent1 = agent1
        self._agent2 = agent2
        self._sentiment = polarity  # from -1 to 1
        self._interactionType = subjectivity  # from 0 to 1
        self._timestamp = timestamp

    def get_agent1(self):
        return self._agent1

    def get_agent2(self):
        return self._agent2

    def get_sentiment(self):
        return self._sentiment

    def get_interaction_type(self):
        return self._interactionType

    def get_timestamp(self):
        return self._timestamp


class EmergentTrust:
    @staticmethod
    def calculate_trust(agent):
        trust_scores = agent.get_trust_scores()
        interactions = agent.get_interactions()

        # Perform trust calculation based on available data and return the result
        # (Implementation left to your specific requirements)
        pass


from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

tokenizer = RegexTokenizer()
tokens = tokenizer.split('всё очень плохо')  # [('всё', None), ('очень', None), ('плохо', None)]

model = FastTextSocialNetworkModel(tokenizer=tokenizer)


messages = [
    'Сегодня хорошая погода',
    'Я счастлив проводить с тобою время',
    'Мне нравится эта музыкальная композиция',
    'В больнице была ужасная очередь',
    'Сосед с верхнего этажа мешает спать',
    'Маленькая девочка потерялась в торговом центре',
]

results = model.predict(messages, k=6)

for message, sentiment in zip(messages, results):
    # привет -> {'speech': 1.0000100135803223, 'skip': 0.0020607432816177607}
    # люблю тебя!! -> {'positive': 0.9886782765388489, 'skip': 0.005394937004894018}
    # малолетние дебилы -> {'negative': 0.9525841474533081, 'neutral': 0.13661839067935944}]
    print(message, '->', sentiment)