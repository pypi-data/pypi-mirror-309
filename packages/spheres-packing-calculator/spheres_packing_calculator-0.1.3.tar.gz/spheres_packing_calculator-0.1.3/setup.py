from setuptools import setup, find_packages

setup(
    name="spheres_packing_calculator",
    version="0.1.3",
    description="Calculates a precise packing density for spherical particles in a 3D Cartesian region",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="GPL-3.0-only",
    author="Freddie Barter",
    author_email="fjbarter@outlook.com",
    python_requires=">=3.6",
    packages=find_packages(where=".", include=["spheres_packing_calculator*"]),
    install_requires=[
        "numpy",
        "scipy",
        "pyvista"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
