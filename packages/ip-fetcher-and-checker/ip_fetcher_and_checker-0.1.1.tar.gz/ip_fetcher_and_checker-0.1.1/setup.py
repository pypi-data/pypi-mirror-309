from setuptools import setup, find_packages

setup(
    name="ip_fetcher_and_checker",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["requests"],  # Add any dependencies if needed
    author="Yukendiran",
    author_email="yukendiranjayachandiran@gmail.com",
    description="A tool for fetching ip.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Yukendiran2002/fetch_ip",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
