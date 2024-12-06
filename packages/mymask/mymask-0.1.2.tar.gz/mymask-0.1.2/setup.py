from setuptools import setup, find_packages

setup(
    name='mymask',
    version='0.1.2',
    description='An interactive data masking tool for any x-y data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mingyu Li',
    author_email='lmytime@hotmail.com',
    url='https://github.com/lmytime/mymask',
    license='GPL3',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'astropy',
        'PyQt5',
        'matplotlib'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'mymask = mymask.app:main',  # 设置命令行入口
        ],
    },
    python_requires='>=3.6',
)