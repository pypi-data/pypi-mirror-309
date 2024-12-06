from setuptools import setup, find_packages

setup(
    name="box_object_detection",  # Nama paket Anda
    version="0.1.0",  # Versi pertama paket
    description="A YOLOv8-based object detection tool using FastAPI.",  # Deskripsi singkat
    long_description=open("README.md").read(),  # Baca README sebagai deskripsi panjang
    long_description_content_type="text/markdown",  # Format Markdown untuk README
    author="Your Name",  # Nama Anda
    author_email="kelessamsung22@gmail.com",  # Email Anda
    url="https://github.com/Raizo22",  # URL repositori GitHub
    license="Raizo22",  # Lisensi (MIT adalah pilihan umum)
    packages=find_packages(),  # Temukan semua paket dalam direktori
    include_package_data=True,  # Sertakan file seperti template dan statis
    install_requires=[
        "fastapi",
        "uvicorn",
        "pillow",
        "opencv-python",
        "numpy",
        "ultralytics"
    ],  # Daftar dependensi
    entry_points={
        "console_scripts": [
            "box-object-detection=box_object_detection.app:main",  # Command untuk menjalankan aplikasi
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",  # Versi Python minimum
)
