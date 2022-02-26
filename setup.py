import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rclone_backup",
    version="0.1.0",
    author="takuya",
    author_email="takuya+nospam@gmail.com",
    description="backup script for rclone ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/takuya/python_rclone_backup",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.7',
)
