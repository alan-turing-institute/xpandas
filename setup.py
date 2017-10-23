from setuptools import setup, find_packages


setup(name='XPandas',
      version='1.0.2',
      description='1d/2d data container with map-reduce transformers',
      url='https://github.com/alan-turing-institute/xpandas',
      author='Vitaly Davydov (@iwitaly)',
      author_email='1061040@gmail.com',
      license='BSD',
      keywords='data container sklearn pandas map reduce transformer',
      packages=find_packages(),
      zip_safe=False)