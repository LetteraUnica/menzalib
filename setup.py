import setuptools

with open("README.md", "r", encoding="latin1") as fh:
    long_description = fh.read()

setuptools.setup(
    name="menzalib",
    version="0.8.4",
    author=["Lorenzo Cavuoti", "Francesco Sacco"],
    author_email=["lorenzocav97@gmail.com", "francesco215@live.it"],
    description="Funzioni utili per lab3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LetteraUnica/menzalib",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'numdifftools',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License ::  MIT License",
        "Operating System :: OS Independent",
    ]
)
