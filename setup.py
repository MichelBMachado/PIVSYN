from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
      name = 'pivsyn',
      version = '0.0.1',
      description = 'Particle image velocimetry synthetic dataset tools',
      url = '',
      author = 'Michel Bernardino Machado',
      author_email = 'michelbernardinomachado@gmail.com',
      license = 'MIT',
      packages = ['pivsyn'],
      install_requires = ['numpy'],
      include_package_data = True,
      zip_safe = False
)