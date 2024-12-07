from setuptools import find_packages, setup

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]

setup(
    name='flickpaysdk',
    packages=find_packages(),
    version='1.0.0',
    description='This SDK contains FlickPay inflow and outflow solutions',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    author='Qraba Inc',
    url='https://merchant.getflick.co/',
    author_email='kingsley@getflick.app',
    license='MIT',
    classifiers=classifiers,
    keywords=[
        "flickpaysdk",
        "card",
        "bank",
        "transfer",
        "payout",
        "inflow",
        "outflow",
    ],
    install_requires=[
        'requests>=2.25.1',
        'dataclasses',  # Only for Python < 3.7; remove if using >= 3.7
    ],
)
