from distutils.core import setup
setup(
  name = 'colby',
  packages = ['colby'],
  version = '0.2.0',
  license='MIT',
  description = 'Visualization package',
  author = 'John Ferraro',
  author_email = 'jkf44@georgetown.edu',
  url = 'https://github.com/m1jkf00/colby',
  download_url = 'https://github.com/m1jkf00/colby/releases/tag/v0_2_0.tar.gz',
  keywords = ['plot', 'graph', 'chart', 'table'],
  install_requires=[
          'matplotlib',
          'pandas',
          'PyPDF2'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable', 
    'Intended Audience :: Developers', 
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
  ],
)