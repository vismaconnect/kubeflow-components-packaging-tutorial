# Distributing Kubeflow components in a Python package

Last year we started using the [Kubeflow](https://www.kubeflow.org/) application to manage
the machine learning pipelines in our data science team at [Visma Connect](https://vismaconnect.nl/).
Since the Kubeflow application is still under heavy development, documentation
can sometimes be a bit limited. On top of that the documentation is naturally
focussed on functionality mainly, and less so on what this
could mean for organizing your code.

One of the things we thougt about at Visma Connect, is how to distribute our
Kubeflow components (i.e. pipeline steps) for reuse in different projects. These
reusable components are in our view a key
benefit of the Kubeflow application. In this repository we will show a simple way
of distributing the component definitions in a [Python package](https://packaging.python.org/).

Kubeflow components are defined by a [Docker](https://www.docker.com/) image and a YAML configuration file.
The configuration file tells which command to run on which Docker image, and what the
input and output parameters are. Note that different components can use the same
Docker image (but execute a different command). A Kubeflow pipeline loads these components as operator functions which can then
be knitted together.

The idea thus is to define these operator functions in
a Python package, so they can be used in a pipeline definition by any project
in your team. *Note that we still require the necessary Docker images to be stored
in a Docker container registry (e.g. [Amazon Elastic Container Registry](https://aws.amazon.com/ecr/)).*

First, we will define the YAML configuration files. Here is an example ([`multiply.yaml`](kf_components/yaml/multiply.yaml)):
```
name: Multiply
description: Multiply two numbers.
inputs:
- {name: a}
- {name: b}
implementation:
  container:
    image: 533211398604.dkr.ecr.eu-north-1.amazonaws.com/data-science-kubeflow/demo
    command: [multiply, --a, {inputValue: a}, --b, {inputValue: b}]
```
This will run the command `multiply --a <number-a> --b <number-b>`
on the specified Docker image. To enable this we will need to add the appropriate entrypoint
(i.e. console script) to our Python package and install this package onto the Docker image,
requiring the following steps. Note that the actual function is defined in [`command_line.py`](kf_components/command_line.py).

In [`setup.py`](setup.py):
```
entry_points={'console_scripts': ['multiply=kf_components.command_line:multiply']}
```
In [`requirements.txt`](requirements.txt`):
```
git+ssh://git@github.com/vismaconnect/kubeflow-components-packaging-tutorial.git#egg=kubeflow-demo-components
```
In [`Dockerfile`](Dockerfile):
```
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
```
*A special note when using private git repositories and ssh. In this case you need to
add
`RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts` to
`Dockerfile` and call the `pip` command with the `--mount=type=ssh` option. Subsequently, build the Docker image
with the `--ssh default=<path/to/key>` option.*

Now that we have the component definition, we need to include it as an operator
function in our package definition.

In [`operators.py`](kf_components/operators.py):
```
multiply_op = kfp.components.load_component_from_text(pkg_resources.resource_string(__name__, 'yaml/multiply.yaml'))
```
And make sure the YAML files are included in your package distribution.

In [`setup.py`](setup.py):
```
package_data={'kf_components': ['yaml/*.yaml']}
```
That's all. You can now use your component in any pipeline as simple as ([`pipeline.py`](pipeline.py)):
```
import kfp
from kubeflow_demo_components import operators


@kfp.dsl.pipeline(name="Demo", description="A sample pipeline.")
def my_pipeline(a=2, b=3):
    operators.multiply_op(a, b)
```
