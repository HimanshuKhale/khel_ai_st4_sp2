import math


def clamp(value: float, lower: float = 0, upper: float = 100) -> float:
    return max(lower, min(upper, value))


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def get_catch_label(score: float) -> str:
    if score >= 85:
        return "Elite Catch Conversion"
    if score >= 70:
        return "Strong Above-Expected Catching"
    if score >= 55:
        return "Above Expected Catching"
    if score >= 40:
        return "Around Expected Catching"
    return "Below Expected Catching"


def calculate_catch_probability_model(data):
    actual_conversion_rate = data.catches_taken / data.catch_attempts

    speed_factor = data.average_ball_speed / 120
    distance_factor = data.average_distance_covered / 30
    angle_complexity = abs(data.average_reaction_angle - 45) / 90

    time_cushion = data.average_hang_time / 4
    movement_complexity = (
        0.35 * distance_factor
        + 0.25 * speed_factor
        + 0.20 * angle_complexity
        + 0.10 * data.dive_or_jump_required_rate
        + 0.10 * data.backward_movement_rate
    )

    difficulty_index = clamp(
        movement_complexity - (0.25 * time_cushion),
        0,
        1,
    )

    expected_catch_probability = clamp(
        0.92 - (0.68 * difficulty_index),
        0.08,
        0.96,
    )

    overperformance_gap = actual_conversion_rate - expected_catch_probability

    difficulty_bonus = difficulty_index * 8

    raw_score = (
        50
        + overperformance_gap * 95 * data.sample_stability
        + difficulty_bonus
    )

    catch_probability_score = round(clamp(raw_score), 2)

    expected_catches = expected_catch_probability * data.catch_attempts
    catches_above_expected = data.catches_taken - expected_catches

    return {
        "player_name": data.player_name,
        "catch_attempts": data.catch_attempts,
        "catches_taken": data.catches_taken,
        "actual_conversion_rate": round(actual_conversion_rate, 3),
        "average_hang_time": data.average_hang_time,
        "average_ball_speed": data.average_ball_speed,
        "average_distance_covered": data.average_distance_covered,
        "average_reaction_angle": data.average_reaction_angle,
        "dive_or_jump_required_rate": data.dive_or_jump_required_rate,
        "backward_movement_rate": data.backward_movement_rate,
        "speed_factor": round(speed_factor, 3),
        "distance_factor": round(distance_factor, 3),
        "angle_complexity": round(angle_complexity, 3),
        "time_cushion": round(time_cushion, 3),
        "movement_complexity": round(movement_complexity, 3),
        "difficulty_index": round(difficulty_index, 3),
        "expected_catch_probability": round(expected_catch_probability, 3),
        "expected_catches": round(expected_catches, 2),
        "catches_above_expected": round(catches_above_expected, 2),
        "overperformance_gap": round(overperformance_gap, 3),
        "sample_stability": data.sample_stability,
        "catch_probability_score": catch_probability_score,
        "rating": get_catch_label(catch_probability_score),
        "interpretation": (
            "This model estimates catch difficulty using hang time, ball speed, distance, angle, "
            "dive requirement, and backward movement. The final score rewards conversion above expectation."
        ),
    }