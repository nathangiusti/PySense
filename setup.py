import setuptools


with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PySenseSDK",
    version="0.2.18",
    author="Nathan Giusti",
    author_email="nathanggiusti@gmail.com",
    description="Sisense Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nathangiusti/PySense",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
       'requests',
       'PyYAML'
    ],
)
