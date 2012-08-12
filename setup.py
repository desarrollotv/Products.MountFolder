from setuptools import setup, find_packages

version = '1.2'

setup(name='Products.MountFolder',
      version=version,
      description="An Archetypes Folder acting as a Mount Point for "
                  "separating a Content.fs from the Data.fs.",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        ],
      keywords='MountFolder Plone Zope',
      author='Ingeniweb',
      author_email='support@ingeniweb.com',
      url='http://pypi.python.org/pypi/Products.MountFolder',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
        test=[
        ],
      ),
      install_requires=[
          'setuptools',
        ],
      )
