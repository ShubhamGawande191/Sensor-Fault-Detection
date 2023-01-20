from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

@dataclass
class ClassificationMetricArtifact:
    accuracy: float
    precision: float
    recall: float
    f1_score: float

@dataclass
class ModelTrainerArtifact:
    trained_model_path: str
    trained_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_test_file_path: str
    transformed_train_file_path: str

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_accuracy: float
    best_model_path: str
    train_model_metric_artifact: str
    test_model_metric_artifact: ClassificationMetricArtifact
    best_model_metric_artifact: ClassificationMetricArtifact

@dataclass
class ModelPusherArtifact:
    saved_model_path: str
    model_file_path: str