from setuptools import setup, find_packages

setup(
    name="mlops-fropych",
    version="0.0.1",
    description="A short description of the project.",
    author="Yaroslav",
    packages=find_packages(include=["mlops", "mlops.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires="~=3.10",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)