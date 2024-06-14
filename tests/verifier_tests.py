import unittest
from request_analyzer.verifiers.abstract_verif import ValueStages
from request_analyzer.verifiers.departure_verif import DepartureVerif
from request_analyzer.verifiers.destination_verif import DestinationVerif
from request_analyzer.verifiers.arrival_verif import ArrivalVerif
from request_analyzer.verifiers.return_verif import ReturnVerif
from request_analyzer.verifiers.budget_verif import BudgetVerif

class TestRetrievers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        cls.departure_verif = DepartureVerif()
        cls.destination_verif = DestinationVerif()
        cls.arrival_verif = ArrivalVerif()
        cls.return_verif = ReturnVerif()
        cls.budget_verif = BudgetVerif()

    def test_departure_verif(self):
        test_cases = [
            {"retrieved_field": 'None', "expected_answer": (ValueStages.FIELD_NOT_FOUND, "The user has not entered this field")},
            {"retrieved_field": 'Муром', "expected_answer": (ValueStages.OK, "Everything is good")},
            {"retrieved_field": 'Иннополис', "expected_answer": (ValueStages.OK, "Everything is good")},
            {"retrieved_field": 'None', "expected_answer": (ValueStages.FIELD_NOT_FOUND, "The user has not entered this field")}
        ]

        for case in test_cases:
            retrieved_field = case["retrieved_field"]
            expected_answer = case["expected_answer"]
            verification_result = self.departure_verif.verify(retrieved_field)
            self.assertEqual(verification_result, expected_answer, f"Failed for request: {retrieved_field}")

    def test_destination_verif(self):
        test_cases = [
            {"retrieved_field": 'None', "expected_answer": (ValueStages.FIELD_NOT_FOUND, "The user has not entered this field")},
            {"retrieved_field": 'Муром', "expected_answer": (ValueStages.OK, "Everything is good")},
            {"retrieved_field": 'Иннополис', "expected_answer": (ValueStages.OK, "Everything is good")},
            {"retrieved_field": 'None', "expected_answer": (ValueStages.FIELD_NOT_FOUND, "The user has not entered this field")}
        ]

        for case in test_cases:
            retrieved_field = case["retrieved_field"]
            expected_answer = case["expected_answer"]
            verification_result = self.destination_verif.verify(retrieved_field)
            self.assertEqual(verification_result, expected_answer, f"Failed for request: {retrieved_field}")

    def test_arrival_verif(self):
        test_cases = [
            {"retrieved_field": 'None', "expected_answer": (ValueStages.FIELD_NOT_FOUND, "The user has not entered this field")},
            {"retrieved_field": 'Муром', "expected_answer": (ValueStages.INCORRECT_VALUE, "The user entered wrong arrival time")},
            {"retrieved_field": '02/12/2023', "expected_answer": (ValueStages.INCORRECT_VALUE, "The user entered wrong arrival time")},
            {"retrieved_field": '02/13/2025', "expected_answer": (ValueStages.INCORRECT_VALUE, "The user entered wrong arrival time")},
            {"retrieved_field": '02/10/2024', "expected_answer": (ValueStages.OK, "Everything is good")}
        ]

        for case in test_cases:
            retrieved_field = case["retrieved_field"]
            expected_answer = case["expected_answer"]
            verification_result = self.arrival_verif.verify(retrieved_field)
            self.assertEqual(verification_result, expected_answer, f"Failed for request: {retrieved_field}")
    
    def test_return_verif(self):
        test_cases = [
            {"retrieved_field": 'None', "expected_answer": (ValueStages.FIELD_NOT_FOUND, "The user has not entered this field")},
            {"retrieved_field": 'Муром', "expected_answer": (ValueStages.INCORRECT_VALUE, "The user entered wrong arrival time")},
            {"retrieved_field": '02/12/2023', "expected_answer": (ValueStages.INCORRECT_VALUE, "The user entered wrong arrival time")},
            {"retrieved_field": '02/13/2025', "expected_answer": (ValueStages.INCORRECT_VALUE, "The user entered wrong arrival time")},
            {"retrieved_field": '02/10/2024', "expected_answer": (ValueStages.OK, "Everything is good")}
        ]

        for case in test_cases:
            retrieved_field = case["retrieved_field"]
            expected_answer = case["expected_answer"]
            verification_result = self.return_verif.verify(retrieved_field)
            self.assertEqual(verification_result, expected_answer, f"Failed for request: {retrieved_field}")

    def test_budget_verif(self):
        test_cases = [
            {"retrieved_field": 'None', "expected_answer": (ValueStages.FIELD_NOT_FOUND, "The user has not entered this field")},
            {"retrieved_field": 'Муром', "expected_answer":(ValueStages.INCORRECT_VALUE, "The user has entered wrong budget")},
            {"retrieved_field": '-10243', "expected_answer": (ValueStages.INCORRECT_VALUE, "The user has entered wrong budget")},
            {"retrieved_field": '0.32', "expected_answer": (ValueStages.INCORRECT_VALUE, "The user has entered wrong budget")},
            {"retrieved_field": '10000', "expected_answer": (ValueStages.OK, "Everything is good")}
        ]

        for case in test_cases:
            retrieved_field = case["retrieved_field"]
            expected_answer = case["expected_answer"]
            verification_result = self.budget_verif.verify(retrieved_field)
            self.assertEqual(verification_result, expected_answer, f"Failed for request: {retrieved_field}")

if __name__ == '__main__':
    unittest.main()
