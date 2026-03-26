"""Module """
import json
import os
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

    # pylint: disable=too-many-arguments, too-many-positional-arguments, too-many-branches
    def register_project(self, company_cif: str, project_achronym: str,
                         project_description: str, department: str,
                         date: str, budget: float):
        """Registers a new project"""
        if not self.validate_cif(company_cif):
            raise EnterpriseManagementException("Invalid Company CIF")
        if not isinstance(project_achronym, str):
            raise EnterpriseManagementException("Invalid Project Acronym")
        if not 5 <= len(project_achronym) <= 10:
            raise EnterpriseManagementException("Invalid Project Acronym")
        if not re.match(r'^[A-Z0-9]+$', project_achronym):
            raise EnterpriseManagementException("Invalid Project Acronym")
        if not isinstance(project_description, str):
            raise EnterpriseManagementException("Invalid Project Description")
        if not 10 <= len(project_description) <= 30:
            raise EnterpriseManagementException("Invalid Project Description")
        if department not in ("HR", "FINANCE", "LEGAL", "LOGISTICS"):
            raise EnterpriseManagementException("Invalid Department")
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', date):
            raise EnterpriseManagementException("Invalid Date")
        try:
            date_obj = datetime.strptime(date, "%d/%m/%Y")
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid Date") from exc
        if not 2025 <= date_obj.year <= 2027:
            raise EnterpriseManagementException("Invalid Date")
        if date_obj.date() < datetime.now().date():
            raise EnterpriseManagementException("Invalid Date")
        if not isinstance(budget, float):
            raise EnterpriseManagementException("Invalid Budget")
        if round(budget * 100) != budget * 100:
            raise EnterpriseManagementException("Invalid Budget")
        if not 50000.00 <= budget <= 1000000.00:
            raise EnterpriseManagementException("Invalid Budget")
        json_file = "corporate_operations.json"
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entry in data:
                if entry["company_cif"] == company_cif and \
                        entry["project_acronym"] == project_achronym:
                    raise EnterpriseManagementException("Duplicate project")
        else:
            data = []
        project = EnterpriseProject(company_cif, project_achronym,
                                    project_description, department,
                                    date, budget)
        data.append(project.to_json())
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return project.project_id
