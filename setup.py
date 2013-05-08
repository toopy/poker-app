from setuptools import setup, find_packages

setup(
    name="poker-app",
    version="0.1",
    description="",
    long_description="""\
""",
    classifiers=[],
    keywords="",
    author="Florent",
    author_email="florent@toopy.org",
    url="http://www.toopy.org",
    license="MIT",
    packages=find_packages(exclude=[]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "fanstatic",
        "pillow",
        "pycv-toolbox",
        "pyscreenshot",
        "sqlalchemy",
        "west-socket",
    ],
    namespace_packages=[
        "poker",
        "poker.twisted",
        "poker.static",
    ],
    entry_points={
        "fanstatic.libraries": [
            "jquery = poker.static.jquery:library",
            "bootstrap = poker.static.bootstrap:library",
            "poker = poker.static.poker:library",
        ],
    }
)
