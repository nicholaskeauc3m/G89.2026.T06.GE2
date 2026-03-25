"""class for testing the register_project method"""
import os
import unittest
from uc3m_consulting import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class TestRegisterProject(unittest.TestCase):
    """Test cases for register_project - Equivalence Classes & Boundary Values"""

    def setUp(self):
        """Set up valid default inputs reused across tests"""
        self.manager = EnterpriseManager()
        self.valid_cif = "A1234567D"
        self.valid_acronym = "PROJ1"
        self.valid_description = "Valid Project Desc"
        self.valid_department = "HR"
        self.valid_date = "01/06/2026"
        self.valid_budget = 50000.00
        if os.path.exists("corporate_operations.json"):
            os.remove("corporate_operations.json")

    def test_tc01_valid_all_inputs(self):
        """TC_01 - All valid inputs should return a 32-char MD5 string"""
        result = self.manager.register_project(
            self.valid_cif, self.valid_acronym,
            self.valid_description, self.valid_department,
            self.valid_date, self.valid_budget
        )
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 32)

    def test_tc02_invalid_cif_wrong_letter(self):
        """TC_02 - CIF with invalid first letter should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                "11234567J", self.valid_acronym,
                self.valid_description, self.valid_department,
                self.valid_date, self.valid_budget
            )

    def test_tc03_invalid_cif_wrong_digit_count(self):
        """TC_03 - CIF with wrong number of digits should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                "A123456J", self.valid_acronym,
                self.valid_description, self.valid_department,
                self.valid_date, self.valid_budget
            )

    def test_tc04_invalid_cif_wrong_control(self):
        """TC_04 - CIF with invalid control character should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                "A1234567X", self.valid_acronym,
                self.valid_description, self.valid_department,
                self.valid_date, self.valid_budget
            )

    def test_tc05_invalid_cif_empty(self):
        """TC_05 - Empty CIF should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                "", self.valid_acronym,
                self.valid_description, self.valid_department,
                self.valid_date, self.valid_budget
            )

    def test_tc06_acronym_too_short_boundary(self):
        """TC_06 - Acronym with 4 chars should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, "PRJ1",
                self.valid_description, self.valid_department,
                self.valid_date, self.valid_budget
            )

    def test_tc07_acronym_min_boundary_valid(self):
        """TC_07 - Acronym with exactly 5 chars should be valid"""
        result = self.manager.register_project(
            self.valid_cif, "PROJ1",
            self.valid_description, self.valid_department,
            self.valid_date, self.valid_budget
        )
        self.assertEqual(len(result), 32)

    def test_tc08_acronym_max_boundary_valid(self):
        """TC_08 - Acronym with exactly 10 chars should be valid"""
        result = self.manager.register_project(
            self.valid_cif, "PROJ123456",
            self.valid_description, self.valid_department,
            self.valid_date, self.valid_budget
        )
        self.assertEqual(len(result), 32)

    def test_tc09_acronym_too_long_boundary(self):
        """TC_09 - Acronym with 11 chars should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, "PROJ1234567",
                self.valid_description, self.valid_department,
                self.valid_date, self.valid_budget
            )

    def test_tc10_acronym_invalid_chars_lowercase(self):
        """TC_10 - Acronym with lowercase letters should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, "proj1",
                self.valid_description, self.valid_department,
                self.valid_date, self.valid_budget
            )

    def test_tc11_acronym_invalid_chars_special(self):
        """TC_11 - Acronym with special characters should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, "PRJ-1",
                self.valid_description, self.valid_department,
                self.valid_date, self.valid_budget
            )

    def test_tc12_description_too_short_boundary(self):
        """TC_12 - Description with 9 chars should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, self.valid_acronym,
                "123456789", self.valid_department,
                self.valid_date, self.valid_budget
            )

    def test_tc13_description_min_boundary_valid(self):
        """TC_13 - Description with exactly 10 chars should be valid"""
        result = self.manager.register_project(
            self.valid_cif, self.valid_acronym,
            "1234567890", self.valid_department,
            self.valid_date, self.valid_budget
        )
        self.assertEqual(len(result), 32)

    def test_tc14_description_max_boundary_valid(self):
        """TC_14 - Description with exactly 30 chars should be valid"""
        result = self.manager.register_project(
            self.valid_cif, self.valid_acronym,
            "123456789012345678901234567890", self.valid_department,
            self.valid_date, self.valid_budget
        )
        self.assertEqual(len(result), 32)

    def test_tc15_description_too_long_boundary(self):
        """TC_15 - Description with 31 chars should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, self.valid_acronym,
                "1234567890123456789012345678901", self.valid_department,
                self.valid_date, self.valid_budget
            )

    def test_tc16_department_hr_valid(self):
        """TC_16 - Department HR should be valid"""
        result = self.manager.register_project(
            self.valid_cif, self.valid_acronym,
            self.valid_description, "HR",
            self.valid_date, self.valid_budget
        )
        self.assertEqual(len(result), 32)

    def test_tc17_department_finance_valid(self):
        """TC_17 - Department FINANCE should be valid"""
        result = self.manager.register_project(
            self.valid_cif, self.valid_acronym,
            self.valid_description, "FINANCE",
            self.valid_date, self.valid_budget
        )
        self.assertEqual(len(result), 32)

    def test_tc18_department_legal_valid(self):
        """TC_18 - Department LEGAL should be valid"""
        result = self.manager.register_project(
            self.valid_cif, self.valid_acronym,
            self.valid_description, "LEGAL",
            self.valid_date, self.valid_budget
        )
        self.assertEqual(len(result), 32)

    def test_tc19_department_logistics_valid(self):
        """TC_19 - Department LOGISTICS should be valid"""
        result = self.manager.register_project(
            self.valid_cif, self.valid_acronym,
            self.valid_description, "LOGISTICS",
            self.valid_date, self.valid_budget
        )
        self.assertEqual(len(result), 32)

    def test_tc20_department_invalid(self):
        """TC_20 - Department MARKETING should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, self.valid_acronym,
                self.valid_description, "MARKETING",
                self.valid_date, self.valid_budget
            )

    def test_tc21_department_lowercase_invalid(self):
        """TC_21 - Lowercase department should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, self.valid_acronym,
                self.valid_description, "hr",
                self.valid_date, self.valid_budget
            )

    def test_tc22_date_wrong_format(self):
        """TC_22 - Date in wrong format should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, self.valid_acronym,
                self.valid_description, self.valid_department,
                "2026/06/01", self.valid_budget
            )

    def test_tc23_date_year_too_early_boundary(self):
        """TC_23 - Date with year 2024 should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, self.valid_acronym,
                self.valid_description, self.valid_department,
                "01/06/2024", self.valid_budget
            )

    def test_tc24_date_year_max_boundary_valid(self):
        """TC_24 - Date with year 2027 should be valid"""
        result = self.manager.register_project(
            self.valid_cif, self.valid_acronym,
            self.valid_description, self.valid_department,
            "01/06/2027", self.valid_budget
        )
        self.assertEqual(len(result), 32)

    def test_tc25_date_year_too_late_boundary(self):
        """TC_25 - Date with year 2028 should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, self.valid_acronym,
                self.valid_description, self.valid_department,
                "01/06/2028", self.valid_budget
            )

    def test_tc26_date_invalid_month(self):
        """TC_26 - Month 13 should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, self.valid_acronym,
                self.valid_description, self.valid_department,
                "01/13/2026", self.valid_budget
            )

    def test_tc27_date_invalid_day(self):
        """TC_27 - Day 32 should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, self.valid_acronym,
                self.valid_description, self.valid_department,
                "32/06/2026", self.valid_budget
            )

    def test_tc28_date_in_the_past(self):
        """TC_28 - Date in the past should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, self.valid_acronym,
                self.valid_description, self.valid_department,
                "01/01/2025", self.valid_budget
            )

    def test_tc29_budget_below_min_boundary(self):
        """TC_29 - Budget 49999.99 should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, self.valid_acronym,
                self.valid_description, self.valid_department,
                self.valid_date, 49999.99
            )

    def test_tc30_budget_min_boundary_valid(self):
        """TC_30 - Budget exactly 50000.00 should be valid"""
        result = self.manager.register_project(
            self.valid_cif, self.valid_acronym,
            self.valid_description, self.valid_department,
            self.valid_date, 50000.00
        )
        self.assertEqual(len(result), 32)

    def test_tc31_budget_max_boundary_valid(self):
        """TC_31 - Budget exactly 1000000.00 should be valid"""
        result = self.manager.register_project(
            self.valid_cif, self.valid_acronym,
            self.valid_description, self.valid_department,
            self.valid_date, 1000000.00
        )
        self.assertEqual(len(result), 32)

    def test_tc32_budget_above_max_boundary(self):
        """TC_32 - Budget 1000000.01 should raise exception"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, self.valid_acronym,
                self.valid_description, self.valid_department,
                self.valid_date, 1000000.01
            )

    def test_tc33_duplicate_project_same_cif_and_acronym(self):
        """TC_33 - Registering same CIF + acronym twice should raise exception"""
        self.manager.register_project(
            self.valid_cif, self.valid_acronym,
            self.valid_description, self.valid_department,
            self.valid_date, self.valid_budget
        )
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_project(
                self.valid_cif, self.valid_acronym,
                self.valid_description, self.valid_department,
                self.valid_date, self.valid_budget
            )


if __name__ == '__main__':
    unittest.main()