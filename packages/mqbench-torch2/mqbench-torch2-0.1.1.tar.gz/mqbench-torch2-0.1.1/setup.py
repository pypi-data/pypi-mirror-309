import setuptools
from mqbench import __version__

setuptools.setup(
    name="mqbench-torch2",
    version=__version__,
    author="weiyuzhou, The Great Cold",
    author_email="short_after@163.com",
    description=("model quantization tools."),
    python_requires='>=3.10',
    url = 'https://github.com/StephenChou0119/MQBench',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        "requirements": ["requirements.txt"],
    },
    classifiers=(
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux"),
    install_requires=["prettytable"],
    license='Apache-2.0',
    
)
