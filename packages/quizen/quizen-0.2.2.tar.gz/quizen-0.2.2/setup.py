from setuptools import setup, find_packages

setup(
    name='quizen',                          # Nom du paquet
    version='0.2.2',                       # Version du paquet
    packages=find_packages(),              # Inclut tous les sous-dossiers contenant __init__.py
    install_requires=[                     # Liste des dépendances du paquet
        'rich',                             # Affichage dans la console (exemple)
    ],
    entry_points={                         # Point d'entrée si nécessaire (pour les commandes CLI)
        'console_scripts': [
            'quizen = quizen.quiz:main',         # Point d'entrée principal pour le jeu de quiz
        ],
    },
    author='kouya tosten',
    author_email='kouyatosten@gmail.com', # Votre email
    description='Un module pour créer facilement un jeu de quiz',  # Brève description
    long_description=open('README.md', encoding='utf-8').read(),  # Lire le README.md pour la description longue
    long_description_content_type='text/markdown',  # Format du fichier README
    url='https://github.com/Tostenn/Quizen.git',  # Lien vers le dépôt GitHub
    classifiers=[                          # Classifiers PyPI pour mieux catégoriser le paquet
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',                # Version minimale de Python requise
)
