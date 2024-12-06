from setuptools import setup, find_packages

setup(
    name="seven_deadly_swarms",
    version="1.0.0",
    description="A Python library to modify text based on the seven deadly sins.",
    author="Scott Davis",
    author_email="scottleedavis@gmail.com",
    url="https://github.com/scottleedavis/seven_deadly_swarms",
    packages=find_packages(),
    install_requires=[
        "openai>=0.27.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
