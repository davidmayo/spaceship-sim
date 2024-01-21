from typing import Literal, Union
from vector import Vector


class Spaceship:
    def __init__(
        self,
        position: Vector = Vector.zero,
        direction: Vector = Vector.plus_x,
        speed: float = 1.0,
        turning_speed: float = 10.0,
        weapon_range: float = 50.0,
        weapon_angle_degrees = 15.0,
        name: str = "",
        enemy: Union["Spaceship", None] = None,
    ) -> None:
        """_summary_

        Args:
            position (Vector, optional): _description_. Defaults to Vector.zero.
            direction (Vector, optional): _description_. Defaults to Vector.plus_x.
            speed (float, optional): Speed in UNITS PER TICK. Defaults to 1.0.
            turning_speed (float, optional): Max turn in DEGREES PER TICK. Defaults to 10.0.
            weapon_range (float, optional): Max weapon rang in UNITS. Defaults to 10.0.
            weapon_angle_degrees (float, optional): Max weapon cylindrical angle in DEGREES. Defaults to 15.0.
            name (str, optional): _description_. Defaults to "".
        """
        self.position = position
        self.direction = direction.normalized
        self.speed = speed
        self.turning_speed = turning_speed
        self.weapon_range = weapon_range
        self.weapon_angle_degrees = weapon_angle_degrees
        self.name = name
        self.enemy = enemy

        self.strategy: Literal["patrol", "evade", "chase"] = "patrol"

    def __repr__(self) -> str:
        return f"Spaceship(name={self.name!r}, position={self.position}, direction={self.direction}), speed={self.speed}, turning_speed={self.turning_speed})"

    def turn_towards(self, point: Vector) -> None:
        """Turn towards the given point, subject to turn speed limit"""
        desired_direction = point - self.position
        angle = self.direction.angle_degrees(desired_direction)
        if angle <= self.turning_speed:
            self.direction = desired_direction.normalized
        else:
            self.direction = self.direction.rotate_towards_degrees(
                desired_direction,
                self.turning_speed,
            )

    def angle_to_enemy_degree(self) -> Union[float, None]:
        """Angle from current direction to enemy position IN DEGREES"""
        if self.enemy is None:
            return None
        return self.vector_to_enemy().angle_degrees(self.direction)
    
    def vector_to_enemy(self) -> Union[Vector, None]:
        """Not normalized"""
        if self.enemy is None:
            return None
        return self.enemy.position - self.position
    
    def direction_to_enemy(self) -> Union[Vector, None]:
        """Normalized"""
        if self.enemy is None:
            return None
        return self.vector_to_enemy().normalized

    def distance_to_enemy(self) -> Union[float, None]:
        if self.enemy is None:
            return None
        return self.vector_to_enemy().magnitude()

    def choose_strategy(
        self,
        enemy_position: Vector | None = None,
        enemy_direction: Vector | None = None,
    ) -> None:
        if self.enemy is None:
            self.strategy = "patrol"
            return
        
        distance = self.distance_to_enemy()
        angle = self.angle_to_enemy_degree()
        if distance > 2.0 * self.enemy.weapon_range:
            self.strategy = "chase-distance"
        elif angle < 90.0:
            self.strategy = "chase-angle"
        else:
            self.strategy = "evade"

    def implement_strategy(
        self,
        enemy_position: Vector | None = None,
        enemy_direction: Vector | None = None,
    ) -> None:
        """Turn the ship some direction"""
        if self.strategy.startswith("patrol"):
            # Turn randomly
            self.turn_towards(Vector.random_direction)
        elif self.strategy.startswith("chase"):
            # Turn straight towards the enemy
            vector_to_enemy = enemy_position - self.position
            self.turn_towards(vector_to_enemy)
        elif self.strategy.startswith("evade"):
            # Move perpendicular to enemy direction AND vector to enemy
            # Two possible vectors:
            vector_to_enemy = enemy_position - self.position
            candidate_1 = vector_to_enemy.cross(enemy_direction)
            
            # If parallel, special case.
            # Indicated by cross product being zero
            # Just pick a random direction perpendicular to enemy direction
            # Do this by picking a random direction and crossing that with the enemy direction
            while candidate_1 == Vector.zero:
                candidate_1 = Vector.random_direction().cross(enemy_direction.direction)
            candidate_2 = -candidate_1

            
            # Choose the one that's the smallest turn. I.E., the one that
            # makes the smallest angle with the current direction
            if candidate_1.angle_degrees(self.direction) < candidate_2.angle_degrees(self.direction):
                self.turn_towards(candidate_1)
            else:
                self.turn_towards(candidate_2)
        else:
            raise ValueError(f"Invalid strategy {self.strategy!r}")

    def is_enemy_in_weapon_range(self) -> bool:
        if self.enemy is None:
            return False
        return self.is_in_weapon_range(self.enemy.position)

    def is_in_weapon_range(self, point: Vector) -> bool:
        """Point is in weapon range if the angle to it is less than the max cylindrical angle
        and the distance is less than the max weapon range"""
        vector_to_target = point - self.position
        return (
            vector_to_target.magnitude() <= self.weapon_range
            and self.direction.angle_degrees(vector_to_target) <= self.weapon_angle_degrees
        )
    
    def move(
        self,
        enemy_position: Vector | None = None,
        enemy_direction: Vector | None = None,
    ) -> None:
        """Move in the current direction of travel at the current speed,
        subject to the current strategy.
        """
        self.choose_strategy(enemy_position=enemy_position, enemy_direction=enemy_direction)
        self.implement_strategy(enemy_position=enemy_position, enemy_direction=enemy_direction)
        self.position += self.direction.normalized * self.speed

if __name__ == "__main__":
    target = Vector(0,10,0)
    slow = Spaceship(name="slow", turning_speed=5.0, speed=2.0, position=Vector(10,10,10))
    fast = Spaceship(name="fast", turning_speed=20.0, speed=1.0, position=Vector(0,0,0))
    slow.enemy = fast
    fast.enemy = slow

    print(slow)

    slow_positions: list[Vector] = []
    fast_positions: list[Vector] = []

    for tick in range(100):
        slow_positions.append(slow.position)
        fast_positions.append(fast.position)
        print(f"{tick=}  {slow.position=}  {slow.direction=}")
        slow.move()
        # slow.turn_towards(target)

        # fast.move()
        # fast.turn_towards(target)

        # target += Vector(0,1,0)

    import matplotlib.pyplot as plt
    slow_xs = [point.x for point in slow_positions]
    slow_ys = [point.y for point in slow_positions]
    slow_zs = [point.z for point in slow_positions]

    fast_xs = [point.x for point in fast_positions]
    fast_ys = [point.y for point in fast_positions]
    fast_zs = [point.z for point in fast_positions]
    plt.plot(slow_xs, slow_ys, label=f"{slow.turning_speed} deg per tick, speed={slow.speed}")
    plt.plot(fast_xs, fast_ys, label=f"{fast.turning_speed} deg per tick, speed={fast.speed}")
    plt.legend()
    plt.show()