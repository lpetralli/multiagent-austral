import requests
from langchain_core.tools import tool
from typing import Dict, Any
from pydantic import BaseModel
from typing import Literal


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
        return {
            "status": "success",
            "message": "Employee learning status added successfully"
        }
        
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
        return {
            "status": "success",
            "message": "Mail draft created successfully"
        }
        
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status": "failed"
        }
