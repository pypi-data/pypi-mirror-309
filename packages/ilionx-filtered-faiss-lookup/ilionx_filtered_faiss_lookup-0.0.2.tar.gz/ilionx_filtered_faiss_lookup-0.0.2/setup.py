from setuptools import find_packages, setup

PACKAGE_NAME = "ilionx_filtered_faiss_lookup"

setup(
    name=PACKAGE_NAME,
    author="B.J. Koop",
    version="0.0.2",
    description="This tool package can be used in AzureML Promptflow to search for similar documents in a FAISS index and filter the results based on metadata.",
    packages=find_packages(),
    entry_points={
        "package_tools": ["filtered_faiss_lookup = ilionx_filtered_faiss_lookup.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)
