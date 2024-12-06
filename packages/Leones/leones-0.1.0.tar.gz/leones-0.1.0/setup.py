from setuptools import setup, find_packages

setup(
    name="Leones",
    version="0.1.0",
    author="Unai de Miguel Bilbao, Unai Martinez Leal, Asier López Bárcena, Aitor Fernandez de Retana",
    author_email="unai.demiguel@alumni.mondragon.edu, unai.martinez@alumni.mondragon.edu, asier.lopezb@alumni.mondragon.edu, aitor.fernandezderet@alumni.mondragon.edu",
    maintainer="Unai de Miguel Bilbao",
    maintainer_email="unai.demiguel@alumni.mondragon.edu",
    description="This library consists of a casino simulator, in which you can play various casino games such as black jack.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/unaidemiguel/Casino-Montepinar.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"],
    python_requires='>=3.6',
)
