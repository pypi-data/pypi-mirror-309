from setuptools import setup, find_packages

setup(
    name="appointment-workflow-manager",
    version="0.2.0",
    description="Utilities to manage appointment workflows including approval, rejection, cancellation, audit logging, and conflict detection.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vinay Gunda",
    author_email="x23302712@student.ncirl.ie",
    url="https://github.com/yourusername/appointment-workflow-manager",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "Django>=3.2",  # Adjust based on your Django version
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
