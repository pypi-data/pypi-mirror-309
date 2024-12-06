from setuptools import setup

setup(
    name="erddapcfg",
    version="0.0.2",
    description="Python program to work with ERDDAP configurations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PlehanSebastian/erddapcfg",
    author="Sebastian Plehan",
    author_email="plehan.sebastian@gmail.com",
    packages=[
        "erddapcfg",
    ],
    package_dir={"erddapcfg": "erddapcfg"},
    entry_points={
        "console_scripts": ["erddapcfg=erddapcfg.cli:cli_entry_point"],
    },
    include_package_data=True,
    install_requires=[
        "pandas",
        "jinja2",
    ],
    data_files=[
        (
            "",
            [
                "erddapcfg/templates/datasets.xml.j2",
                "erddapcfg/templates/db_insert.j2",
                "erddapcfg/templates/macro.j2",
            ],
        )
    ],
)
