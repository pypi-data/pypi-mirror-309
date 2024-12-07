from setuptools import setup, find_packages


setup(
    name="Leones",  
    version="0.2.9",  
    author="Grupo F",
    author_email="aitor.fernandezderet@alumni.mondragon.edu",
    description="This library consists of a casino simulator, in which you can play various casino games such as black jack.",
    long_description = open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/unaidemiguel/Casino-Montepinar.git",  
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9")