from setuptools import setup, find_packages

setup(
    name="pi_gpio_device",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "RPi.GPIO",
    ],
    include_package_data=True,
    description="GPIO control",
    author="Komal Swami",
    author_email="komalsswami@example.com",
    url="https://github.com/neudeeptech/Pi-GpioControl.git",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',  # Specify markdown format
    license='Custom License',  # Update this if using a different license
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # Minimum Python version
)