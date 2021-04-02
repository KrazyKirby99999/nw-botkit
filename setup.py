from setuptools import setup, find_namespace_packages

setup(name='nw-botkit',
      url="https://github.com/KrazyKirby99999/nw-botkit",
      author_email="krazykirby99999@gmail.com",
      version='0.0.3',
      license='AGPLv3',
      packages=find_namespace_packages(include=['nw.*']),
      zip_safe=False,
      install_requires=[
        'matrix-nio==0.17.0',
        'requests==2.25.1',
        'Pillow==8.1.2'
      ]
     )
