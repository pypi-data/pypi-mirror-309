## How to contribute

This is what you can do to make this project a succes:

* Star the github repo - this promotes its visibility
* Join the discussion on the [forum](https://github.com/rox-automation/roxbot/discussions) - we'd love to know how we can make robotics development easier.
* Find something worth fixing? Submit an issue.
* Write a blog post or add to documentation by creating a pull request.


## Development workflow

### Prerequisites

* VSCode with devcontainer extension intalled
* `invoke` - python automation tool (`pip install invoke`)
* `docker`

### Working in devcontainer

This repository provides a `.devcontainer` environment that can be used in VSCode. For more information, read [VSCode containers docs](https://code.visualstudio.com/docs/devcontainers/containers)

The source for devcontainer image is located in `docker/dev`. It is built by github actions and hosted at `ghcr.io/rox-automation/roxbot:latest`


### CI

`ci_script.sh` executes linting and testing steps. This script can be run from a devcontainer or in a CI environment.
CI can be run in these ways:

* on *host* machine, run `invoke ci`. This will build a CI docker container, copy source code into it an run it. Because of caching, this is the fastest way to run ci in a clean envirionment.
* in *devcontainer* run `./ci_script.sh`.
* automated CI with github actions: TODO
