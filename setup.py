import sun
from setuptools import find_packages, setup


def read(f):
    return open(f, 'r', encoding='utf-8').read()


# https://pip.pypa.io/en/latest/user_guide/#fixing-conflicting-dependencies
INSTALL_REQUIREMENTS = read('requirements.txt').splitlines()

setup(
    name='sun-core',
    version=sun.__version__,
    description='基于FastAPI和gRPC轻量级微服务开发框架',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/xqk/sun',
    author='xqk',
    author_email='xiaqiankun@outlook.com',
    license='Apache License 2.0',
    install_requires=INSTALL_REQUIREMENTS,
    packages=find_packages(
        exclude=['examples', 'examples.*', 'tests', 'docker', 'docs']
    ),
    package_data={'sun': ['db/*.pyi']},
    include_package_data=True,
    zip_safe=False,
)
