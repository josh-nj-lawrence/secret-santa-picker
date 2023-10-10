import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="secret-santa-picker",
    version="0.0.1",
    author="Josh Lawrence",
    author_email="josh.nj.lawrence@gmail.com",
    packages=setuptools.find_packages(),
    description="A simple tool to pick names for secret santa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/josh-nj-lawrence/secret-santa-picker/tree/main",
    license="MIT",
    python_requires=">=3.8",
    install_requires=[]
)
