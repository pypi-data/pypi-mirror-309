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
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


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
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key="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")
    
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
    

class PlanificadorAgent:
    def __init__(self):
        self.token = None
        self.embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=self.token, model_name="sentence-transformers/all-MiniLM-l6-v2"
        )

        self.persist_directory = os.path.normpath("danilo_planner\\ChromaDB")
        self.persist_directory_plan = os.path.normpath("danilo_planner\\PlanificacionL.txt")
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
            )]
            
        self.memory = ConversationBufferMemory()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un asistente para llevar a cabo cada una de las indicaciones del usuario, sigue estrictamente las indicaciones proporcionadas"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        self.agent = initialize_agent(
            tools=self.tools,
            llm=ChatOpenAI(temperature=0, model="gpt-4o-mini",api_key=token),
            prompt=self.prompt,
            memory=self.memory,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            return_intermediate_steps=False,
            handle_parsing_errors=True,
        )
    
    def chat(self, input):
        try:
            response = self.agent(input)
            return response
        except Exception as e:
            return str(e)
    
    @property
    def token(self):
        """Getter para _token"""
        return self.token

    @token.setter
    def token(self, value):
        """Setter para _token"""
        self.token = value
    
def main():
#"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"
    agent = PlanificadorAgent()

    agent.chat("crea la planificación de un proyecto de innovación en el sector carbón del departamento norte de Santander de forma no extensa")

if __name__ == "__main__":
    main()