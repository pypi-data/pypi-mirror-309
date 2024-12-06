from setuptools import setup, find_packages

setup(
    name="himpunan-team3",  # Nama package Anda (harus unik di PyPI)
    version="0.1.0",  # Versi package
    author="Franklin Jaya, Muh. Ryan Ardiansyah, Tiffany Tjandinegara",  # Nama pembuat
    description="Package Python untuk operasi himpunan",  # Deskripsi singkat package
    packages=find_packages(),  # Mencari semua subfolder yang mengandung file Python
    classifiers=[
        "Programming Language :: Python :: 3",  # Spesifikasi bahasa  
    ],
)
