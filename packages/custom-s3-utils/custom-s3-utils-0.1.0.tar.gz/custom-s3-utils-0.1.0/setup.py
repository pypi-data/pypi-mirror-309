from setuptools import setup, find_packages

setup(
    name="custom-s3-utils",
    version="0.1.0",
    description="A simple utility for handling S3 file uploads.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Rajesh Reddy Madduri",
    author_email="x23340231@student.ncirl.ie",
    url="https://github.com/yourusername/custom-s3-utils",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)