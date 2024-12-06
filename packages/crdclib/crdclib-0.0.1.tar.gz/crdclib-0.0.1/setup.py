from setuptools import setup, find_packages
import pathlib

thispath = pathlib.Path(__file__).parent.resolve()
long_description = thispath / "README.md"

setup(
    name="crdclib",
    version="0.0.1",
    description="Random routines I use in CRDC work",
    long_description=long_description,
    url="https://github.com/pihltd/CRDCLib",
    author="Todd Pihl",
    author_email="todd.pihl@gmail.com",
    classifiers=[
        "Developement Status ::  3 - Alpha"
        "License :: OSI Approved :: Apache Software License"
        "Programming Language :: Python :: 3"
        "Programming Language :: Python :: 3.7"
        "Programming Language :: Python :: 3.8"
        "Programming Language :: Python :: 3.9"
        "Programming Language :: Python :: 3.10"
        "Programming Language :: Python :: 3.11"
        "Programming Language :: Python :: 3.12"
    ],
    package_dir={"": "src/crdclib"},
    packages=find_packages(where="src/crdclib"),
    python_requires=">=3.6",
    install_requires=["requests", "pyyaml"],
    project_urls={
        "Source": "https://github.com/pihltd/CRDCLib",
        "Issues": "https://github.com/pihltd/CRDCLib/issues"
    }
)
