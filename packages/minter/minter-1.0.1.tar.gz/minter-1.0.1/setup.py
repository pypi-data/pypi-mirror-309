from setuptools import setup, find_packages

setup(
    name="Minter",
    version="1.0.1",
    description="a lib to mint nft's on any EVM chain",
    long_description="Minter: A Python library for fast, effortless minting of NFTs from collections on EVM-compatible networks. Simplify blockchain integration with ease.",
    author="SpicyPenguin",
    packages=["Minter", "Minter.types", "Minter.types.abis", "Minter.storage", "Minter.data"],
    include_package_data=True,
    package_data={"": ["*.json"]},
    install_requires=["kvsqlite", "web3"]
)