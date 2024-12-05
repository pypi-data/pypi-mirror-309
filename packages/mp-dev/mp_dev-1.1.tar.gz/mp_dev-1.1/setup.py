# setup.py
from setuptools import setup, find_packages

setup(
    name="mp_dev",
    version="1.1",
    description="A FastAPI plugin for generating project structures",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="MarshallPierre",
    author_email="nguemazengmp@gmail.com",
    url="https://github.com/Marshall-Pierre",  # Lien vers le repo GitHub si disponible
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mp-dev = mp_dev.cli:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "pyjwt",
        "passlib[bcrypt]",
        "sqlalchemy"
    ],
)
