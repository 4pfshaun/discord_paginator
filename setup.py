from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
desc = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="discord_paginator",
    version="1.0",
    description="A module which allows easy implementation of button pagination for your embeds",
    long_description=desc,
    long_description_content_type="text/markdown",
    author="prettylittlelies",
    url="https://github.com/prettylittlelies/discord_paginator",
    python_requires=">=3.8",
    packages=find_packages(include=["discord_paginator", "discord_paginator.*"]),
)