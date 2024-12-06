## DEVELOPMENT

Please help develop this module if you are interested!


### GET THE CODE
Clone from gitlab:
```bash
git clone https://gitlab.com/MAXIV-SCISW/JUPYTERHUB/jnbv.git
cd jnbv/
```


### VIRTUAL ENVIRONMENT INSTALLATION
The virutal environment can be installed either via the included makefile or
by hand.

For this project, the testing routines need to be run in a conda environment.
Using the makefile:
```bash
make venv
```

![makefile_help](screenshots/makefile_help.png)


To install by hand, first install conda:
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh
sh Miniconda3-py39_4.9.2-Linux-x86_64.sh -s -p venv -b
rm Miniconda3-py39_4.9.2-Linux-x86_64.sh
```

Then install the requirements for the validation scripts into the virtual
environment:
```bash
source venv/bin/activate
conda env update --name base --file development/venv-requirements.yml
```

### RUN TESTS
Testing is done using [pytest](https://docs.pytest.org/) with environments
created using [tox](https://tox.readthedocs.io/en/latest/index.html)
along with the plugin [tox-conda](https://github.com/tox-dev/tox-conda).

A comprehensive set of tests has been setup to run with python versions 3.6,
3.7, 3.8, and 3.9. See the [tox configuration](tox.ini) for more information.

The tests can be executed with tox or pytest, or with several makefile targets,
for example to run tests of the execution function:
```bash
make tox-execution-tests
```

This will create the virtual environments, source that environment,
and then use tox to run pytest.  Doing this without the makefile, one would
enter:
```bash
source venv/bin/activate
tox -e "py3{6,7,8,9}-execution-tests-{valid,invalid}-kernel"
```

tox is configured in (tox.ini)[tox.ini], and when executed as above will:
- create virtual environments with conda (placed for example in
  .tox/py39-execution-tests-valid-kernel)
- install dependencies with pip that are under "deps" in tox.ini
- install dependencies with conda that are specified in the yaml file under
  "conda_env"
- build with 'python setup.py sdist'
- install jnbv
- execute pytest on the functions in tests/test_execute_notebook.py

Tests exist aswell for reading, testing, comparing, and validating notebooks.

There is also a test of the terminal execution that can be run:
```bash
make tox-validation-tests-cli
```

which uses tox to execute the command:
```bash
source venv/bin/activate
jnbv tests/example-hdf5-notebook.ipynb --kernel python3 --validate
```

To see all tests available:
```bash
source venv/bin/activate
tox -l
```


### RUN LINTER
Use flake8 to lint the code with:
```bash
make tox-lint
```

or:
```bash
source venv/bin/activate
tox -e lint
```


### DEVELOP MODE
Activate the environment and install jnbv into it:
```bash
source venv/bin/activate
pip install -e .
```

This installs jnbv into the virtual environment, and allows one to use the
entry_points defined in setup.cfg, and when code is changed, the changes are
immediately available for use.

See the help output with:
```bash
jnbv
```

![jnbv_help](screenshots/jnbv_help.png)


Use the module in a python terminal:
```bash
python
```
```python
>>> from jnbv import compare
>>> compare.dummy_test()
```


### DEVELOP MODE IN RUNNING INSTALLATION
To develop jnbv while using a running installation of JupyterHub, start a
JupyterLab session, then activate the base environment, which is will be
something like:
```bash
source activate /opt/conda
```

Then get the jnbv code, and install jnbv from the repository:
```bash
git clone https://gitlab.com/MAXIV-SCISW/JUPYTERHUB/jnbv.git
cd jnbv/
pip install -e .
```

Make changes to the jnbv code, then test out resulting executions, for
example:
```bash
jnbv --validate \
    --kernel maxiv-jhub-docker-kernel-hdf5 \
    08-azint-benchmark.ipynb
