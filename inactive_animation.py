from plane import Plane


def inactive_animation(
    last_move_time: int,
    INACTIVITY_THRESHOLD: float,
    ticks: int,
    is_alternating: bool,
    last_animation_time: int,
    ANIMATION_INTERVAL: float,
    current_sprite: int,
    plane: Plane,
):
    if ticks - last_move_time > INACTIVITY_THRESHOLD * 1000:
        is_alternating = True

    if is_alternating and (ticks - last_animation_time > ANIMATION_INTERVAL * 1000):
        current_sprite = 1 if current_sprite == 0 else 0
        plane.image = Plane(current_sprite).image
        last_animation_time = ticks
    return [is_alternating, current_sprite, plane, last_animation_time]
