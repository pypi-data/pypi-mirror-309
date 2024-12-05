from pathlib import Path
from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description_mkd = (this_directory / "README.md").read_text()

setup(
    name='gotohuman',
    packages=find_packages(),
    version='0.1.1',
    description='Python SDK for gotoHuman',
    long_description=long_description_mkd,
    long_description_content_type="text/markdown",
    keywords="gotohuman ai agents llm automation human-in-the-loop",
    url="https://gotohuman.com",
    project_urls={
        "Documentation": "https://docs.gotohuman.com/",
        "Twitter": "https://twitter.com/gotohuman",
    },
    author='gotoHuman',
    author_email='founders@gotohuman.com',
    install_requires=[
      'requests'
    ],
    python_requires=">=3.8",
    license="GPL-3.0"
)