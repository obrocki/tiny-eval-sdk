from setuptools import setup, find_packages

setup(
    name='prompt-eval-sdk',
    version='0.0.3',
    author='Dawid Obrocki',
    author_email='dawid.obrocki@microsoft.com',
    description='A AI prompt evaluation SDK using Azure Open AI Services',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/obrocki/prompt-eval-sdk',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        'prompt_eval_sdk': ['code_evaluator.prompty'],  # Specify the file to include
    },
    install_requires=[
        'azure-identity',
        'azure-ai-evaluation',
        'promptflow',
        'requests',
        'pytest',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)