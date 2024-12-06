from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',          
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3', 
]

setup(
    name='louay_ml_library',
    version='0.0.2',
    author='Louay El Masri',
    author_email='masrilouay5@gmai.com',
    description='A custom machine learning library containing several models',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/louay01/louay_ml_library',
    packages=find_packages(),
    keywords='machine learning linear regression linear classifier neural networks decision trees SVM AI',
    license='MIT',
    classifiers=classifiers,
    install_requies=[
        'numpy'
    ]
)