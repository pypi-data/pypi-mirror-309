from dataclasses import dataclass, field

import marshmallow.validate


@dataclass()
class LogisticRegressionParams:
    penalty: str = field(
        default="l2", metadata={"validate": marshmallow.validate.OneOf(["l1", "l2"])}
    )


@dataclass()
class RandomForestParams:
    n_estimators: int = field(default=20, metadata={"validate": marshmallow.validate.Range(min=1)})
    max_depth: int = field(default=10, metadata={"validate": marshmallow.validate.Range(min=1)})


@dataclass()
class DecisionTreeParams:
    max_depth: int = field(default=10, metadata={"validate": marshmallow.validate.Range(min=1)})


@dataclass()
class TrainParams:
    model_path: str
    model_file_name: str
    metrics_path: str
    model_name: str = field(
        metadata={
            "validate": marshmallow.validate.OneOf(
                ["logistic_regression", "random_forest", "decision_tree"]
            )
        }
    )
    n_estimators: int = field(default=50, metadata={"validate": marshmallow.validate.Range(min=0)})
    classification_model_params: dict = field(default_factory=dict)
