from setuptools import setup, find_packages
from pathlib import Path

long_description = Path("../readme.md").read_text(encoding='utf-8')

extras = {
    "filing_viewer": ["lxml"],
    "mulebot": ['openai'],
    "mulebot_server": ['flask'],
    "dataset_builder": ['pandas', 'google-generativeai', 'psutil']  # Add new extra
}

all_dependencies = set(dep for extra_deps in extras.values() for dep in extra_deps)
extras["all"] = list(all_dependencies)

setup(
    name="datamule",
    author="John Friedman",
    version="0.379",
    description="Making it easier to use SEC filings.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(include=['datamule*']) + ['datamule.dataset_builder'],  # Just add the specific package
    url="https://github.com/john-friedman/datamule-python",
    install_requires=[
        'aiohttp',
        'aiolimiter',
        'tqdm',
        'requests',
        'nest_asyncio',
        'aiofiles',
        'polars',
        'setuptools',
        'selectolax'
    ],
    extras_require=extras,
    package_data={
        "datamule": ["data/*.csv"],
        "datamule.mulebot.mulebot_server": [
            "templates/*.html",
            "static/css/*.css",
            "static/scripts/*.js"
        ],
    },
    include_package_data=True,
)