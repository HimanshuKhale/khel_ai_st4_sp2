from typing import Literal
from pydantic import BaseModel, Field, model_validator


MovementType = Literal[
    "stationary",
    "forward",
    "lateral",
    "backward",
    "forward_dive",
    "lateral_dive",
    "backward_dive",
    "jump",
    "sprint",
]


class ExpectedRunsSavedRequest(BaseModel):
    player_name: str = Field(..., example="Ravindra Jadeja")

    expected_runs_without_intervention: float = Field(..., ge=0, le=8, example=3.8)
    actual_runs_conceded: float = Field(..., ge=0, le=8, example=1.0)

    fielding_attempts: int = Field(..., ge=1, example=6)
    successful_interventions: int = Field(..., ge=0, example=4)

    boundary_saves: int = Field(default=0, ge=0, example=2)

    direct_hit_attempts: int = Field(default=0, ge=0, example=2)
    direct_hits: int = Field(default=0, ge=0, example=1)

    throw_accuracy: float = Field(default=0.5, ge=0, le=1, example=0.76)
    fielding_pressure_index: float = Field(default=0.5, ge=0, le=1, example=0.81)

    @model_validator(mode="after")
    def validate_counts(self):
        if self.successful_interventions > self.fielding_attempts:
            raise ValueError("successful_interventions cannot exceed fielding_attempts.")

        if self.direct_hits > self.direct_hit_attempts:
            raise ValueError("direct_hits cannot exceed direct_hit_attempts.")

        return self


class CatchProbabilityRequest(BaseModel):
    player_name: str = Field(..., example="Ravindra Jadeja")

    catch_attempts: int = Field(..., ge=1, example=8)
    catches_taken: int = Field(..., ge=0, example=6)

    average_hang_time: float = Field(..., gt=0, le=8, example=2.1)
    average_ball_speed: float = Field(..., gt=0, le=180, example=88)
    average_distance_covered: float = Field(..., ge=0, le=60, example=12.5)
    average_reaction_angle: float = Field(..., ge=0, le=180, example=42)

    dive_or_jump_required_rate: float = Field(default=0, ge=0, le=1, example=0.38)
    backward_movement_rate: float = Field(default=0, ge=0, le=1, example=0.25)

    sample_stability: float = Field(default=0.75, ge=0.1, le=1, example=0.75)

    @model_validator(mode="after")
    def validate_catches(self):
        if self.catches_taken > self.catch_attempts:
            raise ValueError("catches_taken cannot exceed catch_attempts.")

        return self


class ReactionTimeProxyRequest(BaseModel):
    player_name: str = Field(..., example="Ravindra Jadeja")

    ball_speed: float = Field(..., gt=0, le=180, example=92)
    distance_moved: float = Field(..., ge=0, le=60, example=14)

    response_window: float = Field(..., gt=0, le=5, example=0.62)
    movement_type: MovementType = Field(default="lateral", example="lateral_dive")

    execution_quality: float = Field(..., ge=0, le=1, example=0.84)

    successful_stop: bool = Field(default=True, example=True)
    direct_hit: bool = Field(default=False, example=False)


class FullFieldingAnalysisRequest(BaseModel):
    expected_runs_saved_data: ExpectedRunsSavedRequest
    catch_probability_data: CatchProbabilityRequest
    reaction_time_proxy_data: ReactionTimeProxyRequest