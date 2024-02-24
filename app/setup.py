from setuptools import setup, find_packages

setup(
    name='app',  # Your application's name
    version='0.1.0',  # Your application's version
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[
        # List your project's dependencies here.
        # Examples:
        # 'numpy>=1.18.5',
        # 'pandas>=1.0.5',
    ],
    entry_points={
        'console_scripts': [
            # If your application is a command-line tool, you can specify its entry point here.
            # For example, if you have a script called 'main.py' in your package 'app' with a main method,
            # you could use the following line to make it callable from the command line directly.
            'app=app.main:main',
        ],
    },
    # Additional metadata about your project
    author='Your Name',
    author_email='your.email@example.com',
    description='A brief description of your application',
    keywords='Some relevant keywords',
    url='http://example.com/yourapp',  # Project home page
)
