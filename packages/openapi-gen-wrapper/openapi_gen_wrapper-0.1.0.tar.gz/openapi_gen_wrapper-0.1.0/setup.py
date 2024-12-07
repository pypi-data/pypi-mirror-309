from setuptools import setup, find_packages

setup(
    name="openapi-gen-wrapper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click", "pyyaml"],
    entry_points={
        'console_scripts': [
            'openapi-gen=src.cli:main'
        ]
    },
    author="Arkodeep Sen",
    author_email="arkodeepsen72@gmail.com.com",
    description="An OpenAPI generator for Flask apps.",
    url="https://github.com/arkodeepsen/openapi-gen",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
