from setuptools import setup, find_packages

setup(
    name="Rock-Paper-scissers",
    version="0.1.0",  # Initial version
    author="Dorus Rutten",
    author_email="Dorsrutten@gmail.com",
    description="A AI that plays Rock Papier Scissers with u using the camera",
    long_description=open("README.md").read(),  # Reads your README.md for details
    long_description_content_type="text/markdown",
    url="https://github.com/Dorus-rutten/Rock-Paper-Scissers",  # Replace with your GitHub repo
    packages=find_packages(),  # Automatically finds your Python packages
    install_requires=[
        "pygame>=2.1.0",
        "numpy>=1.23.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.20',  # Corrected this line
)