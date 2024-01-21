import csv
import dataclasses
from pathlib import Path
from typing import NamedTuple

from vector import Vector
from spaceship import Spaceship


@dataclasses.dataclass
class Data:
    index: int
    result: str
    ship1_strategy: str
    ship2_strategy: str

    ship1_position: Vector
    ship2_position: Vector
    ship1_direction: Vector
    ship2_direction: Vector

    ship1_position_x: float
    ship1_position_y: float
    ship1_position_z: float
    ship2_position_x: float
    ship2_position_y: float
    ship2_position_z: float

    ship1_direction_x: float
    ship1_direction_y: float
    ship1_direction_z: float
    ship2_direction_x: float
    ship2_direction_y: float
    ship2_direction_z: float

    ship_distance: float
    ship1_angle_to_enemy: float
    ship2_angle_to_enemy: float


class Simulation:
    def __init__(
        self,
        ship1: Spaceship,
        ship2: Spaceship,
        ticks: int = 100,
    ) -> None:
        self.ship1 = ship1
        self.ship2 = ship2

        self.ship1.enemy = self.ship2
        self.ship2.enemy = self.ship1

        self.initial_settings = {
            "ship1": {
                "direction": self.ship1.direction,
                "position": self.ship1.position,
                "speed": self.ship1.speed,
                "turning_speed": self.ship1.turning_speed,
                "weapon_angle_degrees": self.ship1.weapon_angle_degrees,
                "weapon_range": self.ship1.weapon_range,
            },
            "ship2": {
                "direction": self.ship2.direction,
                "position": self.ship2.position,
                "speed": self.ship2.speed,
                "turning_speed": self.ship2.turning_speed,
                "weapon_angle_degrees": self.ship2.weapon_angle_degrees,
                "weapon_range": self.ship2.weapon_range,
            }
        }

        self.data: list[Data] = []

        # Do the sim
        for index in range(ticks):
            ship1_win = self.ship1.is_enemy_in_weapon_range()
            ship2_win = self.ship2.is_enemy_in_weapon_range()

            if ship1_win and ship2_win:
                result = "BOTH_DESTROYED"
            elif ship1_win:
                result = "SHIP_1_WINS"
            elif ship2_win:
                result = "SHIP_2_WINS"
            else:
                result = "ONGOING"

            data = Data(
                index=index,
                result=result,
                
                ship1_strategy = self.ship1.strategy,
                ship2_strategy = self.ship2.strategy,

                ship1_position=self.ship1.position,
                ship2_position=self.ship2.position,
                ship1_direction=self.ship1.direction,
                ship2_direction=self.ship2.direction,

                ship1_position_x = self.ship1.position.x,
                ship1_position_y = self.ship1.position.y,
                ship1_position_z = self.ship1.position.z,
                ship2_position_x = self.ship2.position.x,
                ship2_position_y = self.ship2.position.y,
                ship2_position_z = self.ship2.position.z,

                ship1_direction_x = self.ship1.direction.x,
                ship1_direction_y = self.ship1.direction.y,
                ship1_direction_z = self.ship1.direction.z,
                ship2_direction_x = self.ship2.direction.x,
                ship2_direction_y = self.ship2.direction.y,
                ship2_direction_z = self.ship2.direction.z,

                ship_distance = self.ship1.distance_to_enemy(),
                ship1_angle_to_enemy = self.ship1.angle_to_enemy_degree(),
                ship2_angle_to_enemy = self.ship2.angle_to_enemy_degree(),
            )
            self.data.append(data)
            
            if result != "ONGOING":
                break
            
            ship1_pos = self.ship1.position
            ship1_dir = self.ship1.direction

            ship2_pos = self.ship2.position
            ship2_dir = self.ship2.direction

            self.ship1.move(
                enemy_position=ship2_pos,
                enemy_direction=ship2_dir,
            )
            self.ship2.move(
                enemy_position=ship1_pos,
                enemy_direction=ship1_dir,
            )

    def summary(self) -> str:
        rv = ""
        rv += f"RESULT: {self.data[-1].result}\n"
        rv += f"TICKS: {len(self.data)}"

        for ship, dict_ in self.initial_settings.items():
            rv += f"\n{ship} initial:\n"
            rv += "\n".join([
                f"  {key}: {value}"
                for key, value
                in dict_.items()
            ])
        return rv

    def to_csv(self, path: Path):
        data = [
            dataclasses.asdict(entry)
            for entry
            in self.data
        ]
        with open(path, "w", encoding="utf8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            for row in data:
                row.pop("ship1_position")
                row.pop("ship2_position")
                row.pop("ship1_direction")
                row.pop("ship2_direction")
                writer.writerow(row)


if __name__ == "__main__":
    ship1 = Spaceship(position=Vector(0,0,0), direction=Vector(0,1,0))
    ship2 = Spaceship(position=Vector(200,200,200), direction=Vector(-1,0,0))

    sim = Simulation(ship1, ship2, 1000)
    # print(sim.data)

    sim.to_csv(Path("./data.csv"))

    for entry in sim.data:
        print(f"-----------------")
        print(f"INDEX: {entry.index} {entry.result}")
        # print(f"1: {entry.ship1_position_} @ {entry.ship1_direction} {entry.ship1_strategy}")
        # print(f"2: {entry.ship2_position} @ {entry.ship2_direction} {entry.ship2_strategy}")
        print(f"dist: {entry.ship_distance}  angle1: {entry.ship1_angle_to_enemy}  angle2: {entry.ship2_angle_to_enemy}")

    ship1_x = [entry.ship1_position_x for entry in sim.data]
    ship1_y = [entry.ship1_position_y for entry in sim.data]
    ship1_z = [entry.ship1_position_z for entry in sim.data]

    ship2_x = [entry.ship2_position_x for entry in sim.data]
    ship2_y = [entry.ship2_position_y for entry in sim.data]
    ship2_z = [entry.ship2_position_z for entry in sim.data]

    max_coord = -1e30
    min_coord = 1e30
    for list_ in [
        ship1_x,
        ship1_y,
        ship1_z,
        ship2_x,
        ship2_y,
        ship2_z,
    ]:
        for item in list_:
            if item < min_coord:
                min_coord = item
            if item > max_coord:
                max_coord = item

    ship1_strategy = [entry.ship1_strategy.replace("-", "\n") for entry in sim.data]
    ship2_strategy = [entry.ship2_strategy.replace("-", "\n") for entry in sim.data]
    ship1_angle = [entry.ship1_angle_to_enemy for entry in sim.data]
    ship2_angle = [entry.ship2_angle_to_enemy for entry in sim.data]
    distance = [entry.ship_distance for entry in sim.data]

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.axes3d import Axes3D
    from mpl_toolkits.mplot3d.axes3d import Axes
    ax_strat= plt.axes(projection="3d")
    ax_strat: Axes3D
    ax_strat.plot(ship1_x, ship1_y, ship1_z, label="ship1")
    ax_strat.scatter(ship1_x, ship1_y, ship1_z, label="ship1")
    ax_strat.plot(ship2_x, ship2_y, ship2_z, label="ship2")
    ax_strat.scatter(ship2_x, ship2_y, ship2_z, label="ship2")
    ax_strat.legend()
    ax_strat.set_xlabel("x")
    ax_strat.set_ylabel("y")
    ax_strat.set_zlabel("z")
    # ax_strat.set_xlim(min_coord, max_coord)
    # ax_strat.set_ylim(min_coord, max_coord)
    # ax_strat.set_zlim(min_coord, max_coord)
    plt.show()
    print(ax_strat.__class__.__module__)
    print(ax_strat.__class__.__qualname__)
    print(sim.ship1.speed)
    print(sim.ship2.speed)

    fig, [[ax_strat, ax_distance], [ax_angle, ax4]] = plt.subplots(2,2)
    ax_strat: Axes
    ax_distance: Axes
    ax_angle: Axes
    ax4: Axes
    
    
    ax_strat.plot(ship1_strategy, label="ship1")
    ax_strat.plot(ship2_strategy, label="ship2")
    ax_strat.legend()
    ax_strat.set_title("Strategy")
    ax_strat.set_xlabel("Tick")
    
    ax_distance.plot(distance)
    ax_distance.set_title("Ship separation")
    ax_distance.set_xlabel("Tick")
    
    ax_angle.plot(ship1_angle, label="ship1")
    ax_angle.plot(ship2_angle, label="ship2")
    ax_angle.legend()
    ax_angle.set_title("Angle to enemy ship (deg)")
    ax_angle.set_xlabel("Tick")

    ax4.set_title("Parameters")
    ax4.text(0.1, 0.1, sim.summary())

    plt.show()
    print(sim.summary())