from setuptools import setup

setup(
    name='danilo-planner',
    version='0.1',
    packages=['danilo_planner'],
    description='Planificador de tareas con IA implementando diferentes modelos',
    author='Danilo Florez',
    author_email='gersondiaz030998@gmail.com',
    url='',
    install_requires=[
        'langchain',
        'chromadb',
        'langchain_community',
        'langchain-chroma',
        'huggingface_hub',
        'langchainhub'
    ],
)