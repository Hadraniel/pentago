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
import sys
import names
import random


def nextPowerOf2(n):
    count = 0

    if n and not (n & (n - 1)):
        return n

    while n != 0:
        n >>= 1
        count += 1

    return 1 << count


def gather_agents():
    agent_dict = {
        "RandomAgent": RandomAgent,
        "BuildAgent": BuildAgent,
        "BuildAndDenyAgent": BuildAndDenyAgent,
        "AdjacentAgent": AdjacentAgent,
    }
    all_agents = []
    with open("agents.txt", "r") as f:
        for line in f:
            # getting specifications of each agent (e.g. agent type, name, id)
            strat, name, id = line.split(" ")
            agent = agent_dict[strat](name=name, id=id)
            all_agents.append(agent)
        f.close()
    return all_agents


def check_number_of_participants(n):
    if not ((n & (n - 1) == 0) and n != 0):
        return 0
    return 1


def Log2(x):
    if x == 0:
        return False

    return int(math.log10(x) / math.log10(2))


# defining a function to return ranks (we will use this as a sorting parameter)
def sort_by_rank(agent):
    return agent.rank


# checking if the number of best of matches are odd!
def is_valid_best_of(n):
    if n % 2 == 0:
        return 0
    return 1


# checking if the number of best of matches are given!
def check_best_of_given():
    return 0 if len(sys.argv) == 1 else 1


def compete(best_of_num, agent_1, agent_2, is_final):
    output = {}
    agent_1_points = 0
    agent_2_points = 0
    for i in range(best_of_num):
        core = Pentago()
        core.add_agents(g[0], g[1])
        core.play()
        if is_final:
            display(core.winner)
        if core.winner == 1:
            agent_1_points += 1
        elif core.winner == 2:
            agent_2_points += 1
        else:
            agent_2_points += 1
    if agent_1_points > agent_2_points:
        output["winner"] = agent_1
        output["point_log"] = str(agent_1_points) + "-" + str(agent_2_points)
    elif agent_2_points > agent_1_points:
        output["winner"] = agent_2
        output["point_log"] = str(agent_2_points) + "-" + str(agent_1_points)
    else:
        output["winner"] = "draw"
        output["point_log"] = str(agent_1_points) + "-" + str(agent_2_points)
    return output


# instead of writing points separately, we do them at once in this function
def logging(
    time_log, No_of_agents_log, No_of_repetitions_log, rounds_logs, ranking_log
):
    f = open("results.txt", "w")
    f.write(time_log)
    f.write(No_of_agents_log)
    f.write(No_of_repetitions_log)
    for round in rounds_logs:
        f.write("\n" + round)
    f.write(ranking_log)
    f.close()
    os.system("results.txt")


if not (check_best_of_given()):
    print("number of best of matches is not given!")
else:
    best_of = int(sys.argv[1])
    if not (is_valid_best_of(best_of)):
        print("best of matches should be an odd number!")
    else:
        won_agents = []  # list of winner agents in each round!
        lost_agents = []  # list of lost agents in each round
        participants = []  # unMatched agents getting paired in 2 groups
        finalists = []  # for determining 3nd and 4th place !
        remaining_agents = (
            gather_agents()
        )  # list of remaining agents to compete against eachother in 1 v 1
        n = len(remaining_agents)
        # we store the number of agents for logging purpoces later on!
        number_of_agents = n
        # round is for logging purposes !
        round = 1
        # round_logs is for storing every round's log
        rounds_logs = []
        # we store the below log into rounds_logs
        round_log = None
        if not check_number_of_participants(n):
            new_n = nextPowerOf2(n)
            for i in range(new_n - n):
                agent = RandomAgent(
                    name=names.get_first_name(), id=random.randint(1, 2)
                )
                remaining_agents.append(agent)
            number_of_agents = new_n
            n = new_n
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
                    g[0].id = 1
                    g[1].id = 2
                    if level == 1:
                        result = compete(best_of, g[0], g[1], 1)
                    else:
                        result = compete(best_of, g[0], g[1], 0)
                    round_log += "    Match {id} : {player_1} vs {player_2} , ".format(
                        id=idx + 1, player_1=g[0].name, player_2=g[1].name
                    )
                    if result["winner"] == 1:
                        round_log += "Winner : {winner}, {scores} \n".format(
                            winner=g[0].name, scores=result["point_log"]
                        )
                        g[1].rank = level + 1
                        won_agents.append(g[0])
                        lost_agents.append(g[1])
                    elif result["winner"] == 2:
                        round_log += "Winner : {winner}, {scores} \n".format(
                            winner=g[1].name, scores=result["point_log"]
                        )
                        g[0].rank = level + 1
                        won_agents.append(g[1])
                        lost_agents.append(g[0])
                    else:
                        round_log += "Winner : {winner}, {scores} \n".format(
                            winner=g[1].name, scores=result["point_log"]
                        )
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
            if number_of_agents == 2:
                finalists.append(lost_agents[i])
            elif lost_agents[i].rank == 3:
                finalists.append(lost_agents[i])
            elif lost_agents[i].rank > 3:
                lost_agents[i].rank += 1
        finalists[0].id = 1
        finalists[1].id = 2
        output = compete(best_of, finalists[0], finalists[1], 0)
        if output["winner"] == 1:
            if number_of_agents == 2:
                finalists[0].rank = 1
                finalists[1].rank = 2
            else:
                finalists[0].rank = 3
                finalists[1].rank = 4
        else:
            if number_of_agents == 2:
                finalists[0].rank = 2
                finalists[1].rank = 1
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
        No_of_agents_log = "No of agents = {num} \n".format(num=number_of_agents)
        No_of_repetitions_log = "No of repetitions = {best_of} \n\n".format(
            best_of=best_of
        )

        logging(
            time_log,
            No_of_agents_log,
            No_of_repetitions_log,
            rounds_logs,
            ranking_log,
        )
