from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
print(long_description) 

setup(
    name = 'Plan_Your_Workout',
    version = '0.0.1',
    packages = find_packages(),
    author = 'Grupo 1',
    author_email = 'irati.artaraz@alumni.mondragon.edu',
    description = 'A Guide to Structuring Your Fitness Agenda',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url='https://github.com/eddamarcos/BDATA4_Progra_Grupo1',  
    package_data={
        "": ["docs/*"],
    },
)