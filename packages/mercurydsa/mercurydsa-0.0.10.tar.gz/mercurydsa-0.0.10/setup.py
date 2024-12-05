from setuptools import setup, find_packages

setup(
    name="mercurydsa",
    version="0.0.10",
    description="data structures made easy as a py package",
    author="Walter Michel Raja",
    author_email="waltermichelraja@gmail.com",
    packages=find_packages(where="."),
    package_dir={"": "."},
    install_requires=[],
    entry_points={
        'console_scripts': [
            'mercurydsa-version=mercurydsa:version'
        ]
    },
)
