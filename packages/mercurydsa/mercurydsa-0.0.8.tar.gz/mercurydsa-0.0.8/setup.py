from setuptools import setup, find_packages

setup(
    name="mercurydsa",
    version="0.0.8",
    author="Walter Michel Raja",
    author_email="waltermichelraja@gmail.com",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'mercurydsa-version=mercurydsa:version'
        ]
    },
)
