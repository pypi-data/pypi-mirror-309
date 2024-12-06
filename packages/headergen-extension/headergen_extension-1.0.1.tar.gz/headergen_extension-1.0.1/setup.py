from setuptools import setup, find_packages

setup(
    name='headergen_extension',
    version='1.0.1',  # Update the version number
    description='A Jupyter extension to convert your undocumented notebooks to documented notebooks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rishma Merkaje Nanaiah',
    author_email='rishmamn@mail.upb.de',
    url='https://github.com/rishma123/headergen1',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('share/jupyter/nbextensions/headergen_extension', [
            'static/main.js'
        ]),
        ('etc/jupyter/nbconfig/notebook.d', [
            'headergen_extension.json'
        ])
    ],
    install_requires=[
        'notebook>=6.0.0',
        'jupyterlab>=3.0.0'
    ],
    classifiers=[
        'Framework :: Jupyter',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'headergen=headergen_extension:main',
        ]
    }
)