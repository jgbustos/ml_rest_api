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
    ],
    keywords="python3 flask-restx machine-learning rest-api",
    packages=find_packages(),
    install_requires=[
        "Flask>=1.0",
        "flask-restx>=0.1.0",
        "werkzeug>=1.0.1",
        "strict-rfc3339>=0.7",
        "numpy>=1.18.0",
        "scipy>=1.4.0",
        "pandas>=1.0.1",
        "scikit-learn>=0.22.0",
        "lightgbm>=2.3.0",
        "xgboost>=0.90",
        "tensorflow>=2.1.0",
        "keras>=2.3.0",
        "nltk>=3.4.5",
        "mypy>=0.761",
    ],
)
