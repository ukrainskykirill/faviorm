import os
from pathlib import Path

from setuptools import find_packages, setup  # type: ignore [import]


setup(
    name="faviorm",
    version=os.environ["GITHUB_REF_NAME"],
    description="ASGI webserver",
    author="Vladimir Vojtenko",
    author_email="vladimirdev635@gmail.com",
    license="MIT",
    packages=find_packages(exclude=["__tests__*"]),
    include_package_data=True,
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
)
