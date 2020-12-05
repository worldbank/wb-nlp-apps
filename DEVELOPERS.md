# Development workflow

This project uses the [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) paradigm.

Please create a new feature branch when working on a new exploratory project or feature.

## Setting up the environment

The project environment can be easily replicated using conda. A linux environment is needed to maintain the packages across different platforms.

A pre-push hook is available in `/ops/git/hooks/pre-push` that handles the automatic update of the environments. To use this, simply create a soft link to your git hooks: `ln -s <path-to-git hooks> /ops/git/hooks/pre-push`.

A list of excluded packages that are not available on either mac or windows should be maintained. The excluded packages are maintained in:

- `excluded.env.mac.yml`
- `excluded.env.win.yml`

#### For linux

Run `conda env create -f environment.yml`

#### For MacOS

Run `conda env create -f environment.mac.yml`

#### For Windows

Run `conda env create -f environment.win.yml`

Then, simply activate the environment using `conda activate wb_nlp`. To install the `wb_nlp` package, run this command: `python setup.py develop`. You can now import the package within the environment.

#### Adding the environment as kernel to Jupyter/Lab

```bash
$ python -m ipykernel install --user --name=wb_nlp
```

## Setting up frontend

To run the frontend component on your local machine, first add `127.0.0.1   w1lxbdatad07` into your host's `/etc/hosts` file. Then run `docker-compose -f docker-compose.yml up`.

## Note

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.

> ##### PyScaffold includes a pre-commit config
> ---
> A `.pre-commit-config.yaml` file was generated inside your project but in order to make sure the hooks will run, please don't forget to install the `pre-commit` package:

    $ cd wb_nlp
    $ # it is a good idea to create and activate a virtualenv here
    $ pip install pre-commit
    $ pre-commit install
    $ # another good idea is update the hooks to the latest version
    $ # pre-commit autoupdate
> ---
