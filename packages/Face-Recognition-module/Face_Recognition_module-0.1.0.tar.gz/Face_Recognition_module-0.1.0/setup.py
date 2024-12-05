from setuptools import setup, find_packages

setup(
    name='Face_Recognition_module',
    version='0.1.0',
    description='A Python package for facial recognition using DeepFace',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Aditya Seth',
    author_email='adityaseth936@gmail.com',
    url='https://github.com/AdityaSeth0905/Xyrionix-Labs-Codebase.git',  
    packages=find_packages(),  
    install_requires=[  
        'opencv-python',
        'deepface',
        'tensorflow',
        'pathlib',
    ],
    classifiers=[  
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12.4',
)
