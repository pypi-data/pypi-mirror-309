from setuptools import setup, find_packages

setup(
    name="runtexts",
    version="1.7",
    packages=find_packages(),
    install_requires=[
        "pyautogui",
        "colorama",
        "requests",
        "keyboard",  
    ],
    entry_points={
        "console_scripts": [
            "runtexts=runtexts.cli:main", 
            "runtexts-gui=runtexts.gui:main",  
        ],
    },
    author="Maruf Ovi",
    author_email="fornet.ovi@gmail.com",
    description="A CLI and GUI tool to send automated messages.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iamovi/project_runtexts",
    license="MIT",
    keywords="automation, messaging, CLI, pyautogui, tkinter, GUI",
    python_requires=">=3.6",
)
