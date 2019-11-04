from setuptools import setup, find_packages

with open("README.md", encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name="pyspfc",
    version="0.0.1",
    author="Christian Klosterhalfen (TH Köln), Anjo Niewöhner (TH Köln)",
    author_email="aniewoeh@th-koeln.de",
    description="PySPFC - Python for simple power flow calculations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anjoniewo/PySPFC",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent"],
    install_requires=['pandas']
)
