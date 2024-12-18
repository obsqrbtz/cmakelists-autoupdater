from setuptools import setup, find_packages

setup(
    name="cmakelists-updater",
    version="1.0.1",
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
    author="obsqrbtz",
    author_email="dan@obsqrbtz.space",
    url="https://github.com/obsqrbtz/cmakelists-autoupdater",
    keywords="cmake, automation, updater",
)