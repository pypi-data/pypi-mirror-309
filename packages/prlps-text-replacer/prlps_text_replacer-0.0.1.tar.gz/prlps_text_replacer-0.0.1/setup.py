from setuptools import setup, find_packages

setup(
    name='prlps_text_replacer',
    version='0.0.1',
    author='prolapser',
    packages=find_packages(),
    url='https://github.com/prolapser/prlps_text_replacer',
    license='LICENSE.txt',
    description='замена слов и фраз по словарям замен с сохранением исходного регистра',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
