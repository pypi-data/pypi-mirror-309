from setuptools import setup

setup(
    name="bananopie_bns",
    url="https://github.com/jetstream0/bananopie_bns",
    author="John Though",
    author_email="prussia@prussia.dev",
    packages=["bananopie_bns"],
    install_requires=["bananopie"],
    version="0.0.1",
    license="MIT",
    description="A python library to simplify sending and receiving Banano. Also a RPC wrapper.",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5"
)
