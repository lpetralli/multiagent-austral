import requests
from langchain_core.tools import tool
from typing import Dict, Any
from pydantic import BaseModel
from typing import Literal, List


class EmployeeLearningStatus(BaseModel):
    nombre: str
    apellido: str 
    sector: str
    capacitacion: Literal["SI", "NO"]

@tool
def add_employee_learning_status(
    nombre: str,
    apellido: str,
    sector: str, 
    capacitacion: Literal["SI", "NO"]
) -> Dict[Any, Any]:
    """
    Add an employee's learning status via webhook.
    
    Args:
        nombre: Employee's first name
        apellido: Employee's last name
        sector: Employee's department/sector
        capacitacion: Learning status, either "SI" or "NO"
        
    Returns:
        Dictionary containing the response data
        
    Raises:
        Exception: If the request fails
    """
    WEBHOOK_URL = "https://hook.us1.make.com/glaoqvgpbznxve282fplcv4ubzt1bqcg"
    
    try:
        # Validate data with Pydantic model
        payload = EmployeeLearningStatus(
            nombre=nombre,
            apellido=apellido,
            sector=sector,
            capacitacion=capacitacion
        )

        response = requests.post(
            WEBHOOK_URL,
            json=payload.model_dump(),
            headers={
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        response.raise_for_status()
        
        # Try to parse as JSON, if it fails return the text response
        try:
            return response.json()
        except ValueError:
            # If response is not JSON, return it as text
            return response.text
        
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status": "failed"
        }
    

class MailDraft(BaseModel):
    """Schema for mail draft data."""
    mail: str
    asunto: str 
    contenido: str

@tool
def create_one_mail_draft(
    mail: str,
    asunto: str,
    contenido: str
) -> Dict[Any, Any]:
    """
    Create ONE mail draft via webhook. Use this tool only once.
    
    Args:
        mail: Recipient email address
        asunto: Email subject
        contenido: Email content/body
        
    Returns:
        Dictionary containing the response data
        
    Raises:
        Exception: If the request fails
    """
    WEBHOOK_URL = "https://hook.us1.make.com/ttuc08gt5xsckmp4dkw4zn224avxqpu4"
    
    try:
        # Validate data with Pydantic model
        payload = MailDraft(
            mail=mail,
            asunto=asunto,
            contenido=contenido
        )

        response = requests.post(
            WEBHOOK_URL,
            json=payload.model_dump(),
            headers={
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        response.raise_for_status()
        
        # Try to parse as JSON, if it fails return the text response
        try:
            return response.json()
        except ValueError:
            # If response is not JSON, return it as text
            return response.text
        
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status": "failed"
        }

class SIUTema(BaseModel):
    nombreProfesor: str
    materia: str
    horas: str
    fecha: str
    temaDictado: str

class EventoAcademico(BaseModel):
    profesor: str
    materia: str
    evento: str
    fecha: str

@tool
def subir_tema_siu(
    nombreProfesor: str,
    materia: str,
    horas: str,
    fecha: str,
    temaDictado: str
) -> Dict[Any, Any]:
    """
    Automatiza la carga de clases dictadas en la materia de IA usando Webhooks, Google Sheets y
    filtros inteligentes que validan su existencia en el temario, ahorrando tiempo y evitando errores.
    
    Args:
        nombreProfesor: Nombre del profesor
        materia: Nombre de la materia
        horas: Número de horas
        fecha: Fecha de la clase
        temaDictado: Tema dictado
        
    Returns:
        - "Clase del [fecha] cargada correctamente": cuando los datos del cronograma/Syllabus coinciden con el pedido que hace el profesor.
        - "Error en los datos": cuando los datos del cronograma/Syllabus NO coinciden con el pedido del profesor.
        
    Raises:
        Exception: If the request fails
    """
    WEBHOOK_URL = "https://hook.us2.make.com/trx3m5faw6wjel067qhu9wer4sww88oa"
    
    try:
        # Validate data with Pydantic model
        payload = SIUTema(
            nombreProfesor=nombreProfesor,
            materia=materia,
            horas=horas,
            fecha=fecha,
            temaDictado=temaDictado
        )

        response = requests.post(
            WEBHOOK_URL,
            json=payload.model_dump(),
            headers={
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        response.raise_for_status()
        
        # Try to parse as JSON, if it fails return the text response
        try:
            return response.json()
        except ValueError:
            # If response is not JSON, return it as text
            return response.text
        
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status": "failed"
        }

@tool
def crear_recordatorio_evento(
    profesor: str,
    materia: str,
    evento: str,
    fecha: str
) -> Dict[Any, Any]:
    """
    Permite a un profesor registrar un evento académico y notificar a los alumnos de la materia Big Data
    y IA. Registra el evento en el calendario (vía Google Sheets) y crea recordatorios por alumno, la tool
    funciona para las materias IA y Big Data.
    
    Args:
        profesor: Nombre del profesor
        materia: Nombre de la materia
        evento: Descripción del evento
        fecha: Fecha del evento
        
    Returns:
        - "Recordatorio cargado correctamente": cuando el evento se registra y se encuentran alumnos correspondientes a la materia.
        - "La materia no coincide": cuando no se encuentra ningún alumno asociado a la materia indicada.
        
    Raises:
        Exception: If the request fails
    """
    WEBHOOK_URL = "https://hook.us2.make.com/oiwt4mbbldx7rrtqv0qx6epqo7257tuj"
    
    try:
        # Validate data with Pydantic model
        payload = EventoAcademico(
            profesor=profesor,
            materia=materia,
            evento=evento,
            fecha=fecha
        )

        response = requests.post(
            WEBHOOK_URL,
            json=payload.model_dump(),
            headers={
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        response.raise_for_status()
        
        # Try to parse as JSON, if it fails return the text response
        try:
            return response.json()
        except ValueError:
            # If response is not JSON, return it as text
            return response.text
        
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status": "failed"
        }


class ArchivoMateria(BaseModel):
    accion: Literal["subir", "ocultar", "visibilizar", "eliminar"]
    materia: str
    clase: str
    nombre_archivo: str

@tool
def gestionar_archivo_materia(
    accion: Literal["subir", "ocultar", "visibilizar", "eliminar"],
    materia: str,
    clase: str,
    nombre_archivo: str
) -> Dict[Any, Any]:
    """
    Permite a los profesores gestionar archivos en el campus virtual mediante cuatro acciones: subir, ocultar, visibilizar o eliminar.
    
    Args:
        accion: Acción a realizar sobre el archivo. Puede ser: subir, ocultar, visibilizar o eliminar.
        materia: Nombre de la materia donde se quiere realizar la acción. Ejemplo: 'Matemática', 'Biología', etc.
        clase: Número o identificador de la clase en la que se aplica la acción. Ejemplo: '5', 'Clase 2', etc.
        nombre_archivo: Nombre del archivo sobre el cual se realizará la acción. Puede incluir extensiones como .pdf, .docx, etc., o ser un nombre descriptivo del contenido.
        
    Returns:
        Dictionary containing the response data
        
    Raises:
        Exception: If the request fails
    """
    WEBHOOK_URL = "https://hook.us2.make.com/jb68sug209rt7e71sx8toou5to3jsjyt"
    
    try:
        # Validate data with Pydantic model
        payload = ArchivoMateria(
            accion=accion,
            materia=materia,
            clase=clase,
            nombre_archivo=nombre_archivo
        )

        response = requests.post(
            WEBHOOK_URL,
            json=payload.model_dump(),
            headers={
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        response.raise_for_status()
        
        # Try to parse as JSON, if it fails return the text response
        try:
            return response.json()
        except ValueError:
            # If response is not JSON, return it as text
            return response.text
        
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status": "failed"
        }

class RedencionGastos(BaseModel):
    fecha: str
    nombre: str
    categoria: str
    descripcion: str
    monto: str
    estado: str

@tool
def procesar_redencion_gastos(
    fecha: str,
    nombre: str,
    categoria: str,
    descripcion: str,
    monto: str,
    estado: str
) -> Dict[Any, Any]:
    """
    Procesa una factura para determinar si es reembolsable o no reembolsable según las políticas universitarias.
    Clasifica automáticamente: Viáticos, Comida y Capacitación como reembolsables; Personal como no reembolsable.
    
    Args:
        fecha: Fecha de la factura
        nombre: Nombre del responsable
        categoria: Categoría del gasto (Viáticos, Comida, Capacitación, Personal, etc.)
        descripcion: Descripción detallada del gasto
        monto: Monto de la factura
        estado: Estado del gasto
        
    Returns:
        Dictionary containing the response data
        
    Raises:
        Exception: If the request fails
    """
    WEBHOOK_URL = "https://hook.us2.make.com/7s7p05c28rltncn9bk61y6n9tyg6obr1"
    
    try:
        # Validate data with Pydantic model
        payload = RedencionGastos(
            fecha=fecha,
            nombre=nombre,
            categoria=categoria,
            descripcion=descripcion,
            monto=monto,
            estado=estado
        )

        response = requests.post(
            WEBHOOK_URL,
            json=payload.model_dump(),
            headers={
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        response.raise_for_status()
        
        # Try to parse as JSON, if it fails return the text response
        try:
            return response.json()
        except ValueError:
            # If response is not JSON, return it as text
            return response.text
        
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status": "failed"
        }


class PostLinkedIn(BaseModel):
    contenido_texto: str
    url_imagen: str

@tool
def crear_post_linkedin(
    contenido_texto: str,
    url_imagen: str
) -> Dict[Any, Any]:
    """
    Genera y publica contenido profesional en LinkedIn usando IA para crear texto alineado con la comunicación institucional.
    
    Args:
        contenido_texto: Idea o contenido base para el post
        url_imagen: URL de la imagen que acompañará el post
        
    Returns:
        Dictionary containing the response data
        
    Raises:
        Exception: If the request fails
    """
    WEBHOOK_URL = "https://hook.us2.make.com/6296k4pv2n8y1742al1b8ois4j9e9p39"
    
    try:
        # Validate data with Pydantic model
        payload = PostLinkedIn(
            contenido_texto=contenido_texto,
            url_imagen=url_imagen
        )

        response = requests.post(
            WEBHOOK_URL,
            json=payload.model_dump(),
            headers={
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        response.raise_for_status()
        
        # Try to parse as JSON, if it fails return the text response
        try:
            return response.json()
        except ValueError:
            # If response is not JSON, return it as text
            return response.text
        
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status": "failed"
        }


class ProfesorPendiente(BaseModel):
    nombre: str
    horasFaltantes: int
    horasRegistradas: int

@tool
def enviar_recordatorio_horas_siu() -> Dict[str, Any]:
    """
    Sends a reminder email to professors who have not yet logged their teaching hours. Returns a JSON with the send status and a list of professors still missing hours.
    
    Returns:
        Dictionary containing:
        - message: Status of email sending
        - profesoresPendientes: List of professors with pending hours, including:
            - nombre: Professor's full name
            - horasFaltantes: Number of hours still to log
            - horasRegistradas: Number of hours already logged
        
    Raises:
        Exception: If the request fails
    """
    WEBHOOK_URL = "https://hook.us2.make.com/4ccbfb6xuhdjhhbl1qpiltwwe5y7mt0u"
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            headers={
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        response.raise_for_status()
        
        # Try to parse as JSON, if it fails return the text response
        try:
            return response.json()
        except ValueError:
            # If response is not JSON, return it as text
            return response.text
        
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status": "failed"
        }

class ConsultaFaltas(BaseModel):
    dni: int
    materias: List[Literal["Microeconomia", "Contabilidad", "Derecho Comercial", "Estadística", "Finanzas Públicas"]]

@tool
def consultar_faltas(
    dni: int,
    materias: List[Literal["Microeconomia", "Contabilidad", "Derecho Comercial", "Estadística", "Finanzas Públicas"]] = []
) -> Dict[str, Any]:
    """
    Informa cuántas faltas tiene un alumno en una o más materias. Recibe un DNI y, opcionalmente, los nombres de las materias.
    Devuelve la cantidad de faltas por materia e indica si está en riesgo de quedar libre.
    
    Args:
        dni: DNI del alumno (ej: 44852795)
        materias: Lista opcional de materias a consultar. Si está vacía, devuelve información de todas las materias del alumno.
                 Materias posibles: Microeconomia, Contabilidad, Derecho Comercial, Estadística, Finanzas Públicas
        
    Returns:
        Dictionary containing the response data with information about absences and free course risk status
        
    Raises:
        Exception: If the request fails
    """
    WEBHOOK_URL = "https://hook.us2.make.com/ylv76tbneejnnxgnv77mmfwuciyslohm"
    
    try:
        # Validate data with Pydantic model
        payload = ConsultaFaltas(
            dni=dni,
            materias=materias
        )

        response = requests.post(
            WEBHOOK_URL,
            json=payload.model_dump(),
            headers={
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        response.raise_for_status()
        
        # Try to parse as JSON, if it fails return the text response
        try:
            return response.json()
        except ValueError:
            # If response is not JSON, return it as text
            return response.text
        
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status": "failed"
        }

class ExamenRecordatorio(BaseModel):
    mail: str
    accion: Literal["Recordatorio", "Consulta"]
    materia: Literal["Dirección Comercial", "Dirección Estratégica", "Dirección de Personas"]

@tool
def gestionar_recordatorio_examen(
    mail: str,
    accion: Literal["Recordatorio", "Consulta"],
    materia: Literal["Dirección Comercial", "Dirección Estratégica", "Dirección de Personas"]
) -> Dict[Any, Any]:
    """
    Automatiza el envío de recordatorios por correo electrónico a estudiantes sobre exámenes próximos. 
    La herramienta calcula cuántos días faltan hasta la fecha del examen y envía un mail exactamente 
    14 días antes, o de forma inmediata si quedan menos de 14 días. En caso de consulta, accede a una 
    base de datos previamente cargada y devuelve la fecha del examen correspondiente.
    
    Args:
        mail: Email del estudiante (ej: mdanon@mail.austral.edu.ar)
        accion: Acción a realizar - "Recordatorio" o "Consulta"
        materia: Nombre de la materia - "Dirección Comercial", "Dirección Estratégica", o "Dirección de Personas"
        
    Returns:
        Dictionary containing the response data
        
    Raises:
        Exception: If the request fails
    """
    WEBHOOK_URL = "https://hook.us2.make.com/cdqfv7c25zbl8j8ylsvgm8r14yarsfc1"
    
    try:
        # Validate data with Pydantic model
        payload = ExamenRecordatorio(
            mail=mail,
            accion=accion,
            materia=materia
        )

        response = requests.post(
            WEBHOOK_URL,
            json=payload.model_dump(),
            headers={
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        response.raise_for_status()
        
        # Try to parse as JSON, if it fails return the text response
        try:
            return response.json()
        except ValueError:
            # If response is not JSON, return it as text
            return response.text
        
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status": "failed"
        }