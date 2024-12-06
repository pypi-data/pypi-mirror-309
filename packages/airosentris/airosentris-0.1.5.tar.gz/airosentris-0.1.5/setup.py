from setuptools import setup, find_packages

setup(
    name='airosentris',
    version='0.1.5',
    description='A sentiment analysis platform with AI runner and trainer components',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/sindika/project/airosentris/airosentris-python-lib',
    author='Willy Achmat Fauzi',
    author_email='willy.achmat@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests==2.32.3',
        'python-dotenv',
        'apify-client',
        'tweepy',
        'selenium',
        'webdriver-manager'
        'gputil==1.4.0'
        'psutil==6.0.0'
        'py-cpuinfo==9.0.0'
        'pika==1.3.2'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)