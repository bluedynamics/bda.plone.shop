import os
from setuptools import setup
from setuptools import find_packages


version = '2.0.dev0'
shortdesc = "Shop Solution for Plone"
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'CHANGES.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()


setup(
    name='bda.plone.shop',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    author='BlueDynamics Alliance',
    author_email='dev@bluedynamics.com',
    license='GNU General Public Licence',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['bda', 'bda.plone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'bda.plone.discount',
        'bda.plone.orders',
        'collective.z3cform.datagridfield',
        'Products.CMFPlone',
        'plone.api>=1.3.0',
        'plone.app.users>=2.0',
        'plone.app.workflow>=2.1.9',
        'setuptools',
        'zope.deferredimport',
        'z3c.form>=3.2.4',  # Issue #55
    ],
    extras_require={
        'test': [
            'plone.app.contenttypes',
            'plone.app.dexterity',
            'plone.app.robotframework [debug]',
            'plone.app.testing [robot]',
            'Products.PrintingMailHost',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
