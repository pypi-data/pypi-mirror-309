from setuptools import setup, find_packages

with open("mercurydsa/README.md", "r", encoding="utf-8") as f:
    description=f.read()

setup(
    name="mercurydsa",
    version="0.0.11",
    description="python package to implement data structures",
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
    long_description=description,
    long_description_content_type="text/markdown"
)
