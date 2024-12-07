from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Leones",
    version="0.2.2",
    author="Grupo F",
    author_email="aitor.fernandezderet@alumni.mondragon.edu",
    description="This library consists of a casino simulator, in which you can play various casino games such as black jack.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/unaidemiguel/Casino-Montepinar.git",
    packages=find_packages(),
    package_data={
        "": ["docs/*"]
    }
)
