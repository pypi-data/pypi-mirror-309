# AnhaltAI Commons PL Hyper

**AnhaltAI** **Commons** **P**ytorch **L**ightning Trainer Framework for **Hyper**
Parameter Optimization

## Summary

Deep Learning Trainer based on PyTorch Lightning with common usable setup for different
deep learning tasks that supports k-Fold cross-validation to fulfill automated
hyperparameter optimization.
The runs are planned by using sweeps
from [Weights and Biases (wandb)](https://wandb.ai/site/)
that are created based on the supported configuration files.

With the usage of the code of Weights and Biases and Lightning AI the training using
multiple GPUs
and wandb agent processes is a main part of this framework.

The foundation provided by this framework must be extended with code parts for each
AI learning task.

The package is accessible on [PyPI](https://pypi.org/project/anhaltai-pl-hyper/) and
compatible to [Python version >=3.10](https://www.python.org/downloads/)

## Contents

- [Usage](#usage)
    - [Install with pip](#install-with-pip)
    - [Extend the implementation for your task](#extend-the-implementation-for-your-task)
      <details open>
      <summary>Related Links</summary>

        - [src/anhaltai_commons_pl_hyper/README.md](src/anhaltai_commons_pl_hyper/README.md)
      </details>
    - [Extend sweep server and wandb agent](#extend-sweep-server-and-wandb-agent)
    - [Configure logging for multiprocessing](#configure-logging-for-multiprocessing)
    - [Setup Configs](#setup-configs)
      <details open>
      <summary>Related Links</summary>

        - [docs/config-documentation.md](docs/config-documentation.md)
        - [docs/data-splitting-documentation.md](docs/data-splitting-documentation.md)
      </details>
    - [Setup Environment Variables](#setup-environment-variables)
    - [Run your training](#run-your-training)
- [Development Setup](#development-setup)
    - [Install python requirements](#install-python-requirements)
    - [Entrypoints](#entrypoints)
    - [Build package locally](#build-package-locally)
    - [Unit Tests and Integration Tests](#unit-tests-and-integration-tests)

## Usage

### Install with pip

```
pip install anhaltai-pl-hyper
```

### Extend the implementation for your task

To use this framework for your very specific task you have to extend the provided
abstract classes and functions.
You need to add the implementation of your **Trainer**, **DataModule**,
**TrainingModule**
and preprocessing of your **datasets** for your specific AI learning **task**.

There are multiple integration tests in the ``tests/integration`` directory showing
examples how to use this framework for your AI training e.g. for different tasks and
data splitting.

You will find detailed information
here: [src/anhaltai_commons_pl_hyper/README.md](src/anhaltai_commons_pl_hyper/README.md)

### Extend sweep server and wandb agent

The package provides functions to run a **sweep server** that creates or resumes a
Weights and Biases (wandb)
sweep. Then **multiple agents** can be started. They get the sweep IDs from the server
via REST request and start an available run of the sweep.

To use them you can create your own functions to call the provided functions
``create_agent()`` and
``SweepServer().main()`` from your code base. Feel free to extend or overwrite these
functions for your need.
Having these in your implementation enables the later
step [Build docker images](#build-docker-images)

#### Basic example:

.../wandb_utils/sweep_server.py

````Python
from anhaltai_commons_pl_hyper.wandb_utils.sweep_server import SweepServer

if __name__ == "__main__":
    # load your env variables here

    SweepServer().main()  # run
````

.../wandb_utils/sweep_agent.py

````Python
from anhaltai_commons_pl_hyper.wandb_utils.sweep_agent import create_agent

if __name__ == "__main__":
    # load your env variables here

    create_agent()  # run
````

To resume Weights and Biases (wandb) runs by using SweepServer you will need to install
wandb on your **system interpreter**!
The resume of a sweep is explained in a further section [Setup Configs](#setup-configs).

````shell
pip install wandb
````

#### Configure logging for multiprocessing:

It is recommended to insert custom logging options before calling `create_agent()` and
`SweepServer().main()` to be able to read logs of multiple processes more clearly:

````Python
import logging

log_format = "%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format, datefmt="%Y-%m-%d %H:%M:%S")
````

### Setup Configs

Example config files are located in ``./configs/``

You will find its documentation
here: [docs/config-documentation.md](docs/config-documentation.md)

Supported data splitting modes are documented here:
[docs/data-splitting-documentation.md](docs/data-splitting-documentation.md)
TL;DR: basically: train, or train+test, or train+test+val.

The location of the config files can be set with environment variables as explained in
[Setup Environment Variables](#setup-environment-variables).

### Setup Environment Variables

Usage: First copy ``.env-example`` file as ``.env`` file to your project root and change
its values as you need.

#### Required Environment Variables for training

| Variable               | Example                               | Source                                                                                                 | Description                                                                         | 
|------------------------|---------------------------------------|--------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| WANDB_PROJECT          | myproject                             | [wandb](https://docs.wandb.ai/guides/track/environment-variables/)                                     | Name of the wandb project. (https://docs.wandb.ai/ref/python/init/)                 |                                   
| WANDB_API_KEY          |                                       | [wandb](https://docs.wandb.ai/guides/track/environment-variables/)                                     | API KEY of your wandb account                                                       |                                   
| WANDB_ENTITY           | mycompany                             | [wandb](https://docs.wandb.ai/guides/track/environment-variables/)                                     | Name of the wandb entity. (https://docs.wandb.ai/ref/python/init/)                  |                                   
| CHECKPOINT_DIRECTORY   | models                                | <br/>                                                                                                  | Local directory to save the checkpoints.                                            |                                   
| SWEEP_DIRECTORY        | configs/sweep                         |                                                                                                        | Local directory of the configs for your wandb sweeps.                               |                                   
| SINGLE_RUN_CONFIG_PATH | configs/single-run.yaml               |                                                                                                        | Local file of the single run config for your single wandb run if not using a sweep. |                                   
| TRAINER_PATH           | classification.classification_trainer |                                                                                                        | Python file where your trainer subclass is implemented for your learning task       |                                   
| SWEEP_SERVER_ADDRESS   | http://localhost:5001                 |                                                                                                        | The address of your hosted sweep server                                             |                                   
| HF_USERNAME            | username                              | [Hugging Face](https://huggingface.co/docs/huggingface_hub/en/package_reference/environment_variables) | Huggingface username                                                                |                                   
| HF_TOKEN               |                                       | [Hugging Face](https://huggingface.co/docs/huggingface_hub/en/package_reference/environment_variables) | Huggingface token                                                                   |                                   

#### Additional Environment Variables for Docker and Kubernetes

| Variable                       | Example                  | Source | Description                                            |  
|--------------------------------|--------------------------|--------|--------------------------------------------------------|
| DOCKER_REPOSITORY_SERVER       | gitlab.com:5050          |        | Repository server of of your docker container registry |                                   
| DOCKER_REPOSITORY_PATH         | myprojectGroup/myproject |        | Repository path of your docker container registry      |                                   
| DOCKER_TRAINING_IMAGE_NAME     | 2024.10.dev0             |        | Trainer image name for docker build (dev or release)   |                                   
| DOCKER_SWEEP_SERVER_IMAGE_NAME | sweep-server             |        | Sweep server image name for docker build               |                                   
| DOCKER_USERNAME                | username                 |        | Username of your docker container registry             |                                   
| DOCKER_TOKEN                   |                          |        | Token of your docker container registry                |                                   
| KUBE_NAMESPACE                 | my-training              |        | Your kubernetes namespace                              |                                   
| KUBE_SWEEP_SERVER_ADDRESS      | http://sweep-server:5001 |        | The address of your hosted sweep server on kubernetes  |                                   

### Run your training

This step depends on your project specific setup, your hardware and your configuration.
Run a wandb sweep by running the ``SweepServer`` or other options provided by
Weights and Biases ([wandb](https://docs.wandb.ai/guides/sweeps/)).

Then run one or more sweep agents with ``create_agent()`` or your specific
implementation.

You can also start a single run by starting your trainer subclass e.g. ``trainer.py``.

#### Metrics

The metrics of the runs can be retrieved from the
[Weights and Biases website](https://wandb.ai/).
You can set the config for it via the [run/sweep config](docs/config-documentation.md)
and the login with wandb
[environment variables](#additional-environment-variables-for-docker-and-kubernetes).

#### Checkpoints

The checkpoints are saved to the relative directory path that is given by the [env
variable](#additional-environment-variables-for-docker-and-kubernetes)
``CHECKPOINT_DIRECTORY`` which is by default ``models``.
Subfolders are created for the ``best`` and ``latest`` checkpoints
(its existence depends on [run/sweep config](docs/config-documentation.md)).
Inside these folders subfolders with the timestamp of creation are created.
There you will find the checkpoint directories for your runs named by the wandb run id
of the run that is logged on the [Weights and Biases website](https://wandb.ai/).

The upload of the checkpoints of the trained model to Hugging Face can be configured
in the [run/sweep config](docs/config-documentation.md).

When using [Kubernetes](#example-for-running-on-kubernetes) it is possible to mount this
checkpoint folder as [volume](https://kubernetes.io/docs/concepts/storage/volumes/)
e.g. [Persistent Volumes (PVC)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
to be able to retrieve the checkpoints after a training.

#### Build docker images

This step depends also on your project specific setup.

You can build **docker images** for the sweep agent and the sweep server.

> **_Hint:_** Configs explained in [Setup Configs](#setup-configs) will be
> baked into the docker image for now. So can rebuild the SweepServer if you
> make changes in the sweep config files. Alternatively you can mount the config
> files as volumes (Read further for examples:
> [Example for running on Kubernetes](#example-for-running-on-kubernetes)).

You will find example **Dockerfiles** in the root of this repository
and **example build scripts** in the ``scripts`` directory.

#### Example for running on Kubernetes

You can run the (custom) built docker images with
[Kubernetes](https://kubernetes.io/docs/home/).
There are also templates for kubernetes yaml files in the ``configs`` dir that fit to
the example Dockerfiles.

##### For a sweep:

- ``segmentation-training-with-sweep-server.yaml`` (cmd runs trainer from sweep agent)
- ``sweep-server-service.yaml``

Alternatively for a sweep:

- ``segmentation-training-pod.yaml``
- ``sweep-server.yaml``

In the example the sweep config files  ``model.yaml``, ``logging.yaml`` and
``dataset.yaml`` are given in addition to the mandatory ``sweep.yaml``.

They are given in
a [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/)
named ``sweep-config-yaml`` and mounted by using a
[volume](https://kubernetes.io/docs/concepts/storage/volumes/)
to replace the default config files. The ConfigMap must be created in the same
Kubernetes namespace as used for the training.

To create the ConfigMap add the filename and the content of the file
for each config file as key value pairs to the ConfigMap. The filename is used as key
and the file content is to be pasted as value.

The image shows an example for two files:
<img src="docs/imgs/kubernetes-config-map-sweep.png" alt="img scikit-learn cross validation" width="800">

As shown in the ``classification-training-with-sweep-server.yaml`` the ConfigMap is
provided as volume for the sweep server so that all files given in the ConfigMap are
used to fully replace the default ``configs/sweep`` folder:

Shown are the most important lines:

````
metadata:
  name: sweep-server
[...]
spec:
[...]
  containers:
[...]
      volumeMounts:
        - name: sweep-config-yaml
          mountPath: /configs/sweep
[...]
  volumes:
    - name: sweep-config-yaml
      configMap:
        name: sweep-config-yaml
````

For more details, see the
[Kubernetes docs](https://kubernetes.io/docs/concepts/configuration/configmap/).

##### For a single run:

- ``classification-training-pod-single-run.yaml`` (cmd runs trainer directly)

For the single run it is also possible to provide the ``single-run.yaml`` in a
[ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/)
e.g. ``single-run-yaml``. The filename ``single-run.yaml`` is used as key
and the file content as value inside the ConfigMap.

As visible in the example ``classification-training-pod-single-run.yaml`` the
ConfigMap is provided as [volume](https://kubernetes.io/docs/concepts/storage/volumes/)
for the container (sweep server is not needed) in which
the training runs.
To be able to only replace the default ``single-run.yaml`` that is located at
``/workspace/configs/single-run.yaml`` in the docker image only the ``single-run.yaml``
key is used from the ConfigMap as volume. For the volume mount is the ``subPath``
parameter necessary to only replace that single file.

Shown are the most important lines:

````
[...]
      containers:
        - name: pytorch-model-single-run
[...]
          volumeMounts:
            [...]
            - mountPath: /workspace/configs/single-run.yaml
              name: single-run-yaml
              subPath: single-run.yaml
[...]
      volumes:
        [...]
        - name: single-run-yaml
          configMap:
            name: single-run-yaml
            items:
              - key: single-run.yaml
                path: single-run.yaml
````

## Development Setup

### Install python requirements

````shell
pip install -r requirements.txt
pip install -r requirements-tests.txt
````

### Entrypoints

You need to prepare the following:

- [Setup Configs](#setup-configs)
- [Setup Environment Variables](#setup-environment-variables)

It is just a demo for debugging and to write tests.
You will need to do all steps described in [Usage](#usage) to be able to run a minimal
working example.

To start wandb single run without sweep:

````shell
python src/anhaltai_commons_pl_hyper/trainer.py
````

To start wandb sweep server:

````shell
python src/anhaltai_commons_pl_hyper/wandb_utils/sweep_server.py
````

To start a local sweep run that gets the sweep ID from the sweep server to execute its
runs:

````shell
python src/anhaltai_commons_pl_hyper/wandb_utils/sweep_agent.py
````

### Build package locally

````shell
python -m build 
````

### Unit Tests and Integration Tests

- Test scripts directory: tests
- Integration test scripts directory: tests/integration
- The integration tests in tests/integration ar used to show minimal example project
  setups
- All tests have to be run from the project root dir as workdir
- Please do not mark the subdirectories named "src" python as source folders to avoid
  breaking the structure
- To find all code modules during tests the ``pythonpath`` is defined in the
  ``pyproject.toml`` file

This way all tests functions (with prefix "tests") are found and executed from project
root:

````shell
pytest tests
````