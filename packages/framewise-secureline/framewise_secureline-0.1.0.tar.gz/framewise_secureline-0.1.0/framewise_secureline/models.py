import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Callable, Tuple
from .exceptions import ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class RiskCategory(Enum):
    """Enum to define risk categories."""
    BENIGN = "Benign"
    PROMPT_ATTACKS = "Prompt Attacks"
    DENIED_TOPICS = "Denied Topics"
    PPI = "PPI Information"
    WORD_FILTERS = "Word Filters"


@dataclass
class DetectionResult:
    """Container for detection results."""
    raw_response: Dict[str, Dict[str, float]]
    elapsed_time: float
    timestamp: datetime = field(default_factory=datetime.now)
    _probabilities: Dict[str, float] = field(init=False)

    def __post_init__(self):
        logger.info("Initializing DetectionResult instance.")
        self._probabilities = self.raw_response.get("probabilities", {})
        if not isinstance(self._probabilities, dict):
            logger.error("Invalid probabilities format in raw_response.")
            raise ValidationError("Probabilities must be a dictionary.")
        logger.info("Initialization complete. Probabilities loaded.")

    def get_score(self, category: RiskCategory) -> float:
        """Get score for a specific category."""
        logger.info(f"Fetching score for category: {category.name}.")
        if not isinstance(category, RiskCategory):
            logger.error(f"Invalid category provided: {category}.")
            raise ValidationError("Invalid category.")
        score = self._probabilities.get(category.value, 0.0)
        logger.info(f"Score for {category.name}: {score}.")
        return score

    def get_highest_risk(self) -> Tuple[str, float]:
        """Get the highest risk category."""
        if not self._probabilities:
            logger.warning("No probabilities available for highest risk calculation.")
            return "None", 0.0
        highest_risk = max(self._probabilities.items(), key=lambda x: x[1], default=("None", 0.0))
        logger.info(f"Highest risk category: {highest_risk[0]} with score: {highest_risk[1]}.")
        return highest_risk

    def __getattr__(self, name: str) -> Callable[[], float]:
        """
        Dynamically handle get_{category} calls as functions.

        Args:
            name (str): The name of the method being accessed.

        Returns:
            Callable[[], float]: A function that returns the score for the requested category.

        Raises:
            ValidationError: If the requested method does not match the expected pattern.
        """
        if name.startswith("get_"):
            category_name = name[4:].upper()
            try:
                category = RiskCategory[category_name]
                logger.info(f"Creating dynamic method for category: {category_name}.")
                return lambda: self.get_score(category)
            except KeyError:
                logger.error(f"Invalid risk category requested: {category_name}.")
                raise ValidationError(f"Invalid risk category: {category_name}")
        logger.error(f"Invalid attribute or method requested: {name}.")
        raise AttributeError(f"'DetectionResult' object has no attribute '{name}'")
