from dataclasses import dataclass, field

import marshmallow.validate


@dataclass()
class DataParams:
    data_dir: str
    n_samples: int = field(
        default=10000, metadata={"validate": marshmallow.validate.Range(min=10)}
    )
    n_features: int = field(default=10, metadata={"validate": marshmallow.validate.Range(min=1)})
    test_size: float = field(
        default=0.2, metadata={"validate": marshmallow.validate.Range(min=0.1)}
    )
