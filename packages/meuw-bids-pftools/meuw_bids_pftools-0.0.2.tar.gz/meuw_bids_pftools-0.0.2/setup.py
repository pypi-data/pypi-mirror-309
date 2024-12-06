from setuptools import find_packages, setup

PACKAGE_NAME = "meuw_bids_pftools"

setup(
    name=PACKAGE_NAME,
    version="0.0.2",
    description="This is my tools package",
    packages=find_packages(),
    entry_points={
        "package_tools": [
            "custom_search = meuw_bids_pftools.tools.utils:list_package_tools"
        ],
    },
    include_package_data=True,  # This line tells setuptools to include files from MANIFEST.in
)
