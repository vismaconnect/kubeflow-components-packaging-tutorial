import kfp
from kubeflow_demo_components import operators


@kfp.dsl.pipeline(
    name="Demo",
    description="A sample pipeline."
)
def my_pipeline(a=2, b=3):
    operators.multiply_op(a, b)
