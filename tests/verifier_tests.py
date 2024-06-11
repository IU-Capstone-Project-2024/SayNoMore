import unittest
from request_analyzer.verifiers.abstract_verif import ValueStages
from request_analyzer.verifiers.departure_verif import DepartureVerif
from request_analyzer.verifiers.destination_verif import DestinationVerif

class TestRetrievers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        cls.departure_verif = DepartureVerif()
        cls.destination_verif = DestinationVerif()

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

if __name__ == '__main__':
    unittest.main()
