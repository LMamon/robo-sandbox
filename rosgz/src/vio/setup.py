from setuptools import find_packages, setup

package_name = 'vio'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Louis M',
    maintainer_email='maintainer@example.com',
    description='bridge between ov_msckf and px4 topics for mono VIO',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'vio_node = vio.vio_node:main',
        ],
    },
)
