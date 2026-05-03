from fastapi import APIRouter

from app.schemas import (
    ExpectedRunsSavedRequest,
    CatchProbabilityRequest,
    ReactionTimeProxyRequest,
    FullFieldingAnalysisRequest,
)

from app.services.expected_runs_saved import calculate_expected_runs_saved
from app.services.catch_probability import calculate_catch_probability_model
from app.services.reaction_time_proxy import calculate_reaction_time_proxy


router = APIRouter(
    prefix="/student4",
    tags=["Student 4 Sprint 2 Fielding Analytics"],
)


@router.post("/expected-runs-saved")
def expected_runs_saved(payload: ExpectedRunsSavedRequest):
    return calculate_expected_runs_saved(payload)


@router.post("/catch-probability-model")
def catch_probability_model(payload: CatchProbabilityRequest):
    return calculate_catch_probability_model(payload)


@router.post("/reaction-time-proxy")
def reaction_time_proxy(payload: ReactionTimeProxyRequest):
    return calculate_reaction_time_proxy(payload)


@router.post("/full-fielding-analysis")
def full_fielding_analysis(payload: FullFieldingAnalysisRequest):
    expected_runs_saved_result = calculate_expected_runs_saved(
        payload.expected_runs_saved_data
    )

    catch_probability_result = calculate_catch_probability_model(
        payload.catch_probability_data
    )

    reaction_time_proxy_result = calculate_reaction_time_proxy(
        payload.reaction_time_proxy_data
    )

    expected_runs_saved_score = expected_runs_saved_result.get(
        "expected_runs_saved_score",
        0,
    )
    catch_probability_score = catch_probability_result.get(
        "catch_probability_score",
        0,
    )
    reaction_time_proxy_score = reaction_time_proxy_result.get(
        "reaction_time_proxy_score",
        0,
    )

    final_score = (
        0.40 * expected_runs_saved_score
        + 0.35 * catch_probability_score
        + 0.25 * reaction_time_proxy_score
    )

    final_score = round(max(0, min(100, final_score)), 2)

    if final_score >= 85:
        final_rating = "Elite Fielding Asset"
    elif final_score >= 70:
        final_rating = "High-Impact Fielder"
    elif final_score >= 55:
        final_rating = "Reliable Fielding Contributor"
    elif final_score >= 40:
        final_rating = "Developing Fielding Value"
    else:
        final_rating = "Low Fielding Impact"

    return {
        "player_name": payload.expected_runs_saved_data.player_name,
        "expected_runs_saved_analysis": expected_runs_saved_result,
        "catch_probability_analysis": catch_probability_result,
        "reaction_time_proxy_analysis": reaction_time_proxy_result,
        "final_fielding_intelligence_score": final_score,
        "final_rating": final_rating,
        "model_weights": {
            "expected_runs_saved_score": 0.40,
            "catch_probability_score": 0.35,
            "reaction_time_proxy_score": 0.25,
        },
        "interpretation": (
            "The final fielding intelligence score combines counterfactual run prevention, "
            "catch conversion above expectation, and inferred reaction quality."
        ),
    }