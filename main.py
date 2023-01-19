from pentago import Pentago
from random_agent import RandomAgent
from build_agent import BuildAgent
from build_and_deny_agent import BuildAndDenyAgent
from adjacent_agent import AdjacentAgent
from new_game_env import display


core = Pentago()
agent_1 = RandomAgent("player_1", 1)
agent_2 = RandomAgent("player_2", 2)


core.add_agents(agent_1, agent_2)
core.play()
display(core.winner)
