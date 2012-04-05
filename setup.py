from setuptools import setup

setup(name='thepian-pages',
      version=0.32,
      description="The Thepian Web Pages",
      long_description="""\
""",
      keywords='thepian web pages jekyll',
      author='Henrik Vendelbo',
      author_email='hvendelbo.dev@googlemail.com',
      maintainer='Henrik Vendelbo',
      maintainer_email='hvendelbo.dev@googlemail.com',
      url='www.thepian.org',
      license='AGPL',
      packages= ['webpages'],
      entry_points = {
        'console_scripts': [
          'runserver = webpages:runserver',
          'populateserver=webpages:populateserver',
        ]
      },
      include_package_data=True,
      zip_safe=True,
      setup_requires=['tornado',],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ], 
      )