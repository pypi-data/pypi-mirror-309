from setuptools import find_packages, setup

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="ConnKeeper",
    version="0.0.10",
    description="Allows to save, manage and efficiently use rdbms connections and store them locally in one location.",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ankit48365/ConnKeeper",
    author="Ankiz",
    author_email="ankit48365@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["PyYAML>=6.0.2","SQLAlchemy<=2.0.36","psycopg2>=2.9.10", "pandas>=2.2.3", "pyodbc>=5.2.0"],
    # install_requires=["PyYAML","SQLAlchemy","psycopg2", "pandas", "pyodbc"],

    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
