import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shopwareapi",
    version="0.1.26",
    author="Stefan Eiermann, Sachs Media",
    author_email="support@sachs-media.com",
    description="Provides a Python (object-based) API for Shopware",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Sachs-Media/shopwareapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries"
    ],
    install_requires=["requests>=2.25.0"],
    python_requires='>=3.6',
)