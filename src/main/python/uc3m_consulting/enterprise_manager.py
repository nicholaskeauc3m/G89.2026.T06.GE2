"""Module """
import json
import hashlib
from datetime import datetime
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_project import EnterpriseProject


class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True

    def register_project(self, company_cif: str, project_achronym: str,
                         project_description: str, department: str,
                         date: str, budget: float):
        """Registers a new project"""
        pass
