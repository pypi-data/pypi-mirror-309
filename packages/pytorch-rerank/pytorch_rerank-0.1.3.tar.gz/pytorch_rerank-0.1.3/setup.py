from setuptools import setup, find_packages

setup(
    name='pytorch_rerank',
    version='0.1.3',
    description='A simple distributed script to modify container RANK envs for pytorch training jobs',
    author='wenhuhu',
    author_email='huwenhu.hwh@alibaba-inc.com',
    url='http://gitlab.alibaba-inc.com/tre-ai-infra/pytorch_rerank.git',
    packages = find_packages(),
    include_package_data=True,
    scripts=['torchrerank', 'rerank.py'],
    install_requires=[
        'torch',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)