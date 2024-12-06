from setuptools import setup, find_packages

setup(
    name="mzk_aleph",
    version="1.0.0",
    description="Aleph client for multiple Aleph instances developed by MZK",
    author="Robert Randiak",
    author_email="randiak@mzk.com",
    packages=find_packages(),
    install_requires=[
        "lxml",
        "pymarc",
        "requests"
    ],
    setup_requires=["wheel"],
    extras_require={
        "yaz": ["yaz"]
    },
    python_requires=">=3.6",
)
