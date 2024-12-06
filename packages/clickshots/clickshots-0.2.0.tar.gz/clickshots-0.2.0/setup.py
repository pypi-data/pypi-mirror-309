from setuptools import setup, find_packages

setup(
    name="clickshots",
    version="0.2.0",
    author="Akmol Masud",
    author_email="akmolmasud5@gmail.com",
    description="A robust automated screenshot capture system",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pynput>=1.7.0",
        "Pillow>=9.0.0",
        "pyscreenshot>=3.1",
        "python-xlib; platform_system=='Linux'",
        "PyQt5; platform_system=='Linux'",
        "pyautogui; platform_system=='Darwin'",
    ],
    extras_require={
        'test': [
            'pytest>=7.0',
            'pytest-cov>=4.0',
            'pytest-mock>=3.10',
            'coverage>=7.0',
            'pytest-xvfb; platform_system=="Linux"',
        ],
    },
    entry_points={
        "console_scripts": [
            "clickshots=clickshots.core:main",
        ],
    },
    python_requires='>=3.8',
)