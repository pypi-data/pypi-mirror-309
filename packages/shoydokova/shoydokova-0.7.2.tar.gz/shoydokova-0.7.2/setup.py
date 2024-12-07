from setuptools import setup, find_packages

setup(
    name="shoydokova",
    version="0.7.2",  
    description="A fun API for generating jokes and funny facts",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Snezha",
    author_email="YlC9L@example.com",
    url="https://github.com/snexha/Sheg",
    packages=find_packages(include=["shoydokova", "shoydokova.*"]),
    include_package_data=True,
    package_data={"": ["*.py"]}, 
    python_requires=">=3.6",
)
