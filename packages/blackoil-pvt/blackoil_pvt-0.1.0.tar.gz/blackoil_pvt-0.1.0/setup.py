from setuptools import setup, find_packages

setup(
    name="blackoil_pvt",
    version="0.1.0",
    description="A library for calculating black oil PVT properties using the Standing method.",
    author="Mohamed ElSersy",
    author_email="mrsersy@gmail.com",
    url="https://github.com/MElSersy/blackoil-pvt",  # Update with your repository URL
    packages=find_packages(),
    install_requires=[],  # Add dependencies if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
