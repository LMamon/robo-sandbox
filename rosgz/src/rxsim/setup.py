import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'rxsim'

setup(
    name=package_name,
    version='1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        (os.path.join('share', package_name, 'config', 'nvblox'),
            glob('config/nvblox/*.yaml')),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*launch.py')),
        (os.path.join('share', package_name, 'config'), 
            glob('config/*.yaml'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Louis M',
    maintainer_email='maintainer@example.com',
    description='integration package for vSLAM + 3d reconstruction with autonomy pipeline.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