```

When satisfied, commit and push changes like usual.


### BUMP VERSION
For the present, versioning is done simply as a date stamp in the version line
in setup.cfg plus a count of the number of version tags made for the day, for
example:
```bash
version = 2021.6.22.3
```

The CI is made to trigger the uploading of a new build only when there is a
new tag, which can be done for example like this:
```bash
git tag 2021.6.22.3
```

Which would then needed to be pushed to gitlab:
```bash
git push origin 2021.6.22.3
```

A makefile target has been created to simplify this procedure:
```bash
make bump-version
```
This then does the following, for example with the date of 2021.6.22:
- Sets new version number in setup.cfg
    - `sed -i "/^version =.*/ s//version = 2021.6.22.3/" setup.cfg`
- Commits the changes to git
    - `git add -A`
    - `git commit -m "bumped version in setup.cfg to 2021.6.22.3"`
- Does a git tag
    - `git tag 2021.6.22.3`
- Remakes the changelog file

The final push of the tag is left to be done by hand, so that one can double
check things first.  After it is all sent off to gitlab, the package will
then be built and uploaded to PyPi, and some 6 hours or so later a github bot
will have also uplodade the new package version to conda-forge.
```bash
git push 2021.6.22.3
```

Here's a screenshot of this running:

![make-bump-version](screenshots/make-bump-version.png)


### BUILD PACKAGE
The CI takes care of the building, but it can also be done by hand in the
terminal.

Using the Makefile:
```bash
make build
```

Or directly with python:
```bash
source venv/bin/activate
./venv/bin/python3 setup.py sdist bdist_wheel
```

### UPLOAD PYPI PACKAGE
The CI takes care of the uploading, but it can also be done by hand in the
terminal.

After building, upload to either [TestPyPi](https://test.pypi.org/):
```bash
make upload-testpypi
    <enter username>
    <enter password>
```

or to [PyPi](https://pypi.org/):
```bash
make upload-pypi
    <enter username>
    <enter password>
```

Directly with python, uploading is done like this:
```bash
source venv/bin/activate
python3 -m twine upload --repository testpypi dist/*
    <enter username>
    <enter password>
```

![twine_upload_success](screenshots/twine_upload_success.png)

Then view uploaded content:
- [PyPi - jnbv](https://pypi.org/project/jnbv/)
- [TestPyPi - jnbv](https://test.pypi.org/project/jnbv/)

![pypi_jnbv](screenshots/pypi_jnbv.png)


### UPLOAD CONDA PACKAGE
A conda package was created in the conda-forge channel:

[conda-forge jnbv](https://anaconda.org/conda-forge/jnbv)

![conda-forge-jnbv](screenshots/conda-forge-jnbv.png)

And new versions of the package are uploaded to conda-forge via this
repository:
- [jnbv-feedstock](https://github.com/conda-forge/jnbv-feedstock)

Github has an automatic bot running (~every 6 hours) which detects new versions
of packages on PyPi, and when a new version is found, a pull request with an
updated version number for the package is sent to the jnbv-feedstock.  The
feedstock repository is setup to automatically accept the pull request, and the
new package version will then shortly (< 30 minutes) be made available in
conda-forge.


### RUN EXAMPLES
In this repository there is an example kernel environment, dataset, and Jupyter
notebook which can be tested or used as an example for the creation of other
kernels:
```bash
development/
├── example-data.h5
├── example-hdf5-notebook.ipynb
└── hdf5-kernel-env.yml
```

The testing procedures using tox already have this example kernel and dataset
in use, and they can also be run by hand in the terminal when developing,
There are several steps in the creation of the kernel, so use of the makefile
target is advised for this:
```bash
make hdf5-kernel
```

Then one can make use of the kernel:
```bash
make cli-execution
```

Or more explicitly:
```bash
source venv/bin/activate
jnbv development/example-hdf5-notebook.ipynb --kernel hdf5-kernel --validate
```

In either case, you should then see some output in the terminal that begins
with:

![cli-execution-start](screenshots/cli-execution-start.png)


And finishes with:

![cli-execution-end](screenshots/cli-execution-end.png)


### PACKAGE UPDATES

Update to the PyPi and conda-forge packages ought to be done via the CI.

The gitlab CI for this project is setup to:
- Lint the code with python 3.9
- Build the package using python 3.6, 3.7, 3.8, 3.9
- Execute pytest to run all tests in the directory tests/ using python 3.6,
  3.7, 3.8, 3.9
  - These tests include executions of the validation routines using an
    example kernel and dataset
- Execute the validation routines using jnbv in the command line along using
  python 3.6, 3.7, 3.8, 3.9

Then if a new tag is pushed to gitlab, the CI will also:
- Build the package
- Upload the package to PyPi

See the [CI config file](.gitlab-ci.yml) for more.

The conda-forge package will be rebuilt after the PyPi is uploaded, as
mentioned in the above section [UPLOAD CONDA PACKAGE](#upload-conda-package).
