from setuptools import setup, find_packages

setup(
    name="oslc4py_domains_auto",
    version="0.1.1",
    author="Matej Grós",
    author_email="492906@mail.muni.cz",
    description="OSLC automation domain package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pajda.fit.vutbr.cz/verifit/oslc4py-domains-auto", 
    packages=find_packages(),
    install_requires=[
        "oslc4py_client>=0.1.2" 
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)