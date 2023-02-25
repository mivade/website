---
title: Useful BASH shortcuts for conda
date: 2018-10-24
tags:
  - python
  - conda
  - notes
---

Anaconda's [conda](https://conda.io/docs/) has become the de facto environment
management tool in Python-oriented scientific computing. Its lightweight
environments are suitable for development and, at least in some cases,
deployment. In general, for each new project, I like to create a new
environment. Creating a new, mostly empty environment is done with the following
command:

```bash
$ conda env create -y -n my-project-name
```

Then the new environment must be activated with

```bash
$ conda activate my-project-name
```

If I later want to remove the environment:

```bash
$ conda env remove -y -n my-project-name
```

This can get tiresome, so I have the following functions defined in my
`.bashrc`:

```bash
function conact() {
    conda activate $(basename $(pwd))
}

function cenv() {
    if [ -f environment.yaml ]; then
	conda env create --file=environment.yaml -n $(basename $(pwd))
    else
	conda create -yn $(basename $(pwd))
    fi
}

function rmcenv() {
    conda remove -n $(basename $(pwd)) --all
}
```

Now when starting a new project, I need only type

```
$ cenv
$ conact
```
