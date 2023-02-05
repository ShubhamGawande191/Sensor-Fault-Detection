import os, sys
from sensor.exception import SensorException
import shutil
from sensor.utils.main_utils import write_yaml_file, save_object, load_object
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact, ModelTrainerArtifact
from sensor.entity.config_entity import ModelPusherConfig

class ModelPusher:

    def __init__(self, model_pusher_config: ModelPusherConfig,
                    model_evaluation_artifact: ModelEvaluationArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact
        except Exception as e:
            raise SensorException(e, sys)
        
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            trained_model_path = self.model_evaluation_artifact.trained_model_path
            model_path = self.model_pusher_config.model_path
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_path)
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)
            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_path, model_file_path=model_path)
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)