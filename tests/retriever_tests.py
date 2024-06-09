import os
import unittest
from vllm import LLM
from request_analyzer.retreivers.destination_retriever import DestinationRetriever
from request_analyzer.retreivers.departure_retriever import DepartureRetriever

class TestRetrievers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # # Check for the HF_TOKEN environment variable
        # if "HF_TOKEN" not in os.environ:
        #     raise EnvironmentError("The environment variable 'HF_TOKEN' is not set. "
        #                            "Please set it to your Hugging Face access token "
        #                            "before running the tests.")
        
        # Specify the primary GPU to use (GPU 0, which has more available memory)
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"

        # Setting PyTorch environment variable for better memory management
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

        # Model configuration (assuming you have a model_name variable defined)
        model_name = "meta-llama/Meta-Llama-3-8B"

        # Initialize the LLM
        cls.llm = LLM(
            model=model_name,
            tensor_parallel_size=1,  # Adjust as needed based on your GPU setup
            gpu_memory_utilization=0.4,
            enforce_eager=True,
            enable_chunked_prefill=True,
            max_num_batched_tokens=2048
        )

        cls.departure_retr = DepartureRetriever(cls.llm)
        cls.destination_retr = DestinationRetriever(cls.llm)

    def test_departure_retriever(self):
        test_cases = [
            {"request": "Планирую уехать в Минеральные воды через три недели.", "expected_departure": 'None"'},
            {"request": "Хочу уехать из Мурома куда-нибудь на три дня", "expected_departure": 'Муром"'},
            {"request": "Уеду в Питер из Иннополиса в июле с 12 по 17 числа", "expected_departure": 'Иннополис"'},
            {"request": "Мне срочно надо достать билеты в Кисловодск", "expected_departure": 'None"'}
        ]

        for case in test_cases:
            request = case["request"]
            expected_departure = case["expected_departure"]
            retrieved_departure = self.departure_retr.retrieve(request).strip()
            self.assertEqual(retrieved_departure.lower(), expected_departure.lower(), f"Failed for request: {request}")

    def test_destination_retriever(self):
        test_cases = [
            {"request": "Планирую уехать в Минеральные воды через три недели.", "expected_destination": 'Минеральные воды"'},
            {"request": "Хочу уехать из Мурома куда-нибудь на три дня", "expected_destination": 'None"'},
            {"request": "Уеду в Питер из Иннополиса в июле с 12 по 17 числа", "expected_destination": 'Санкт-Петербург"'},
            {"request": "Мне срочно надо достать билеты в Кисловодск", "expected_destination": 'Кисловодск"'}
        ]

        for case in test_cases:
            request = case["request"]
            expected_destination = case["expected_destination"]
            retrieved_destination = self.destination_retr.retrieve(request).strip()
            self.assertEqual(retrieved_destination.lower(), expected_destination.lower(), f"Failed for request: {request}")

if __name__ == '__main__':
    unittest.main()
