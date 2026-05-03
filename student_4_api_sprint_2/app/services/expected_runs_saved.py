import math


def clamp(value: float, lower: float = 0, upper: float = 100) -> float:
    return max(lower, min(upper, value))


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def get_ers_label(score: float) -> str:
    if score >= 85:
        return "Elite Run Prevention"
    if score >= 70:
        return "Strong Fielding Value"
    if score >= 55:
        return "Positive Fielding Value"
    if score >= 40:
        return "Neutral to Mild Value"
    return "Negative Fielding Value"


def calculate_expected_runs_saved(data):
    expected_runs = data.expected_runs_without_intervention
    actual_runs = data.actual_runs_conceded

    run_swing = expected_runs - actual_runs

    intervention_rate = data.successful_interventions / data.fielding_attempts

    direct_hit_rate = (
        data.direct_hits / data.direct_hit_attempts
        if data.direct_hit_attempts > 0
        else 0
    )

    boundary_save_density = data.boundary_saves / data.fielding_attempts

    throw_quality_signal = (
        0.65 * data.throw_accuracy
        + 0.35 * direct_hit_rate
    )

    repeatability_weight = math.sqrt(intervention_rate)

    pressure_multiplier = 1 + (0.15 * data.fielding_pressure_index)

    counterfactual_value_signal = (
        1.30 * run_swing
        + 1.10 * intervention_rate
        + 0.90 * boundary_save_density
        + 0.75 * throw_quality_signal
        + 0.50 * repeatability_weight
    )

    normalized_score = sigmoid(counterfactual_value_signal - 2.25) * 100
    normalized_score *= pressure_multiplier

    expected_runs_saved_score = round(clamp(normalized_score), 2)

    return {
        "player_name": data.player_name,
        "expected_runs_without_intervention": expected_runs,
        "actual_runs_conceded": actual_runs,
        "run_swing": round(run_swing, 3),
        "fielding_attempts": data.fielding_attempts,
        "successful_interventions": data.successful_interventions,
        "intervention_rate": round(intervention_rate, 3),
        "boundary_saves": data.boundary_saves,
        "boundary_save_density": round(boundary_save_density, 3),
        "direct_hit_rate": round(direct_hit_rate, 3),
        "throw_accuracy": data.throw_accuracy,
        "throw_quality_signal": round(throw_quality_signal, 3),
        "repeatability_weight": round(repeatability_weight, 3),
        "fielding_pressure_index": data.fielding_pressure_index,
        "pressure_multiplier": round(pressure_multiplier, 3),
        "counterfactual_value_signal": round(counterfactual_value_signal, 3),
        "expected_runs_saved_score": expected_runs_saved_score,
        "rating": get_ers_label(expected_runs_saved_score),
        "interpretation": (
            "This model compares expected runs without intervention against actual runs conceded. "
            "Positive run swing, repeatable interventions, boundary saves, and throw quality increase the score."
        ),
    }