import setuptools

def readme():
    with open("README.md", "r") as fh:
        return fh.read()

with open('requirements.txt') as fid:
    INSTALL_REQUIRES = []
    for line in fid.readlines():
        if line == '' or line[0] == '#' or line[0].isspace():
            continue
        INSTALL_REQUIRES.append(line.strip())

setuptools.setup(
    name="skynapp-fcmpy",
    version="0.0.1",
    author="Yaroslav Napadailo, Samvel Mkhitaryan, Philippe J. Giabbanelli, Maciej Wozniak, Nanne K. de Vries, Rik Crutzen",
    author_email="napadailo@skynapp.com",
    description="Fuzzy Cognitive Maps for Behavior Change Interventions and Evaluation",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/man1207/FCMpy.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10.0',
    install_requires=INSTALL_REQUIRES
)
