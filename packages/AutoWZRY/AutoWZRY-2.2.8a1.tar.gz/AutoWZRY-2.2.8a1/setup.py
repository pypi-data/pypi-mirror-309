from setuptools import setup

setup(
    name='AutoWZRY',
    version='2.2.8a1',
    author='cndaqiang',
    author_email='who@cndaqiang.ac.cn',
    description='王者荣耀自动化农活脚本.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    py_modules=['wzry', 'wzyd', 'tiyanfu'],
    package_data={
        'assets': ['assets/*'],  # Include all files from assets
    },
    include_package_data=True,  # Ensure package_data is included
    url='https://github.com/cndaqiang/WZRY', 
    install_requires=[
        'airtest-mobileauto>=2.0.12',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
)
