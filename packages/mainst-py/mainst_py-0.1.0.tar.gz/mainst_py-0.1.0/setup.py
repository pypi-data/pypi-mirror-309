from setuptools import setup, find_packages

setup(
    name="mainst_py",
    version="0.1.0",
    author="Fernando Basurto Echevarria",
    author_email="fernando.basurto.echevarria@gmail.com",
    description="Yet Another Math Library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fbasurto/yaml",  # Replace with your repo
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
