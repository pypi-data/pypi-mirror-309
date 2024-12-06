from setuptools import setup, find_packages

setup(
    name='prprint',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],  # Add any dependencies if needed
    description='An enhanced pprint module with additional features.',
    long_description=open('README.md').read(),  # Ensure README.md exists
    long_description_content_type='text/markdown',
    author='Lovely Cobra',
    author_email='elene.yeti@web.de',
    url='https://github.com/yourusername/prprint',  # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',  # Specify compatible Python versions
)
