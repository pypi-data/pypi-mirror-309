from setuptools import setup, find_packages
from setuptools import find_packages, setup, Extension
from Cython.Build import cythonize
import os
import shutil
import glob

# # Helper function to find all .py files, excluding __init__.py
# def find_pyx_files(directory):
#     pyx_files = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith(".py") and file != "__init__.py":
#                 pyx_files.append(os.path.join(root, file))
#     return pyx_files

# # Specify the directories you want to convert to .so
# directories = ['rejo_ai']

# # Collect all .py files
# pyx_files = []
# for directory in directories:
#     pyx_files.extend(find_pyx_files(directory))

# # Define the extensions
# # Define the extensions
# extensions = [
#     Extension(
#         pyx.replace('.py', '').replace(os.sep, '.'),  # Cross-platform compatible
#         [pyx]
#     ) for pyx in pyx_files
# ]


setup(
    name="rejoai",                       # Package name
    version="0.1.2",                         # Initial version
    description="A brief description",       # Short description
    long_description=open("README.md").read(),  # Detailed description from README
    long_description_content_type="text/markdown",
    author="RejoAI Team",                      # Author name
    author_email="your.email@example.com",   # Author email
    url="https://github.com/rejoai",  # Project URL
    packages=find_packages(),                # Finds all modules in the package
    install_requires=[                       # Dependencies, if any
        "requests>=2.25.1",
         'cython',
    ],
    # ext_modules=cythonize(extensions),
    classifiers=[                            # Additional metadata
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",                 # Minimum Python version
)


# # Copy __init__.py files to obfuscated directory
# for directory in directories:
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file == '__init__.py':
#                 dest_dir = root.replace('rejo_ai', 'obfuscated/rejo_ai')
#                 os.makedirs(dest_dir, exist_ok=True)
#                 shutil.copy(os.path.join(root, file), os.path.join(dest_dir, file))

# # Copy .so files to obfuscated directory
# for so_file in glob.glob('rejo_ai/**/*.so', recursive=True):
#     dest_file = so_file.replace('rejo_ai', 'obfuscated/rejo_ai')
#     dest_dir = os.path.dirname(dest_file)
#     os.makedirs(dest_dir, exist_ok=True)
#     shutil.move(so_file, dest_file)

# # Cleanup .c files from core directory
# for directory in directories:
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith(".c"):
#                 os.remove(os.path.join(root, file))
# # Remove the build folder
# shutil.rmtree('build', ignore_errors=True)
