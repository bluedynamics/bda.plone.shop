from setuptools import find_packages
from setuptools import setup
import os


def read_file(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return f.read()


version = '2.0b2.dev0'
shortdesc = "Shop Solution for Plone"
longdesc = '\n\n'.join([read_file(name) for name in [
    'README.rst',
    'CHANGES.rst',
    'LICENSE.rst'
]])


setup(
    name='bda.plone.shop',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Addon",
        "Framework :: Zope",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    author='BlueDynamics Alliance',
    author_email='dev@bluedynamics.com',
    license='GNU General Public Licence',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.7',
    namespace_packages=['bda', 'bda.plone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'bda.plone.discount',
        'bda.plone.orders',
        'collective.z3cform.datagridfield',
        'Products.CMFPlone>=6.0a1',
        'plone.api',
        'setuptools',
        'zope.deferredimport',
        'zope.schema>=3.4',  # Decimal field
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
