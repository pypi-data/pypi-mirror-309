from setuptools import setup, find_packages


setup(
    name="naiwillcallyou",
    version="2024.11.04",
    description="A tool to call you",
    url="https://github.com/T-K-233/NAI-Will-Call-You",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.10",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "requests",
    ],
    entry_points={  # Optional
        "console_scripts": [
            "callmeathere=naiwillcallyou:main",
        ],
    },
)
