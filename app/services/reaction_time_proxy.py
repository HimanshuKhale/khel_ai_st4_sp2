import math


MOVEMENT_MULTIPLIERS = {
    "stationary": 0.65,
    "forward": 0.85,
    "lateral": 1.00,
    "backward": 1.15,
    "forward_dive": 1.20,
    "lateral_dive": 1.35,
    "backward_dive": 1.50,
    "jump": 1.25,
    "sprint": 1.40,
}


def clamp(value: float, lower: float = 0, upper: float = 100) -> float:
    return max(lower, min(upper, value))


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def get_reaction_label(score: float) -> str:
    if score >= 85:
        return "Explosive Reactive Fielding"
    if score >= 70:
        return "Fast and Functional"
    if score >= 55:
        return "Good Reactive Value"
    if score >= 40:
        return "Moderate Reactive Value"
    return "Reaction Under Question"


def calculate_reaction_time_proxy(data):
    movement_multiplier = MOVEMENT_MULTIPLIERS.get(data.movement_type, 1.0)

    normalized_speed = data.ball_speed / 120
    normalized_distance = data.distance_moved / 30

    movement_burden = normalized_distance * movement_multiplier

    time_pressure = 1 / max(data.response_window, 0.1)

    difficulty_signal = (
        0.45 * normalized_speed
        + 0.35 * movement_burden
        + 0.20 * min(time_pressure / 3, 1)
    )

    stop_bonus = 0.18 if data.successful_stop else -0.12
    direct_hit_bonus = 0.15 if data.direct_hit else 0

    execution_signal = (
        0.70 * data.execution_quality
        + stop_bonus
        + direct_hit_bonus
    )

    reactive_efficiency = execution_signal - (0.45 * difficulty_signal)

    raw_score = sigmoid((reactive_efficiency - 0.15) * 4.2) * 100

    reaction_time_proxy_score = round(clamp(raw_score), 2)

    estimated_response_quality = clamp(
        data.execution_quality * 100
        - movement_burden * 12
        + (15 if data.successful_stop else -10)
        + (10 if data.direct_hit else 0),
        0,
        100,
    )

    return {
        "player_name": data.player_name,
        "ball_speed": data.ball_speed,
        "distance_moved": data.distance_moved,
        "response_window": data.response_window,
        "movement_type": data.movement_type,
        "movement_multiplier": movement_multiplier,
        "normalized_speed": round(normalized_speed, 3),
        "normalized_distance": round(normalized_distance, 3),
        "movement_burden": round(movement_burden, 3),
        "time_pressure": round(time_pressure, 3),
        "difficulty_signal": round(difficulty_signal, 3),
        "execution_quality": data.execution_quality,
        "execution_signal": round(execution_signal, 3),
        "reactive_efficiency": round(reactive_efficiency, 3),
        "estimated_response_quality": round(estimated_response_quality, 2),
        "reaction_time_proxy_score": reaction_time_proxy_score,
        "rating": get_reaction_label(reaction_time_proxy_score),
        "interpretation": (
            "This model infers reaction quality from observable signals: ball speed, distance moved, "
            "available response window, movement type, and execution result."
        ),
    }