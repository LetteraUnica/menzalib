import setuptools

with open("README.md", "r", encoding="latin1") as fh:
    long_description = fh.read()

setuptools.setup(
    name="menzalib",
    version="0.6.1",
    author="Menzalib Developers",
    author_email="",
    description="Funzioni utili per lab3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/Lettera/menza-lib/src",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
