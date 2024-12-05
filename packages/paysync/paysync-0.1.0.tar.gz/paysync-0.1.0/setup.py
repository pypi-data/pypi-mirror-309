from setuptools import setup, find_packages

setup(
    name="paysync",
    version="0.1.0",
    description="A Python client for the PaySync payment gateway",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KenedyMoremi/pay_py",
    author="Tumisang Moremi",
    author_email="moremikenedy@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    python_requires=">=3.6",
)
