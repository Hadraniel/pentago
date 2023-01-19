from pentago import Pentago
from random_agent import RandomAgent
from build_agent import BuildAgent
from build_and_deny_agent import BuildAndDenyAgent
from adjacent_agent import AdjacentAgent
from new_game_env import display
import numpy as np
import math
from datetime import datetime
import os


def Log2(x):
    if x == 0:
        return False

    return int(math.log10(x) / math.log10(2))


# defining a function to return ranks (we will use this as a sorting parameter)
def sort_by_rank(agent):
    return agent.rank


remaining_agents = []  # list of remaining agents to compete against eachother in 1 v 1
won_agents = []  # list of winner agents in each round!
lost_agents = []  # list of lost agents in each round
participants = []  # unMatched agents getting paired in 2 groups
finalists = []  # for determining 3nd and 4th place !

with open("agents.txt", "r") as f:
    for line in f:
        # getting specifications of each agent (e.g. agent type, name, id)
        specs = line.split(" ")
        agent = eval(
            "{agent}('{name}',{id})".format(
                agent=specs[0], name=specs[1], id=int(specs[2])
            )
        )
        remaining_agents.append(agent)

n = len(remaining_agents)
# we store the number of agents for logging purpoces later on!
number_of_agents = n
# round is for logging purposes !
round = 1
# round_logs is for storing every round's log
rounds_logs = []
# we store the below log into rounds_logs
round_log = None
if not ((n & (n - 1) == 0) and n != 0):
    print("Wrong number! input should be power of 2!")
else:
    while True:
        if n == 1:
            remaining_agents[0].rank = 1
            lost_agents.append(remaining_agents[0])
            break
        else:
            round_log = "Round {round_num} :\n".format(round_num=round)
            level = Log2(n)
            participants = np.array_split(remaining_agents, n // 2)
            for idx, g in enumerate(participants):
                # for g in participants:
                g[0].id = 1
                g[1].id = 2
                core = Pentago()
                core.add_agents(g[0], g[1])
                core.play()
                # if it's final game, then show it!
                if level == 1:
                    display(core.winner)
                # setting rank to lost agents
                round_log += "    Match {id} : {player_1} vs {player_2} , ".format(
                    id=idx + 1, player_1=g[0].name, player_2=g[1].name
                )
                if core.winner == 1:
                    round_log += "Winner : {winner} \n".format(winner=g[0].name)
                    g[1].rank = level + 1
                    won_agents.append(g[0])
                    lost_agents.append(g[1])
                elif core.winner == 2:
                    round_log += "Winner : {winner} \n".format(winner=g[1].name)
                    g[0].rank = level + 1
                    won_agents.append(g[1])
                    lost_agents.append(g[0])
                elif core.winner == "draw":
                    round_log += "Winner : {winner} \n".format(winner=g[1].name)
                    g[0].rank = level + 1
                    won_agents.append(g[1])
                    lost_agents.append(g[0])

            # updating and/or resetting log parameters
            rounds_logs.append(round_log)
            round += 1
            round_log = None
            remaining_agents = won_agents.copy()
            won_agents = []
            # half of players have lost, other half have won, so we divide by 2 each time
            n = n // 2
    # this part is for determining 3rd and 4th place !
    # so we find the two agents with rank 3 and then
    # make them play against eachother !
    for i in range(len(lost_agents)):
        if lost_agents[i].rank == 3:
            finalists.append(lost_agents[i])
        elif lost_agents[i].rank > 3:
            lost_agents[i].rank += 1
    finalists[0].id = 1
    finalists[1].id = 2
    core = Pentago()
    core.add_agents(finalists[0], finalists[1])
    core.play()
    if core.winner == 1:
        finalists[0].rank = 3
        finalists[1].rank = 4
    else:
        finalists[0].rank = 4
        finalists[1].rank = 3
    for i in range(len(lost_agents)):
        if lost_agents[i].rank == 3:
            if lost_agents[i].name == finalists[0].name:
                lost_agents[i].rank = finalists[0].rank
            elif lost_agents[i].name == finalists[1].name:
                lost_agents[i].rank = finalists[1].rank

    # sort all agensts based on rank !
    lost_agents.sort(key=sort_by_rank)
    # for i in range(len(lost_agents)):
    #     print(lost_agents[i].rank)

    ranking_log = "\nRanking : \n"
    for i in range(len(lost_agents)):
        if i == 0:
            ranking_log += "    {rank}. {agent_name} (Champion!) \n".format(
                rank=lost_agents[i].rank, agent_name=lost_agents[i].name
            )
        elif i == 1:
            ranking_log += "    {rank}. {agent_name} (Second Place!) \n".format(
                rank=lost_agents[i].rank, agent_name=lost_agents[i].name
            )
        elif i == 2:
            ranking_log += "    {rank}. {agent_name} (Third Place!) \n".format(
                rank=lost_agents[i].rank, agent_name=lost_agents[i].name
            )
        else:
            ranking_log += "    {rank}. {agent_name} \n".format(
                rank=lost_agents[i].rank, agent_name=lost_agents[i].name
            )
    time_log = "PentagoTournament: {time} \n".format(
        time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )
    No_of_agents_log = "No of agents = {num} \n\n".format(num=number_of_agents)

    f = open("results.txt", "w")
    f.write(time_log)
    f.write(No_of_agents_log)
    for round in rounds_logs:
        f.write("\n" + round)
    f.write(ranking_log)
    f.close()
    os.system("results.txt")
