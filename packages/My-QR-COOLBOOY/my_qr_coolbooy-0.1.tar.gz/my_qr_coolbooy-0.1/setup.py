from setuptools import setup, find_packages

setup(
    name='My-QR-COOLBOOY',
    version='0.1',
    packages=find_packages(),
    install_requires=['qrcode'], 
    author='COOLBOOY550',
    author_email='github.mytool.coolbooy@gmail.com',
    description='Create QR codes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[ 
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3 :: Only',
        'Natural Language :: English',
    ],
)
