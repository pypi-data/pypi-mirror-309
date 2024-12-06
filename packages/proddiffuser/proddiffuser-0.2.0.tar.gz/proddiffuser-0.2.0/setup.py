from setuptools import find_packages, setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='proddiffuser',
    version='0.2.0',
    description='A Python application for generating backgrounds based on prompts and combining them with product images.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='hrt-ykym',
    url='https://github.com/hrt-ykym/prodDiffuser',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'accelerate==1.1.1',
        'diffusers==0.31.0',
        'huggingface-hub==0.26.2',
        'numpy==2.1.3',
        'pillow==11.0.0',
        'safetensors==0.4.5',
        'torch>=2.1.2',
        'torchvision>=0.16.2',
        'torchaudio>=2.1.2',
        'transformers==4.46.2',
        'transparent-background==1.3.3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
