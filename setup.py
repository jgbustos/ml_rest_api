"""setuptools config script"""
from setuptools import setup, find_packages

setup(
    name="ml_rest_api",
    version="0.1.0",
    description="A RESTful API to return predictions from a trained ML model,"
    " built with Python 3 and Flask-RESTX",
    url="https://github.com/jgbustos/ml_rest_api",
    author="Jorge Garcia de Bustos",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="python3 flask-restx machine-learning rest-api",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.0.0",
        "flask-restx>=0.5.0",
        "Flask-WTF>=1.0.0",
        "werkzeug>=2.0.0",
        "rfc3339-validator>=0.1.4",
        "numpy>=1.22.0",
        "pandas>=1.4.0",
    ],
)
