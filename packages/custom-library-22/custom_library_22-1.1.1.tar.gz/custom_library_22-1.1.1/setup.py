from setuptools import setup, find_packages

setup(
    name="custom-library_22",
    version="1.1.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A utility library for S3 file management and helper functions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/custom-library",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "boto3",
        "werkzeug",
    ],
)
