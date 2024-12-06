import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain import PromptTemplate, LLMChain
from langchain import hub
import re
from langchain.tools import Tool, tool
from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.agents import load_tools 
from langchain.agents import initialize_agent 
from langchain.agents import AgentType
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

api_hugginface=""
api_gpt=""

@tool
def leer_planificacion(texto_indicacion_leer_planificador):
    """
        parametros: texto con la indicación del usuario para leer la planificación
        procesamiento: se lee la planificación del planificador dado un texto con la indicación
        retorno: El formato adecuado de documentos para crear el repositorio de planificacion
    """
    loader = DirectoryLoader("danilo_planner", glob="**\\PlanificacionL.txt", loader_cls=TextLoader)
    documents = loader.load()
    return documents

@tool
def crear_planificador(especificaciones):
    """
        parametros: texto con las especificaciónes del proyecto a crear
        procesamiento: se crea un planificador dada la indicación de crear el planificador y las especificaciones del proyecto
        retorno: mensaje de confirmación de la creación del planificador y el contenido retornado
    """
    persist_directory_plan = os.path.normpath("danilo_planner\\PlanificacionL.txt")
    agent = PlanificadorAgent()
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key= api_gpt)
    
    if os.path.exists(persist_directory_plan) and os.path.getsize(persist_directory_plan) > 0:
        with open(persist_directory_plan, 'r', encoding='utf-8') as archivo:
            contenido_existente = archivo.read()
        return f"El planificador ya existe y contiene datos:\n{contenido_existente}"
    else:
        try:
            multi_input_template = """
            Eres un experto en lenguaje {programming_language}.
            {query}
            """
            multi_input_prompt = PromptTemplate(
                input_variables=["programming_language", "query"], 
                template=multi_input_template
            )
            llm_chain = LLMChain(prompt=multi_input_prompt, llm=llm)
            
            programming_language = "PDDL"
            query = especificaciones
            
            total = llm_chain.run({"programming_language": programming_language, "query": query})
            
            patron = r"```(.*?)```"
            resultados = re.findall(patron, total, re.DOTALL)
            contenido_dentro_triples_comillas = '\n'.join(resultados) if resultados else total.strip()
            contenido_sin_pddl = re.sub(r'\bpddl\b', '', contenido_dentro_triples_comillas, flags=re.IGNORECASE)
            
            directorio = os.path.dirname(persist_directory_plan)
            if not os.path.exists(directorio):
                os.makedirs(directorio)
                
            with open(persist_directory_plan, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_sin_pddl)
                
            return f"El planificador fue creado exitosamente:\n{contenido_sin_pddl}"
        
        except Exception as e:
            return f"Error al crear el planificador: {e}"
    
@tool        
def crear_repositorio(input_str):
    """
        parametros: texto con las indicación de crear el repositorio 
        procesamiento: se crea el repositorio de planificación si no existe
        retorno: mensaje de confirmación de la creación del repositorio
    """
    persist_directory = "danilo_planner\\ChromaDB"
    agent = PlanificadorAgent()
    Chroma_DB = Chroma(persist_directory=persist_directory, embedding_function=agent.embeddings).as_retriever()
    query = "planificación"
    docs = Chroma_DB.get_relevant_documents(query)
    
    if docs:
        return "El repositorio existe"
        
    documents = leer_planificacion("leer planificación")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    content = "\n\n".join(str(page.page_content) for page in docs)
    texts = text_splitter.split_text(content)
    
    Chroma_DB = Chroma.from_texts(texts, agent.embeddings, persist_directory=persist_directory)
    Chroma_DB.persist()
    return "El repositorio ha sido creado con la planificación existente."

@tool
def consultar_repositorio(input_str):
    """
        parametros: texto con la indicación de consultar el repositorio
        procesamiento: se consulta el repositorio de planificación
        retorno: mensaje de la consulta realizada
    """
    persist_directory = os.path.normpath("danilo_planner\\ChromaDB")
    agent = PlanificadorAgent()
    Chroma_DB = Chroma(
        persist_directory=persist_directory, 
        embedding_function=agent.embeddings
    ).as_retriever(search_kwargs=dict(k=1))
    
    docs = Chroma_DB.get_relevant_documents(input_str)
    context = "\n\n".join(str(page.page_content) for page in docs)
    return f"La planificación del repositorio es lo siguiente:\n{context}\n\n La consulta es la siguiente:\n{input_str}\n\n La respuesta es:\n"

@tool
def extraer_solicitudes_usuario(input_str):
    """
        parametros: texto con la indicación de extraer las solicitudes del usuario
        procesamiento: se extraen las solicitudes específicas del siguiente texto de manera concreta y no extensa
        retorno: mensaje de confirmación de la extracción de las solicitudes
    """
    return f"Analiza y extrae las solicitudes específicas del siguiente texto de manera concreta y no extensa:\n\n{input_str}\n\nSolicitudes: "

@tool
def comparar_solicitudes(input_str):
    """
        parametros: texto con la indicación de comparar las solicitudes
        procesamiento: se comparan las solicitudes de mejora con la planificación actual
        retorno: mensaje de confirmación de la comparación de las solicitudes       
    """
    persist_directory = os.path.normpath("danilo_planner\\ChromaDB")
    agent = PlanificadorAgent()
    Chroma_DB = Chroma(
        persist_directory=persist_directory, 
        embedding_function=agent.embeddings
    ).as_retriever(search_kwargs=dict(k=1))
    
    docs = Chroma_DB.get_relevant_documents("Devuelve todo el código PDDL del problema de innovación regional en Norte de Santander")
    planificacion_actual = "\n\n".join(str(page.page_content) for page in docs)
    return f"Con la planificación: {planificacion_actual} y las nuevas solicitudes:\n {input_str} devuelve si hay diferencias a implementar: "

