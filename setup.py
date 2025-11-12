from setuptools import setup, find_packages

setup(
    name='traffic_signal_control',
    version='0.2.0',
    description='Deep RL-based 4-way Traffic Signal Control System with GPU Support',
    author='Traffic Control Research',
    author_email='dev@traffic-control.local',
    python_requires='>=3.8',
    
    packages=find_packages(exclude=['tests', 'scripts']),
    
    install_requires=[
        'numpy>=1.24.0',
        'pandas>=2.0.0',
        'gymnasium>=0.28.0',
        'cloudpickle>=2.2.1',
        'torch>=2.0.1,<2.8.0',
        'PyQt5>=5.15.0',
        'pyqtgraph>=0.13.0',
        'matplotlib>=3.5.0',
        'seaborn>=0.11.0',
        'PyYAML>=6.0',
        'python-dateutil>=2.8.2',
        'tqdm>=4.64.0',
    ],
    
    extras_require={
        'dev': [
            'pytest>=7.2.0',
            'black>=23.1.0',
            'flake8>=4.0.1',
            'mypy>=1.1.0',
        ],
    },
    
    entry_points={
        'console_scripts': [
            'traffic-demo=scripts.run_demo:main',
            'traffic-train=scripts.train:main',
            'traffic-eval=scripts.evaluate:main',
        ],
    },
    
    zip_safe=False,
    include_package_data=True,
)
