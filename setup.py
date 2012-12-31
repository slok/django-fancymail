from setuptools import setup, find_packages

setup(
    name='django-fancymail',
    version='0.1',
    description='Fancy mail is a Django app to help managing your templated emails. The aim of this app is to be simple and to reuse all the stuff that Django gives us, like the email classes ',
    long_description=open('README.rst').read(),
    # Get more strings from http://www.python.org/pypi?:action=list_classifiers
    author='Xabier Larrakoetxea',
    author_email='slok69@gmail.com',
    url='https://github.com/slok/django-fancymail',
    license='BSD',
    packages=find_packages(exclude=('example', 'email_templates',
                                'fancymail.tests.py')),
    tests_require=[
        'django>=1.4',
    ],
    test_suite='runtests.runtests',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)