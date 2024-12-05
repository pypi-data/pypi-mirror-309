from setuptools import setup, find_packages

setup(
    name='bitpix',
    version='1.0',
    author='Felix Rishar',
    author_email='felix_rishar@tutamail.com',
    description='Pixel painting library',  # Здесь закрыты кавычки
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),  # Находит все пакеты в проекте
    install_requires=[
        'opencv-python',  # Зависимость для cv2
        'Pillow',         # Зависимость для PIL
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  # Минимальная версия Python
)
