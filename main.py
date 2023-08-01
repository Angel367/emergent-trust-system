import random
import csv


class Agent:
    def __init__(self, agent_id, name="baseName", reputation=0.50):
        self.ID = agent_id
        self.name = name
        self.reputation = reputation  # от 0 до 1
        self.trustScores = []  # from 0 to 1 for every score
        self.interactions = []

    def __str__(self):
        return self.ID.__str__() + "." + self.name

    def get_ID(self):
        return self.ID

    def set_ID(self, ID):
        self.ID = ID

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_reputation(self):
        return self.reputation

    def set_reputation(self, reputation):
        self.reputation = reputation

    def get_trust_scores(self):
        return self.trustScores

    def get_trust_score_by_id(self, agent_id):
        for item in self.trustScores:
            if item.get_agent2().ID == agent_id:  # or item.get_agent1().ID == agent_id:
                return item
        return None

    def add_trust_score(self, score):
        self.trustScores.append(score)

    def get_interactions(self):
        return self.interactions

    def get_interactions_by_id_count(self, agent_id):
        items = []
        for item in self.interactions:
            if item._agent2.ID == agent_id:  # or item.agent1.ID == agent_id:
                items.append(item)
        return items.__len__()

    def add_interaction(self, interaction):
        self.interactions.append(interaction)


class Interaction:
    def __init__(self, agent1, agent2, polarity, subjectivity, timestamp):
        self._agent1 = agent1
        self._agent2 = agent2
        self._sentiment = polarity  # from -1 to 1 -negative +positive
        self._interactionType = subjectivity  # from 0 to 1 = neutrality
        self._timestamp = timestamp
        agent1.add_interaction(self)
        agent2.add_interaction(self)
        if not agent1.get_trust_score_by_id(agent2.ID):
            Trust(agent1, agent2, 0.5)
        self.delta_trust()

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

    def delta_trust(self):
        #  TODO осмыслить формулу для расчета доверия trust_change
        trust_change = 0.01 * self.get_sentiment() * \
                       self.get_interaction_type() * self._agent1.reputation
        trust = self._agent1.get_trust_score_by_id(agent_id=self._agent2.ID)
        print(trust_change, trust.get_score(), self._agent1, self._agent2)
        if 0 < trust.get_score() + trust_change < 1:
            trust.set_score(trust.get_score() + trust_change)


class Trust:
    def __init__(self, agent1, agent2, score=0.5):
        self._agent1 = agent1
        self._agent2 = agent2
        self._score = score
        if not agent1.get_trust_score_by_id(agent_id=agent2.ID):
            print("Added ", agent1, "~", agent2)
            agent1.add_trust_score(self)

    def __str__(self):
        return self._agent1.__str__() + "~" + self._agent2.__str__() + ":" \
            + self._score.__str__()

    # def __len__(self):
    #     return int(self._score * 10)

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
    def calculate_for_i_j(agent_i, agent_j, agents):
        trust_score = agent_i.get_trust_score_by_id(agent_id=agent_j.ID).get_score()
        interaction_count = agent_i.get_interactions_by_id_count(agent_id=agent_j.ID)
        sum = 0
        for x in agents:
            for y in agents:
                if not x.ID == y.ID:
                    if not x.get_interactions_by_id_count(agent_id=y.ID) == 0:
                        # print(sum, x, y)
                        sum = x.get_interactions_by_id_count(agent_id=y.ID) * \
                              x.get_trust_score_by_id(agent_id=y.ID).get_score()
        # print(sum, "sum")
        return trust_score * interaction_count / sum
        # TODO протестировать правильность работы ЕД для I,J
        # (InteractionCount(i, j) * TrustScore(i, j)) / Sum(InteractionCount(x, y) * TrustScore(x, y))
        # Perform trust calculation based on available data and return the result
        # (Implementation left to your specific requirements)
        pass
    # TODO sum of all em_tr_for_i_j and div by their count
    @staticmethod
    def calculate_average(agents):
        sum, count = 0, 0
        for a1 in agents:
            for a2 in agents:
                if not a1 == a2:
                    sum += EmergentTrust.calculate_for_i_j(a1, a2, agents)
                    count += 1
        return sum / count
#
# from dostoevsky.tokenization import RegexTokenizer
# from dostoevsky.models import FastTextSocialNetworkModel
#
# tokenizer = RegexTokenizer()
# tokens = tokenizer.split('всё очень плохо')  # [('всё', None), ('очень', None), ('плохо', None)]
#
# model = FastTextSocialNetworkModel(tokenizer=tokenizer)
#
#
# messages = [
#     'Сегодня хорошая погода',
#     'Я счастлив проводить с тобою время',
#     'Мне нравится эта музыкальная композиция',
#     'В больнице была ужасная очередь',
#     'Сосед с верхнего этажа мешает спать',
#     'Маленькая девочка потерялась в торговом центре',
# ]
#
# results = model.predict(messages, k=6)
#
# for message, sentiment in zip(messages, results):
#     # привет -> {'speech': 1.0000100135803223, 'skip': 0.0020607432816177607}
#     # люблю тебя!! -> {'positive': 0.9886782765388489, 'skip': 0.005394937004894018}
#     # малолетние дебилы -> {'negative': 0.9525841474533081, 'neutral': 0.13661839067935944}]
#     print(message, '->', sentiment)
#
#
# def generate_data_from_kt():
#     # generate agents (A...Z)
#     import csv
#     agents_data = [
#         {"ID": 1, "name": "A", "reputation": 0.50},
#         {"ID": 2, "name": "B", "reputation": 0.50}
#     ]
#     fieldnames = ["ID", "name", "reputation"]
#     with open('agents.csv', 'w', newline='') as csvfile:
#         csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         csv_writer.writeheader()
#         csv_writer.writerows(agents_data)
#
#
#
#
# def read_agents_from_csv(filename="agents.csv"):
#     agents = []
#     with open(filename, newline='') as csvfile:
#         csv_reader = csv.DictReader(csvfile)
#         for row in csv_reader:
#             ID = int(row['ID'])
#             name = row['name']
#             reputation = float(row['reputation'])
#             agent = Agent(agent_id=ID, name=name, reputation=reputation)
#             agents.append(agent)
#
#     for agent in agents:
#         print(f"ID: {agent.ID}, Name: {agent.name}, Reputation: {agent.reputation}")
#
#     return agents
#
#
#
#
# with open('kt.csv', newline='', encoding='utf8') as csvfile:
#
#     csv_reader = csv.reader(csvfile)
#
#     for row in csv_reader:
#         # 0 - id отзыва
#         # 1 - содержимое (rus)
#         # 3 - оценка (good, bad, neutral)
#         #print(row[3])
#         pass
