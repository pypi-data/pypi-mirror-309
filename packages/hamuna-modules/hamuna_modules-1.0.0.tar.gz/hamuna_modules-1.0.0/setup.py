from setuptools import setup, find_packages

setup(
    name='hamuna-modules',
    version='1.0.0',
    packages=find_packages(),
    license="MIT",
    description='Modules for Hamuna AI',
    long_description='Hamuna AI modules',
    long_description_content_type="text/plain",
    author='O.Push',
    author_email='opush.developer@outlook.com',
    url='https://www.hamuna.club',
    package_dir={'': '.'},
    install_requires=['diskcache', 'httpx', 'aiofile', 'aiohttp', 'aiohttp_retry','aiodecorators', 'wget']
)
