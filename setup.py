import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyspfc",
    version="0.0.1",
    author="Anjo Niewöhner",
    author_email="aniewoeh@th-koeln.de",
    description="PySPFC - Python for simple power flow calculations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Metalgurke/PySPFC",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)