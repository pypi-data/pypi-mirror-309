from setuptools import find_packages, setup

with open("src/wyge/README.md", "r") as f:
    long_description = f.read()

setup(
    name="wyge",
    version="1.0.2",
    description="A python package for generative ai",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prudvireddyNS/vyzeai",
    author="Prudvi",
    author_email="prudhvisneha2003@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=['openai', 'requests', 'numpy', 'pydantic[email]'],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)