import datetime
import random
import csv
import string

# Define an Agent class to represent individual agents in the reputation system
class Agent:
    def __init__(self, agent_id, name="baseName", reputation=0.50):
        self.ID = agent_id
        self.name = name
        self.reputation = reputation  # от 0 до 1
        self.trustScores = []  # from 0 to 1 for every score
        self.interactions = []

    # Custom string representation of the Agent object
    def __str__(self):
        return self.ID.__str__() + "." + self.name

    # Getters and setters for the Agent attributes
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

    # Get the trust score of this agent for a specific other agent (by agent_id)
    def get_trust_score_by_id(self, agent_id):
        for item in self.trustScores:
            if item.get_agent2().ID == agent_id:  # or item.get_agent1().ID == agent_id:
                return item
        return None

    # Add a new trust score to this agent's list of trust scores
    def add_trust_score(self, score):
        self.trustScores.append(score)

    def get_interactions(self):
        return self.interactions

    # Get the count of interactions with a specific other agent (by agent_id)
    def get_interactions_by_id_count(self, agent_id):
        items = []
        for item in self.interactions:
            if item._agent2.ID == agent_id:  # or item.agent1.ID == agent_id:
                items.append(item)
        return items.__len__()

    # Add a new interaction to this agent's list of interactions
    def add_interaction(self, interaction):
        self.interactions.append(interaction)


# Define an Interaction class to represent interactions between two agents
class Interaction:
    def __init__(self, agent1, agent2, polarity, subjectivity, timestamp=datetime.datetime.now()):
        if not agent1 == agent2:
            self._agent1 = agent1
            self._agent2 = agent2
            self._sentiment = polarity  # from -1 to 1 - negative to positive
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

    # Calculate the change in trust score for the agent after an interaction
    def delta_trust(self):
        # TODO: Define the formula for calculating trust_change
        trust_change = 0.1 * self.get_sentiment() * self.get_interaction_type() * self._agent1.reputation
        trust = self._agent1.get_trust_score_by_id(agent_id=self._agent2.ID)
        # print(trust_change, trust.get_score(), self._agent1, self._agent2)
        if 0 < trust.get_score() + trust_change < 1:
            trust.set_score(trust.get_score() + trust_change)


# Define a Trust class to represent the trust score between two agents
class Trust:
    def __init__(self, agent1, agent2, score=0.5):
        if not agent1.get_trust_score_by_id(agent_id=agent2.ID) and not agent1 == agent2:
            self._agent1 = agent1
            self._agent2 = agent2
            self._score = score
            agent1.add_trust_score(self)

    def __str__(self):
        return self._agent1.__str__() + "~" + self._agent2.__str__() + ":" \
            + self._score.__str__()

    def get_agent1(self):
        return self._agent1

    def get_agent2(self):
        return self._agent2

    def get_score(self):
        return round(self._score, 2)

    def set_score(self, score):
        self._score = score


# Define a static class EmergentTrust to calculate the emergent trust score between two agents
class EmergentTrust:
    # Calculate the emergent trust score for agent_i and agent_j based on their interactions with all agents
    @staticmethod
    def calculate_for_i_j(agent_i, agent_j, agents):
        trust_score = agent_i.get_trust_score_by_id(agent_id=agent_j.ID)
        if trust_score:
            trust_score = trust_score.get_score()
        else:
            trust_score = 0
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
        # TODO: Test the correctness of EmergentTrust calculation for I, J

    # Calculate the average emergent trust score for all agents in the system
    @staticmethod
    def calculate_average(agents):
        sum, count = 0, 0
        for a1 in agents:
            for a2 in agents:
                if not a1 == a2:
                    sum += EmergentTrust.calculate_for_i_j(a1, a2, agents)
                    count += 1
        return sum / count
        # TODO: Test for average emergent trust


# Import libraries for sentiment analysis using dostoevsky
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

# Initialize tokenizer and model for sentiment analysis
tokenizer = RegexTokenizer()
tokens = tokenizer.split('всё очень плохо')  # [('всё', None), ('очень', None), ('плохо', None)]
model = FastTextSocialNetworkModel(tokenizer=tokenizer)


# Function to generate agents data from CSV file
def generate_agents_from_kt(n=10):
    # generate agents (A...Z)
    # import csv
    agents_data = [
        {"ID": i,
         "name": random.choice(string.ascii_letters),
         "reputation": random.random()}
        for i in range(1, n + 1)
    ]
    fieldnames = ["ID", "name", "reputation"]
    with open('input/agents.csv', 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(agents_data)


# Function to read agents data from CSV file and create Agent objects
def read_agents_from_csv(filename="input/agents.csv"):
    agents = []
    with open(filename, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            ID = int(row['ID'])
            name = row['name']
            reputation = float(row['reputation'])
            agent = Agent(agent_id=ID, name=name, reputation=reputation)
            agents.append(agent)

    # for agent in agents:
    #     print(f"ID: {agent.ID}, Name: {agent.name}, Reputation: {agent.reputation}")

    return agents


# Function to generate trust scores data from CSV file
def generate_trusts_from_kt(n):
    trust_data = [
        {"agent1_id": random.randint(1, n),
         "agent2_id": random.randint(1, n),
         "score": random.random()}
        for _ in range(n * 5)
    ]
    trust_data = [trust for trust in trust_data if not trust["agent1_id"] == trust["agent2_id"]]

    fieldnames = ["agent1_id", "agent2_id", "score"]
    with open('input/trusts.csv', 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(trust_data)


# Function to find an agent by ID in the list of agents
def find_agent_by_id(agents, id):
    for agent in agents:
        if id == agent.get_ID():
            return agent


# Function to read trust scores data from CSV file and create Trust objects
def read_trusts_from_csv(agents, filename="input/trusts.csv"):
    trusts = []
    with open(filename, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            agent1 = find_agent_by_id(agents, int(row['agent1_id']))
            agent2 = find_agent_by_id(agents, int(row['agent2_id']))
            score = float(row['score'])
            # print(agent1, agent2)
            if not agent1 == agent2 and not agent1.get_trust_score_by_id(agent2.ID):
                trust = Trust(agent1, agent2, score)
                trusts.append(trust)

    # for trust in trusts:
    #     print(f"agent1: {trust.get_agent1()}, agent2: {trust.get_agent2()}, trust_score: {trust.get_score()}")

    return trusts


# Function to read interactions data from CSV file and create Interaction objects
def read_interactions_from_csv(agents, start=0, finish=10, filename="kt.csv"):
    interactions = []
    with open('input/kt.csv', newline='', encoding='utf8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        count, index = finish - start + 1, 0
        for row in csv_reader:
            # print(index)
            if start > index:
                index += 1
                continue
            if count + start <= index:
                break
            index += 1
            agent1 = find_agent_by_id(agents, random.randint(1, agents.__len__()))
            agent2 = agent1
            while agent1 == agent2:
                agent2 = find_agent_by_id(agents, random.randint(1, agents.__len__()))
            review = [row["review"]]
            result = model.predict(review, k=6)
            interaptionType = float(result[0]['neutral'])
            sentiment = float(result[0]['positive']) - float(result[0]['negative'])
            interaction = Interaction(agent1, agent2, sentiment, interaptionType)
            interactions.append(interaction)
    print(interactions.__len__())
    # for interaction in interactions:
    #     print(f"agent1: {interaction.get_agent1()}, agent2: {interaction.get_agent2()},"
    #           f" sentiment: {interaction.get_sentiment()},"
    #           f" interactionType: {interaction.get_interaction_type()}")
    return interactions
