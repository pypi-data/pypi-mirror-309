from setuptools import find_packages, setup

setup(
    name="ehrt",
    version="0.1.1",
    author="Vidul Ayakulangara Panickan",
    author_email="apvidul@gmail.com",
    description="Toolkit for processing Electornic Health Records",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/apvidul/ehrt/",
    packages=find_packages(where="src"),  # Look for packages inside 'src/'
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
