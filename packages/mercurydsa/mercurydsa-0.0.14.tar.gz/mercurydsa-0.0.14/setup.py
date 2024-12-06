from setuptools import setup, find_packages
from mercurydsa.src import version


with open("mercurydsa/README.md", "r", encoding="utf-8") as f:
    description=f.read()

setup(
    name="mercurydsa",
    version=version(),
    description="python package to implement data structures",
    author="Walter Michel Raja",
    author_email="waltermichelraja@gmail.com",
    packages=find_packages(where="."),
    package_dir={"": "."},
    install_requires=[],
    entry_points={
        'console_scripts': [
            'mercurydsa-version=mercurydsa.src.cli:mercurydsa_version'
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9"
        ]
)
