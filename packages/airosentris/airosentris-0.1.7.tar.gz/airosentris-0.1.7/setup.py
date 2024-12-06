from setuptools import setup, find_packages

setup(
    name='airosentris',
    version='0.1.7',
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
        'selenium',
        'webdriver-manager',
        'psutil==6.0.0',
        'py-cpuinfo==9.0.0',
        'pika==1.3.2',
        'tweepy==4.14.0',
        'python-dotenv==1.0.1',
        'selenium==4.23.1',
        'setuptools==60.2.0',
        'GPUtil==1.4.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)