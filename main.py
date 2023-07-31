import random


class Agent:

    def __init__(self, agent_id):
        self._ID = agent_id
        self._reputation = random.random  # interval
        self._trustScores = []  # БЫЛО random.randint(0, 100)   TODO это массив по идее
        # однако я думаю что это отдельная сущность характеризующ отношения между агентами
        # and what interval
        self._interactions = []

    def get_ID(self):
        return self._ID

    def get_reputation(self):
        return self._reputation

    def set_reputation(self, reputation):
        self._reputation = reputation

    def get_trust_scores(self):
        return self._trustScores

    def get_trust_score_by_id(self, agent_id):
        for item in self._trustScores:
            if item.agent2 == agent_id:
                return item.score
            else:
                return None

    def add_trust_score(self, score):
        self._trustScores.append(score)

    def get_interactions(self):
        return self._interactions

    def get_interactions_by_id(self, agent_id):
        items = []
        for item in self._interactions:
            if item.agent2 == agent_id or item.agent1 == agent_id:
                items.append(item)
        return items

    def add_interaction(self, interaction):
        self._interactions.append(interaction)


class Interaction:
    def __init__(self, agent1, agent2, polarity, subjectivity, timestamp):
        self._agent1 = agent1
        self._agent2 = agent2
        self._sentiment = polarity                  # from -1 to 1 -negative +positive
        self._interactionType = subjectivity        # from 0 to 1 = neutrality
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


class Trust:
    def __init__(self, agent1, agent2, score):
        self._agent1 = agent1
        self._agent2 = agent2
        self._score = score

    def get_agent1(self):
        return self._agent1

    def get_agent2(self):
        return self._agent2

    def get_score(self):
        return self._score

    def set_score(self, score):
        self._score = score


class EmergentTrust:
    @staticmethod
    def calculate_trust(agent_i, agent_j, agents):
        trust_score = agent_i.get_trust_score_by_id(agent_id=agent_j)
        interaction_count = agent_i.get_interactions_by_id(agent_id=agent_j).count()
        sum = 0
        for x in agents:
            for y in agents:
                if not x == y:
                    sum = x.get_interactions_by_id(agent_id=y).count() * \
                          x.get_trust_score_by_id(agent_id=y)
        sum /= 2
        return trust_score * interaction_count / sum
        # (InteractionCount(i, j) * TrustScore(i, j)) / Sum(InteractionCount(x, y) * TrustScore(x, y))
        # Perform trust calculation based on available data and return the result
        # (Implementation left to your specific requirements)
        pass

