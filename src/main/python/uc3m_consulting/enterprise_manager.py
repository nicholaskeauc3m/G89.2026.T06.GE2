"""Module """
import json
import re
from datetime import datetime
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_project import EnterpriseProject


class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str) -> bool:
        """Validates a Spanish CIF code"""
        if not isinstance(cif, str) or len(cif) != 9:
            return False
        if not cif[0].isalpha():
            return False
        if not cif[1:8].isdigit():
            return False
        digits = [int(d) for d in cif[1:8]]
        odd_sum = sum(
            (d * 2 - 9 if d * 2 > 9 else d * 2)
            for d in digits[0::2]
        )
        even_sum = sum(digits[1::2])
        total = odd_sum + even_sum
        control_num = (10 - (total % 10)) % 10
        letter_map = "JABCDEFGHI"
        return cif[8] == str(control_num) or cif[8] == letter_map[control_num]

    def register_project(self, company_cif: str, project_achronym: str,
                         project_description: str, department: str,
                         date: str, budget: float):
        """Registers a new project"""
        # Validate CIF
        if not self.validate_cif(company_cif):
            raise EnterpriseManagementException("Invalid Company CIF")

        # Validate acronym
        if not isinstance(project_achronym, str):
            raise EnterpriseManagementException("Invalid Project Acronym")
        if not (5 <= len(project_achronym) <= 10):
            raise EnterpriseManagementException("Invalid Project Acronym")
        if not re.match(r'^[A-Z0-9]+$', project_achronym):
            raise EnterpriseManagementException("Invalid Project Acronym")

        project = EnterpriseProject(company_cif, project_achronym,
                                    project_description, department,
                                    date, budget)
        return project.project_id