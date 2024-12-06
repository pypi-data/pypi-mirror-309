from setuptools import find_packages, setup

setup(
    name="worlds_creator",
    version="0.1.0",
    author="Your Name",
    author_email="benbasuni1@gmail.com",
    description="A package to create and view worlds.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sun2ii/worlds",
    license="MIT",
    packages=find_packages(include=["utils", "utils.*"]),
    py_modules=["main"],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "worlds=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
