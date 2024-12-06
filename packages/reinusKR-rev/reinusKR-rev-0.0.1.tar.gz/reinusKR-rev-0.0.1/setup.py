from setuptools import setup, find_packages

setup(
    name="reinusKR-rev",
    version="0.0.1",
    description="reverse shell utility, for RCE to use pip",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="reinusKR",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "reinusKR-rev=reinusKR_rev.reinusKR_rev:connect"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)