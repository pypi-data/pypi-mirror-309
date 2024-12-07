from setuptools import setup, find_packages

setup(
    name='PyToolkit-doxy', 
    version='0.2',
    packages=find_packages(),  # Détecte automatiquement tous les packages Python dans le dossier
    description='A toolkit for data analysis and visualization', 
    long_description=open('README.md').read(),
    author='Doxy',  
    author_email='brguillerm@gmail.com',  # Votre email ou celui de votre organisation
    install_requires=[  # Liste des dépendances nécessaires à l'installation
        'numpy',
        'matplotlib',
        'pandas',  # Assurez-vous d'inclure toutes les bibliothèques externes que vous utilisez
        'scikit-learn',
        'seaborn',
    ],
    python_requires='>=3.6',  # Version minimum de Python requise
)