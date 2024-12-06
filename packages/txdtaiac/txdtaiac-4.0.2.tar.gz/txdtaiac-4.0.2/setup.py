from distutils.core import setup
import setuptools
packages = ['taiac']
setup(name='txdtaiac',
    version='4.0.2',
    author='唐旭东',
    packages=packages,
    package_dir={'requests': 'requests'},
    install_requires=[
        "opencv-python","numpy","Pillow",
    ])