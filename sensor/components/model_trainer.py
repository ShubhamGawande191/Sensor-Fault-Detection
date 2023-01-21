import os, sys
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.utils.main_utils import save_object, load_object, load_numpy_array_data
from sensor.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.ml.model.estimator import SensorModel
from sensor.ml.metric.classification_metric import get_classification_score
from xgboost import XGBClassifier

class ModelTrainer:

    def __init__(self, model_trainer_config: ModelTrainerConfig,
                    data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)
        
    def train_model(self, x_train, y_train):
        try:
            model = XGBClassifier()
            model.fit(x_train, y_train)
            return model
        except Exception as e:
            raise e
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.train_file_path
            test_file_path = self.data_transformation_artifact.test_file_path
            train_data = load_numpy_array_data(train_file_path)
            test_data = load_numpy_array_data(test_file_path)
            x_train = train_data[:, :-1]
            y_train = train_data[:, -1]
            x_test = test_data[:, :-1]
            y_test = test_data[:, -1]
            model = self.train_model(x_train, y_train)
            y_train_pred = model.predict(x_train)
            classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)

            if classification_train_metric.f1_score<=self.model_trainer_config.expected_accuracy:
                raise SensorException("Model accuracy is less than expected accuracy")
            
            y_test_pred = model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

            diff = abs(classification_train_metric.f1_score - classification_test_metric.f1_score)
            if diff>self.model_trainer_config.overfitting_underfitting_threshold:
                raise SensorException("Model is overfitting or underfitting")
            
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)
            save_object(model, self.model_trainer_config.model_file_path, obj=SensorModel(preprocessor=preprocessor, model=model))

            model_trainer_artifact = ModelTrainerArtifact(trained_model_path=self.model_trainer_config.trained_model_file_path, train_metric=classification_train_metric, test_metric=classification_test_metric)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise SensorException(e, sys)