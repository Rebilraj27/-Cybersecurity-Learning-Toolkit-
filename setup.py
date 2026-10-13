"""Legacy setup.py — see pyproject.toml for modern config."""
from setuptools import setup, find_packages

setup(
    name="cyber-toolkit",
    version="1.0.0",
    author="Rebilraj",
    description="A Python-based cybersecurity learning toolkit",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.9",
    install_requires=[
        "scapy>=2.5.0",
        "requests>=2.31.0",
        "rich>=13.7.0",
        "bcrypt>=4.1.2",
        "cryptography>=42.0.5",
    ],
    entry_points={"console_scripts": ["cyber-toolkit=cli:main"]},
)
