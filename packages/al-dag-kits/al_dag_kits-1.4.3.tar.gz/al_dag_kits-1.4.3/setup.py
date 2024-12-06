from setuptools import setup, find_packages

setup(
    name='al_dag_kits',
    version='1.4.3',
    description='Custom utilities and triggers for Airflow DAGs',
    author='Zeming lim',
    author_email='zeming.lim@applovin.com',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        'apache-airflow-providers-google>=10.21.0',
        'apache-airflow-providers-cncf-kubernetes>=8.3.3',
    ],
)
