from setuptools import setup, find_packages

setup(
    name='django-variable',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=5',
    ],
    description='Django Variable',
    long_description=open('README.rst').read(),
    long_description_content_type='text/markdown',
    author='Jeisson Perez Molano',
    author_email='jeissonp@gmail.com',
    url='https://github.com/jeissonp/django-variable',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)