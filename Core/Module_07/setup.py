from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder_vs',
    version='0.0.1',
    description='package for sort files',
    url='https://github.com/ErizoUA',
    author='Valerii Sydorenko',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder=clean_folder_vs.clean:main']}
)
