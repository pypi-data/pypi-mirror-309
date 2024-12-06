from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Convertly_LINE",
    version="0.1.2",
    long_description=long_description,  # Aquí va la descripción completa
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["docs/*"],
    },
)
