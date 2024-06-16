import unittest
from vllm import LLM

from request_analyzer.information_retriever import InformationRetriever
from request_analyzer.more_info_required_message_generator import MoreInfoRequiredMessageGenerator


class TestMessageGenerators(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        model_name = "meta-llama/Meta-Llama-3-8B"

        # Initialize the LLM
        cls.llm = LLM(
            model=model_name,
            tensor_parallel_size=1,  # Adjust as needed based on your GPU setup
            gpu_memory_utilization=0.4,
            enforce_eager=True,
            enable_chunked_prefill=True,
            max_num_batched_tokens=2048)

        cls.information_retr = InformationRetriever(cls.llm)
        cls.more_info_required_msg_gen = MoreInfoRequiredMessageGenerator(
            cls.llm)

    def test_more_info_required_msg_gen(self):
        request = "Хочу сгонять в Магадан из Санкт Петербурга. Планирую лететь туда 12 августа."
        information_retriever_result = self.information_retr.retrieve(request)
        field_verification_map, _, post_verification_results = information_retriever_result
        message_generated = self.more_info_required_msg_gen.generate_message(
            request, field_verification_map, post_verification_results)
        self.assertIn("бюджет", message_generated)
        self.assertIn("дату возвращения", message_generated)


if __name__ == '__main__':
    unittest.main()
