from setuptools import setup, find_packages

setup(
    name="spikeweb",  # Replace with your package name
    version="0.1.0",  # Choose an appropriate version
    packages=find_packages(),  # Automatically find all packages in your directory
    install_requires=[  # List any dependencies your package needs
        "requests",  # Example dependency
    ],
    author="saber_x123",
    author_email="yoyue@happy@gmail.com",
    description="creating a web basic folder struture requirment",
    classifiers=[  
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
