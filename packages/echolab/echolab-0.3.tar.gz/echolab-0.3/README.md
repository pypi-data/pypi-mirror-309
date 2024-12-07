# EchoLab

Simple to use Python Library to say hello to us atm.

## Description

This library was made for a school project to exercice on the CI/CD setup on GitLab.

The update and uploading process to Test-PyPI and PyPI of this library is fully automated through a simple git push.

### [In the future]

We will add a way to install it with apt (using a .deb package) for everyone to use it without needing to install a python virtual env on some systems.

## Installation 

### 1st and unique way

For the moment, we are in the testing and development phase of this library, and it's only available on Test-PyPI.

To install it, run this command, having python and pip installed already :

```bash
pip install --index-url https://test.pypi.org/simple/ echolab
```

### 2nd way [NOT AVAILABLE ATM]

Using PyPI servers also with pip :

```bash
pip install echolab
```

### 3rd way [NOT AVAILABLE ATM]

Using the .deb package using apt

```bash
apt install echolab
```

## Usage

Our only feature for the moment, a simple Hello! (to us... the creators :) )

***helloworld()*** :

```python
import echolab as el

# Example usage
yosh = el.helloworld()

print(yosh)
```

The printed result will be :

>**Hello, leo! Hello jiayi !**

## Who are we ?

Two students in the last year Computer Science departement of the french Polytech Montpellier school, Jiayi and Léo !

## License

Should we really need a license for this ?

## Changelog

### 0.1
*2024-09-24*

- Simple hello to us 

## CI/CD Pipeline

Our project uses GitLab CI/CD pipelines for automating the build and deployment of the Python library.

### Pipeline Overview

**Stages**

- Build: This stage creates a source package (sdist) from the code.
- Deploy: This stage uploads the package to either Test-PyPI or PyPI, depending the chosen target.

**Variables**

- PYTHON_VERSION: The Python version used in the pipeline (e.g., 3.11).

- PYPI_UPLOAD_REPO_URL & TEST_PYPI_UPLOAD_REPO_URL: URLs for PyPI and Test-PyPI repositories.

- PYPI_CHECK_REPO_URL & TEST_PYPI_CHECK_REPO_URL: URLs to check if the package version already exists.

### Build Stage

The pipeline installs Python 3.11 and runs the setup.py sdist command to create the source package.

The package is stored in the dist/ folder.

### Deploy Stage

The pipeline installs Twine to upload the package.

It checks if the current version of the package (defined in the setup.py file) is the same as available on the repository (Test-PyPI or PyPI).

If this version does not exist, the package is uploaded to the appropriate repository.

**Targeting Test-PyPI or PyPI**

The pipeline uses the $PYPI_TARGET variable to determine whether to deploy to Test-PyPI or PyPI.
- If the variable is set to : "**test**" in GitLab 
  - deployed on Test-PyPI
- Anything else
  - deployed on PyPI

Test-PyPI is used for testing the deployment process, while PyPI is the official repository for the package.

### Automation

The deployment only happens if the package version doesn't already exist, ensuring no duplicate versions are uploaded.