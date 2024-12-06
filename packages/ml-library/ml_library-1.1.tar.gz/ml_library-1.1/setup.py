from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]


setup(
      name='ml_library',
      version='1.1',
      description='Machine learning algorithms for regression and classification',
      long_description= open('README.txt').read(),
      author='Souhayla Touk',
      author_email='souhayla.tawk11@gmail.com',
      url='',
      license= 'MIT',
      classifiers= classifiers,
      packages= find_packages(),
      install_requires= ['Numpy']
     )