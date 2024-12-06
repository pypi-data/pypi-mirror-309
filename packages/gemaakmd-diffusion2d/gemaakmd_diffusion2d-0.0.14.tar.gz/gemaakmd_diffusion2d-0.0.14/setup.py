from setuptools import setup
import setuptools

# Read the README.md file. so this shows up as the Project Description in the PyPI/TestPyPI page.
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gemaakmd_diffusion2d",
    version="0.0.14",
    author="Muhammad Gema Akbar",
    description="SSE Python Exercise",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    url="https://github.com/mgemaakbar/diffusion2D",
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    install_requires=[
        "matplotlib>=3.9.0",
        "numpy>=2.1.0"
    ]
    # entry_points={
    #   'console_scripts': ['package-import-name = <path-to-main-function-with-dots>']
    # }
)