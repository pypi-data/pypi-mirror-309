from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='EVTUHLIB',
  version='3.0.0',
  author='Evtushenko Vladislav',
  author_email='evtuh545@gmail.com',
  description='...',
  long_description_content_type='text/markdown',
  url='https://sweet-store.ru',
  install_requires=['art'],
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='evtuh evtuh ',
  python_requires='>=3.6'
)