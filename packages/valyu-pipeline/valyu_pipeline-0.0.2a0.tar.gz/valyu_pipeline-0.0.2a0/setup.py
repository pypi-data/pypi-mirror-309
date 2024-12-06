from setuptools import setup, find_packages

setup(
    name="valyu-pipeline",
    version="0.0.2a",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "PyMuPDF",
        "tqdm",
        "Pillow",
    ],
    author="Valyu.Network",
    author_email="harvey@valyu.network",
    description="A Python package for accessing the Valyu Data pipeline infrastructure",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
)