from setuptools import setup, find_packages

setup(
    name="cmakelists-updater",
    version="0.1.0",
    description="A tool to auto-update CMakeLists.txt when source files change.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyyaml==6.0.2",
        "watchdog==6.0.0"
    ],
    entry_points={
        "console_scripts": [
            "cmakelists-updater=cmakelists_updater:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)