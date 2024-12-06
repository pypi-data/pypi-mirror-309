import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="basic_fengfengzai",
    version="0.0.2",
    author="dufeng1010",
    author_email="dufeng@example.com",
    description="short package description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://example.com",
    project_urls = {
        "Bug Tracker": "http://example.com",
    },
    package_dir= {"": "src"},
    packages= setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)