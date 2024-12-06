from setuptools import setup

setup(
    name="python-pod-manager",
    version="1.0.0b4",
    author="Hakan İSMAİL",
    author_email="hakanismail53@gmail.com",
    description="A pod manager for version dependency python projects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license=open("LICENSE").read(),
    url="https://gitlab.com/Hakanbaban53/python-pod-manager",
    package_data={
        "": ["LICENSE", "README.md"],
        "core": ["core/*"],
        "utils": ["utils/*"],
    },
    entry_points={
        'console_scripts': [
            'pypodmanager=pypodmanager.utils.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyyaml",
        "psutil",
        "colorama",
    ],
)
