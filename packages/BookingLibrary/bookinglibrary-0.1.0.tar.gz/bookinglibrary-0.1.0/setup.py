from setuptools import setup, find_packages

setup(
    name="BookingLibrary",  
    version="0.1.0",  
    packages=find_packages(),  
    install_requires=[],  
    description="A simple booking management system.",
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',
    author="Mageshwaran",
    author_email="mageshwaran960@gmail.com",
    url='',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)
