from setuptools import setup, find_packages

setup(
    name="meta-ads-cli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "facebook-business>=22.0.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "meta-ads=meta_ads.cli:main",
        ],
    },
    python_requires=">=3.10",
)
