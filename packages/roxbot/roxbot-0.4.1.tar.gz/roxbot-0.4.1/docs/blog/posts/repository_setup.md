---
date: 2024-05-01
draft: false
categories:
  - cicd
authors:
  - jev
---



# Repository structure

As Aristotle famously said, "Well begun is half done." This is particularly true when starting a new software project. In this post, I'll explain why Continuous Integration (CI) is crucial in modern software development, especially in complex fields like robotics. We'll also look at how CI/CD principles are implemented in the `roxbot` repository, providing practical insights and inviting you to explore the repository's code for more details.

<!-- more -->

## Why Is CI Crucial?

Setting up a CI/CD workflow can be daunting, especially in robotics. Homer Simpson humorously said, "If something is hard to do, then maybe it's not worth doing." However, adopting this mindset can lead to significant challenges in larger projects, such as inconsistent environments, outdated documentation, and unstable software. Here’s why CI/CD is essential:

1. **Consistent Build and Test Environments**: CI/CD standardizes environments across all development stages, crucial in robotics where diverse tools and packages are used.

2. **Enhanced Code Quality**: CI automates testing to ensure new code integrates well with the existing codebase, catching issues early to prevent real-world problems.

3. **Reduced Deployment Risk**: Automated tests in production-like environments decrease the likelihood of failures and enhance safety when deploying software.

## How We Implement CI/CD in `roxbot`

!!! note
    Setting up CI/CD properly takes effort and time; getting it 'fairly OK' is achievable, but perfecting it requires considerable work. As a developer, I aim to spend most of my time building functionality, not endlessly polishing my CI/CD environment—which could easily become a full-time job. You'll likely find many areas for improvement in `roxbot`'s CI/CD, as I capped the setup time at 4 hours. In my experience, CI/CD can *always* be improved, and contributions are welcome!

- **Docker Environments**:
    - **Development Image (`dev`)**: Managed via `docker/dev/Dockerfile`, includes comprehensive tools for development.
    - **Continuous Integration Image (`ci`)**: Managed via `docker/ci/Dockerfile`, designed for reliable and clean testing.

- **GitHub Actions**: Automation is managed through actions configured in `.github/workflows/build-images.yml` for building and hosting the `dev` image.

- **VSCode DevContainer**: Development setup is streamlined using the configuration in `.devcontainer/devcontainer.json`.

- **Hosting Images on GitHub**: Docker images are hosted using GitHub Packages as part of the workflow defined in `.github/workflows/build-images.yml`.

- **Configuration with `pyproject.toml`**:
    - `ruff` linter to maintain high code quality and consistency across the project.
    - `mypy` typechecker enhancing code reliability by catching type errors before runtime.
    - `pytest` with coverage reports. See which lines of code escaped the tests.

- **Task automation with `invoke`**: a modern, pythonic way of scripting. The tasks are defined in `tasks.py`.  Run `invoke --help` for more.

- **Building Documentation with MkDocs**: Documentation is automatically built and updated using MkDocs, configured in `mkdocs.yml`.

This toolset not only solves the "It works on my machine" problem but also ensures a high level of task automation, saving time for actual software deveopment.

Explore the repository to see how these features are implemented and consider integrating them into your own projects.

!!! tip
    Manually setting up a repository for each new project can take a lot of time and result in many different structures. To aid this, there is an excellent tool called [cookiecutter](https://github.com/cookiecutter/cookiecutter). There are many templates available to set up a repo in less than a minute! One of my own templates that I often use is [python-microservice](https://gitlab.com/roxautomation/templates/python-microservice/).  Want to go even further? Take a look at  [cruft](https://cruft.github.io/cruft/) - a tool to update repositories to their templates.
