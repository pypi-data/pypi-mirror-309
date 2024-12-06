import sys
import os
from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.bdist_wheel import bdist_wheel as _bdist_wheel
from distutils.errors import CompileError
import subprocess

# Custom build_ext command to check for C compiler
class BuildExt(build_ext):
    def run(self):
        try:
            # Attempt to run the build process
            super().run()
        except CompileError as e:
            # If there's a compilation error, print a helpful message
            print("*****************************************************************")
            print("ERROR: A C compiler is required to build this package from source.")
            print("Please install a C compiler or try installing a pre-built wheel.")
            print("*****************************************************************")
            sys.exit(1)

# Custom bdist_wheel command to ensure a platform-specific wheel is built
class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False  # Ensures a platform-specific wheel is built

# Custom build command to integrate Nuitka
class BuildWithNuitka(_build_py):
    def run(self):
        target_system = os.getenv("TARGET_SYSTEM", "current")
        nuitka_cmd = [
            sys.executable,
            "-m", "nuitka",
            "--standalone",
            "--onefile",
            "--follow-imports",
            "src/fiscus/main.py",  # Adjust to your main entry script
            "--output-dir=dist",
        ]
        if target_system != "current":
            if target_system == "windows":
                nuitka_cmd.extend(["--windows-target", "10"])
            elif target_system == "linux":
                nuitka_cmd.append("--linux-onefile-icon=icon.png")  # Example for Linux

        try:
            subprocess.check_call(nuitka_cmd)
        except subprocess.CalledProcessError as e:
            print("*****************************************************************")
            print("ERROR: Nuitka build failed.")
            print("Ensure Nuitka is properly installed and configured.")
            print("*****************************************************************")
            raise e
        super().run()

# Read the long description from README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Ensure __init__.py exists in the target directory
init_file = os.path.join("src", "fiscus", "__init__.py")
if not os.path.exists(init_file):
    open(init_file, "w").close()  # Create an empty __init__.py

# List of core dependencies
install_requires = [
    'aiohappyeyeballs>=2.4.3',
    'aiohttp>=3.10.10',
    'aiosignal>=1.3.1',
    'annotated-types>=0.7.0',
    'anyio>=4.6.2.post1',
    'attrs>=24.2.0',
    'certifi>=2024.8.30',
    'charset-normalizer>=3.4.0',
    'distro>=1.9.0',
    'filelock>=3.16.1',
    'frozenlist>=1.4.1',
    'fsspec>=2024.9.0',
    'gevent>=24.2.1',
    'greenlet>=3.1.1',
    'h11>=0.14.0',
    'httpcore>=1.0.6',
    'httpx>=0.27.2',
    'idna>=3.10',
    'jiter>=0.6.1',
    'multidict>=6.1.0',
    'packaging>=24.1',
    'propcache>=0.2.0',
    'pydantic>=2.9.2',
    'pydantic_core>=2.23.4',
    'PyYAML>=6.0.2',
    'requests>=2.32.3',
    'setuptools>=75.1.0',
    'sniffio>=1.3.1',
    'tqdm>=4.66.5',
    'typing_extensions>=4.12.2',
    'urllib3>=2.2.3',
    'websocket-client>=1.8.0',
    'websockets>=13.1',
    'yarl>=1.15.5',
    'zope.event>=5.0',
    'zope.interface>=7.0.3'
]

# Optional dependencies
extras_require = {
    'openai': ['openai>=1.53.0'],
    'anthropic': ['anthropic>=0.37.1', 'tokenizers>=0.20.1'],
    'ai': ['huggingface-hub>=0.25.2', 'tokenizers>=0.20.1', 'anthropic>=0.37.1'],
    'full': ['openai>=1.53.0', 'anthropic>=0.37.1', 'huggingface-hub>=0.25.2', 'tokenizers>=0.20.1']
}

# Define cmdclass with the custom commands
cmdclass = {
    'build_ext': BuildExt,
    'bdist_wheel': bdist_wheel,
    'build_with_nuitka': BuildWithNuitka,
}

# Main setup configuration
setup(
    name="fiscus",
    version="0.1.0a32",
    description="Fiscus is a powerful platform designed to be the API Gateway for the AI World.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Fiscus Flows, Inc.",
    author_email="support@fiscusflows.com",
    url="https://github.com/fiscusflows/fiscus-sdk",
    license="Proprietary",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"fiscus": ["**/*.so", "**/*.pyd", "**/*.py"]},
    zip_safe=False,
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.9",
    keywords="API Gateway AI Machine Learning",
    cmdclass=cmdclass,
)
