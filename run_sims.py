from collections import Counter
import random
from vector import Vector
from spaceship import Spaceship
from simulation import Simulation

SIM_COUNT = 100
MAX_DISTNACE = 1000.0
random.seed(40351)

results = []
initial_distance = []
initial_ship1_angle = []
initial_ship2_angle = []
simulation_length = []
result_counter = Counter()

for sim_number in range(SIM_COUNT):
    ship1 = Spaceship(
        position=Vector.random_direction() * MAX_DISTNACE,
        direction=Vector.random_direction(),
    )
    ship2 = Spaceship(
        # position=Vector(random.random() * 500.0, 0.0, 0.0),
        position=Vector.random_direction() * MAX_DISTNACE,
        direction=Vector.random_direction(),
    )
    sim = Simulation(ship1, ship2, ticks=10_000)
    print(len(sim.data), sim.data[-1].result)

    results.append(sim.data[-1].result)
    initial_distance.append(sim.data[0].ship_distance)
    initial_ship1_angle.append(sim.data[0].ship1_angle_to_enemy)
    initial_ship2_angle.append(sim.data[0].ship2_angle_to_enemy)
    simulation_length.append(len(sim.data))
    result_counter[sim.data[-1].result] += 1

import matplotlib.pyplot as plt
# plt.scatter(initial_distance, results)

fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2)
ax1: plt.Axes
ax2: plt.Axes
ax3: plt.Axes
ax4: plt.Axes

ax1.scatter(initial_distance, results)
ax1.set_title(f"Initial distance")
ax1.set_xlabel(f"Results by initial distance")
ax1.set_ylabel(f"Result")

ax2.scatter(simulation_length, results)
ax2.set_title(f"Simulation length (ticks)")
ax2.set_xlabel(f"Results by Simulation length")
ax2.set_ylabel(f"Result")

ax3.scatter(initial_distance, simulation_length)
ax3.set_title(f"Simulation length by initial distance")
ax3.set_xlabel(f"Initial distance")
ax3.set_ylabel(f"Length (ticks)")


ax4.bar(result_counter.keys(), result_counter.values())
ax4.set_title(f"Total result counts")
ax4.set_xlabel(f"Result")
ax4.set_ylabel(f"Count")


plt.show()











# # sim = sim

# for entry in sim.data:
#     print(f"-----------------")
#     print(f"INDEX: {entry.index} {entry.result}")
#     # print(f"1: {entry.ship1_position_} @ {entry.ship1_direction} {entry.ship1_strategy}")
#     # print(f"2: {entry.ship2_position} @ {entry.ship2_direction} {entry.ship2_strategy}")
#     print(f"dist: {entry.ship_distance}  angle1: {entry.ship1_angle_to_enemy}  angle2: {entry.ship2_angle_to_enemy}")

# ship1_x = [entry.ship1_position_x for entry in sim.data]
# ship1_y = [entry.ship1_position_y for entry in sim.data]
# ship1_z = [entry.ship1_position_z for entry in sim.data]

# ship2_x = [entry.ship2_position_x for entry in sim.data]
# ship2_y = [entry.ship2_position_y for entry in sim.data]
# ship2_z = [entry.ship2_position_z for entry in sim.data]

# max_coord = -1e30
# min_coord = 1e30
# for list_ in [
#     ship1_x,
#     ship1_y,
#     ship1_z,
#     ship2_x,
#     ship2_y,
#     ship2_z,
# ]:
#     for item in list_:
#         if item < min_coord:
#             min_coord = item
#         if item > max_coord:
#             max_coord = item

# ship1_strategy = [entry.ship1_strategy.replace("-", "\n") for entry in sim.data]
# ship2_strategy = [entry.ship2_strategy.replace("-", "\n") for entry in sim.data]
# ship1_angle = [entry.ship1_angle_to_enemy for entry in sim.data]
# ship2_angle = [entry.ship2_angle_to_enemy for entry in sim.data]
# distance = [entry.ship_distance for entry in sim.data]

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d.axes3d import Axes3D
# from mpl_toolkits.mplot3d.axes3d import Axes
# ax_strat= plt.axes(projection="3d")
# ax_strat: Axes3D
# ax_strat.plot(ship1_x, ship1_y, ship1_z, label="ship1")
# ax_strat.scatter(ship1_x, ship1_y, ship1_z, label="ship1")
# ax_strat.plot(ship2_x, ship2_y, ship2_z, label="ship2")
# ax_strat.scatter(ship2_x, ship2_y, ship2_z, label="ship2")
# ax_strat.legend()
# ax_strat.set_xlabel("x")
# ax_strat.set_ylabel("y")
# ax_strat.set_zlabel("z")
# # ax_strat.set_xlim(min_coord, max_coord)
# # ax_strat.set_ylim(min_coord, max_coord)
# # ax_strat.set_zlim(min_coord, max_coord)
# plt.show()
# print(ax_strat.__class__.__module__)
# print(ax_strat.__class__.__qualname__)
# print(sim.ship1.speed)
# print(sim.ship2.speed)

# fig, [[ax_strat, ax_distance], [ax_angle, ax4]] = plt.subplots(2,2)
# ax_strat: Axes
# ax_distance: Axes
# ax_angle: Axes
# ax4: Axes


# ax_strat.plot(ship1_strategy, label="ship1")
# ax_strat.plot(ship2_strategy, label="ship2")
# ax_strat.legend()
# ax_strat.set_title("Strategy")
# ax_strat.set_xlabel("Tick")

# ax_distance.plot(distance)
# ax_distance.set_title("Ship separation")
# ax_distance.set_xlabel("Tick")

# ax_angle.plot(ship1_angle, label="ship1")
# ax_angle.plot(ship2_angle, label="ship2")
# ax_angle.legend()
# ax_angle.set_title("Angle to enemy ship (deg)")
# ax_angle.set_xlabel("Tick")

# ax4.set_title("Parameters")
# ax4.text(0.1, 0.1, sim.summary())

# plt.show()
# print(sim.summary())