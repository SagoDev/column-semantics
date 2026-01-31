"""Package for semantic detection models."""

from .detection_models import Detection
from .output_models import InferenceResult, SemanticHypothesis

__all__ = ["Detection", "InferenceResult", "SemanticHypothesis"]
