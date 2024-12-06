from setuptools import setup, find_packages

setup(
    name="entropy-classifier",
    version="1.1.0",
    author="moudgalya",
    author_email="dattu99rockstar@gmail.com",
    description="A library to calculate entropy and classify data based on uncertainty.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/moudgalya1223/LLM_business",  # Update with your repo link
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
    ],
)
