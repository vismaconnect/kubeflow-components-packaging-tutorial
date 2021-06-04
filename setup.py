import setuptools


setuptools.setup(
    name="kubeflow-components",
    version="0.0.1",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'multiply=kf_components.command_line:multiply',
        ],
    },
    package_data={'kf_components': ['yaml/*.yaml']}
)
