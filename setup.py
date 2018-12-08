import setuptools

with open("README.md", "r", encoding="latin1") as fh:
    long_description = fh.read()

setuptools.setup(
      name="menzalib",
      version="0.5.22",
      author="Lettera, Francesco215",
      author_email="",
      description="Funzioni utili per lab3",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://bitbucket.org/Lettera/menza-lib/src",
      packages=setuptools.find_packages(),
      )
