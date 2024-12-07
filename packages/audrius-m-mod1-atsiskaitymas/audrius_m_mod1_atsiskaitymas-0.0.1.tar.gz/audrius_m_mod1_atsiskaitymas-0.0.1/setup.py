import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="audrius_m_mod1_atsiskaitymas",
    version="0.0.1",
    author="Audrius M",
    author_email="balvakokay@gmail.com",
    description="Website crawler",
    long_description = long_description,
    ##todo change to pypi URL after uploading
    url="https://github.com/audriu/audrius-m-mod1-atsiskaitymas",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "audrius_m_mod1_atsiskaitymas"},
    packages=setuptools.find_packages(where="audrius_m_mod1_atsiskaitymas"),
    python_requires=">=3.6"
)
