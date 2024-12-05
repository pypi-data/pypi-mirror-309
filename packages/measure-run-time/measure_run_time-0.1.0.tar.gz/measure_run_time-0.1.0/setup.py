from setuptools import setup, find_packages


setup(
    name="measure_run_time",
    version="0.1.0",
    description="A Python decorator to measure the execution time of functions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Tu Nombre",
    author_email="tu.email@example.com",
    url="https://github.com/carlos-paezf/PyPI-Measure_Run_Time-Package",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires=">=3.6"
)