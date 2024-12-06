from setuptools import setup

setup(
    name='danilo-planner',
    version='0.4',
    packages=['danilo_planner'],
    description='Planificador de proyectos con IA mediante GPT-4',
    author='Danilo Florez',
    author_email='gersondiaz030998@gmail.com',
    url='',
    install_requires=[
        'langchain',
        'chromadb',
        'langchain_community',
        'langchain-chroma',
        'huggingface_hub',
        'langchainhub',
        'langchain_core'
    ],
)