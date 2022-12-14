from setuptools import setup, find_packages

PACKAGES = find_packages(exclude=['tests', 'tests.*'])

REQUIRES = [
    'aiohttp==3.8.1',
    'beautifulsoup4==4.10.0'
]

setup(
    name='py-cozi',
    version='1.0.0',
    author="Cody Wetzel",
    author_email="wetzelredistribution@gmail.com",
    keywords='unoffical Cozi api',
    description="Cozi Unofficial Python Package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Wetzel402/py-cozi",
    license='MIT',
    packages=PACKAGES,
    include_package_data=True,
    python_requires='>=3.5',
    zip_safe=False,
    install_requires=REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
