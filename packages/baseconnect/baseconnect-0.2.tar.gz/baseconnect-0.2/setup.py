from setuptools import setup, find_packages

setup(
    name="baseconnect",
    version="0.2",
    description="Database connection library for SQL Server",
    author="Domiter Dominik",
    author_email="dominik.domiter@autowallis.hu",
    url="https://github.com/Domiterd/BaseConnect",
    packages=find_packages(),
    install_requires=[
        "pyodbc",
        "pandas",
    ],
    python_requires=">=3.6, <4",  # Megadja a kompatibilis Python verziókat
)