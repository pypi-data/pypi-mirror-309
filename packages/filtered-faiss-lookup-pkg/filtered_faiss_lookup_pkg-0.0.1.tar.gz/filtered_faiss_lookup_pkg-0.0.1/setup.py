from setuptools import find_packages, setup

PACKAGE_NAME = "filtered-faiss-lookup-pkg"

setup(
    name=PACKAGE_NAME,
    version="0.0.1",
    description="Tool package to download a FAISS index from an Azure blobstore, do a similarity search and retrieve answers which can be filtered on metadata.",
    packages=find_packages(),
    entry_points={
        "package_tools": ["my_tools = filtered_faiss_lookup_pkg.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
    extras_require={
        "azure": [
            "azure-ai-ml>=1.11.0,<2.0.0"
        ]
    },
)