@tool
def actualizar_repositorio(input_str):
    """
        parametros: texto con la indicación de actualizar el repositorio
        procesamiento: se actualiza el repositorio de planificación
        salida: mensaje de confirmación de la actualización del repositorio
    """
    persist_directory = os.path.normpath("danilo_planner\\ChromaDB")
    agent = PlanificadorAgent()
    Chroma_DB = Chroma(
        persist_directory=persist_directory, 
        embedding_function=agent.embeddings
    ).as_retriever(search_kwargs=dict(k=1))
    
    docs = Chroma_DB.get_relevant_documents("planificación")
    planificacion_actual = "\n\n".join(str(page.page_content) for page in docs)
    
    prompt_template = f"""
    Al siguiente documento de planificación en PDDL:

        {planificacion_actual}

    edita los siguientes cambios en la parte correspondiente:

        {input_str}

    y lo demás déjalo igual en código PDDL y de forma completa desde su inicio hasta el final.
    """
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key= api_gpt)

    result =llm(prompt_template)
    pattern = re.compile(r'\(define\s+(.*?)\n\)', re.DOTALL)
    match = pattern.search(result)
    codigo_pddl = match.group(0).strip() if match else result
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_text(codigo_pddl)
    
    Chroma_DB = Chroma(persist_directory=persist_directory, embedding_function=agent.embeddings)
    ids_to_delete = Chroma_DB.get()["ids"]
    for id in ids_to_delete:
        Chroma_DB.delete([id])
        
    Chroma_DB = Chroma.from_texts(texts, agent.embeddings, persist_directory=persist_directory)
    Chroma_DB.persist()
    
    return "La planificación ha sido actualizada."

@tool
def implementar_solicitudes_de_mejora(input_str):
        """
        parametros: texto con la indicación de implementar las solicitudes de mejora
        procesamiento: se implementan las solicitudes de mejora en la planificación
        retorno: mensaje de confirmación de la implementación de las solicitudes
        """
        persist_directory = os.path.normpath("danilo_planner\\ChromaDB")
        agent = PlanificadorAgent()
        Chroma_DB = Chroma(
            persist_directory=persist_directory, 
            embedding_function=agent.embeddings
        ).as_retriever(search_kwargs=dict(k=1))
        
        docs = Chroma_DB.get_relevant_documents("planificación")
        planificacion_actual = "\n\n".join(str(page.page_content) for page in docs)
        
        prompt = f"""
        La planificación actual es la siguiente:
        {planificacion_actual}
        Sugiere mejoras a dicha planificación de tal manera que no se altere su estructura y la planificación actual:
        """
        llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key= api_gpt)

        return llm(prompt)


class PlanificadorAgent:
    def __init__(self):
        self.embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=api_hugginface, model_name="sentence-transformers/all-MiniLM-l6-v2"
        )

        self.tools =[
            Tool(
                name='crear_planificador',
                func=crear_planificador,
                description="se crea un planificador dada la indicación de crear el planificador y las especificaciones del proyecto"
            ),
            Tool(
                name='leer_planificacion',
                func=leer_planificacion,
                description="se lee la planificación del planificador dado un texto con la indicación"
            ),
            Tool(
                name='crear_repositorio',
                func=crear_repositorio,
                description="se crea el repositorio de planificación si no existe"
            ),
            Tool(
                name='consultar_repositorio',
                func=consultar_repositorio,
                description="se consulta el repositorio de planificación"
            ),
            Tool(
                name='extraer_solicitudes_usuario',
                func=extraer_solicitudes_usuario,
                description="Analiza y extrae las solicitudes específicas del siguiente texto de manera concreta y no extensa"
            ),
            Tool(
                name='comparar_solicitudes',
                func=comparar_solicitudes,
                description="se comparan las solicitudes de mejora con la planificación actual"
            ),
            Tool(
                name='actualizar_repositorio',
                func=actualizar_repositorio,
                description="se actualiza el repositorio de planificación"
            ),
            Tool(
                name='implementar_solicitudes_de_mejora',
                func=implementar_solicitudes_de_mejora,
                description="se implementan las solicitudes de mejora en la planificación"
            )
            ]
            
        self.memory = ConversationBufferMemory()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un asistente para llevar a cabo cada una de las indicaciones del usuario, sigue estrictamente las indicaciones proporcionadas"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        self.agent = initialize_agent(
            tools=self.tools,
            llm=ChatOpenAI(temperature=0, model="gpt-4o-mini",api_key=api_gpt),
            prompt=self.prompt,
            memory=self.memory,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            return_intermediate_steps=False,
            handle_parsing_errors=True,
        )
    
    def chat(self, input):
        try:
            response = self.agent.invoke({'input': input})
            return response
        except Exception as e:
            return str(e)
    

def main():
    agent = PlanificadorAgent()
    api_hugginface=str(input("Ingrese la api de Hugging Face: "))
    api_gpt=str(input("Ingrese la api de GPT: "))
    agent.chat("crea el repositorio de planificación")

if __name__ == "__main__":
    main()