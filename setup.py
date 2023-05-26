from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    description = f.read()
    f.close
    
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()
    f.close

setup(
      name = 'SPIVUtils',
      version = '0.0.1',
      description = description,
      url = 'https://github.com/MichelBMachado/SPIVUtils',
      author = 'Michel Bernardino Machado',
      author_email = 'michelbernardinomachado@gmail.com',
      license = 'MIT',
      packages = find_packages(),
      install_requires = requirements,
      include_package_data = True,
      zip_safe = False
)