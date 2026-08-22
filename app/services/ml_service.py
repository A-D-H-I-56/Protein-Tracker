from pathlib import Path
from typing import Dict, Any, List
from app.models.ml_engine import MLEngine
from app.models.metrics_model import ModelMetrics
from app.models.nutrition_plan import SimilarProfile

class MLService:
    """
    Service Layer wrapping the ML Engine and Model Evaluation Metadata.
    Decouples controllers and higher-level services from ML persistence specifics.
    """
    def __init__(self, artifacts_dir: Path, dataset_path: Path):
        self.artifacts_dir = Path(artifacts_dir)
        self.dataset_path = Path(dataset_path)
        self.engine = MLEngine(artifacts_dir=self.artifacts_dir, dataset_path=self.dataset_path)
        self._metrics = None

    @property
    def is_ready(self) -> bool:
        return self.engine.is_loaded

    def predict(self, profile_dict: Dict[str, Any]) -> Dict[str, int]:
        return self.engine.predict(profile_dict)

    def find_similar_profiles(self, profile_dict: Dict[str, Any], k: int = 3) -> List[SimilarProfile]:
        return self.engine.find_similar_profiles(profile_dict, k=k)

    def get_metrics(self) -> ModelMetrics:
        metrics_file = self.artifacts_dir / 'evaluation_metrics.json'
        return ModelMetrics.load_from_file(metrics_file)
