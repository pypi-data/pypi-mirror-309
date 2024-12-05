from setuptools import setup, find_packages

setup(
    name="dnd-firefly",
    version="0.4.1",
    packages=find_packages(),
    keywords = ["firefly","visualization", "astronomy","images", "tables","fits", "parquet", "votable", "csv", "tsv"],
    author="Emmanuel Joliet",
    author_email="ejoliet@caltech.edu",
    description="Programmatically drag-and-drop in IRSA Viewer (Firefly) tool via Upload feature",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ejoliet/dnd-firefly.git",
    project_urls={
        'Source': 'https://github.com/ejoliet/dnd-firefly.git',        
        'Issues': 'https://github.com/ejoliet/dnd-firefly/issues',
        'Say Thanks!': 'https://buymeacoffee.com/Red2Green',
    },
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: User Interfaces",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",  # Minimum Python version
    entry_points={
        "console_scripts": [
            "dnd_firefly=app.dnd_firefly:main",
        ],
    },
)
