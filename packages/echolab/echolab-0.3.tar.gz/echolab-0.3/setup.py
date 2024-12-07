from setuptools import setup, find_packages

## Configure Test-PyPI/PyPI infos for the current version 
## Need to be run before uploading a new version, or to change any information 

setup(
    name="echolab", # Nom du package
    version='0.3',  # Version initiale    
    packages=find_packages(),  # Recherche des packages
    description="A simple hello world library",
    long_description="""
    This is a simple hello world library in Python. 

    Commit SHA : <commit_sha>
    """,
    author="Jiayi & Léo",
    author_email="ido-dam-he@proton.me",
    url="https://gitlab.polytech.umontpellier.fr/leo.damerval/ido-dam-he",
    install_requires=[]  # Pas de dépendances externes
)