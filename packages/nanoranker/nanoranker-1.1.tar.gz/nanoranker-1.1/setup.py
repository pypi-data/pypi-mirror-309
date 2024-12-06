from setuptools import setup, find_packages

setup(
    name='nanoranker',
    version='1.1',
    author='Carlo Moro',
    author_email='cnmoro@gmail.com',
    description="Nano Sentence Ranker",
    packages=find_packages(),
    package_data={
        "nanoranker": ["resources/*"]
    },
    include_package_data=True,
    install_requires=[
        "torch",
        "twine",
        "scikit-learn",
        "tqdm",
        "numpy",
        "onnxruntime",
        "onnxruntime_extensions",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)