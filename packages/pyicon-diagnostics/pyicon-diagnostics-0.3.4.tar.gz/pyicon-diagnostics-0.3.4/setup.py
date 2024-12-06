from setuptools import setup, find_packages

with open("pyicon/version.py", 'r') as f:
    version = f.read() 
    version = version.split('=')[1].replace(' ', '').replace('"', '').replace('\n', '')

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name='pyicon-diagnostics',
    version=version,
    description='Diagnostic python software package for ICON',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.dkrz.de/m300602/pyicon',
    author='The pyicon development team',
    author_email='nils.brueggemann@mpimet.mpg.de',
    install_requires=install_requires,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyic_intake = scripts.pyic_intake:main',
            'pyic_fig = scripts.pyic_fig:main',
            'pyic_sec = scripts.pyic_sec:main',
            'pyic_anim = scripts.pyic_anim:main',
       ],
    },
    classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
    ],
    setup_requires=['setuptools'],
)
