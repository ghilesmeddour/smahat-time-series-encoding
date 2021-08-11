import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smahat",
    version="0.0.1",
    author="Ghiles Meddour",
    author_email="ghiles.meddour@munic.io",
    description="Smahat Time Series Encoding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghilesmeddour/smahat-time-series-encoding",
    project_urls={
        "Bug Tracker":
        "https://github.com/ghilesmeddour/smahat-time-series-encoding/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "bitarray",
    ],
)
