from setuptools import find_packages, setup

setup(
    name='temp_monitor_web',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'bokeh',
        'flask-wtf',
        ],
)
