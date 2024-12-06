from setuptools import setup, find_packages

setup(
    name="mlops-ivan-pleshakov",
    version="0.0.2",
    description="mlops misis",
    author="IvanPleshakov",
    packages=find_packages(include=["mlops", "mlops.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires="~=3.10",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
