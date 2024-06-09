from vllm import LLM, SamplingParams

class DepartureRetriever:
    """
    A class designed to retrieve departure
    cities from user travel requests using a 
    VLLM.

    Attributes:
        llm (LLM): An instance of a VLLM
                   used for generating text 
                   based on prompts.
        sampling_params (SamplingParams): Parameters 
                   for controlling the sampling behavior
                   of the VLLM during text generation.
        prefix_prompt (str): A predefined prompt template
                   that guides the VLLM to focus on extracting
                   departure cities from user requests.
    """

    def __init__(self, llm: LLM) -> None:
        """
        Initializes the DepartureRetriever with a given VLLM
        instance and sets up default sampling parameters and 
        a prompt template.

        Args:
            llm (LLM): The VLLM instance to be used for text
                       generation.
        """
        self.llm = llm
        # Setting up sampling parameters for deterministic 
        # output
        self.sampling_params = SamplingParams(temperature=0,
                                              stop="\n")
        # Defining a prompt template to guide the model towards
        # extracting departure cities
        self.prefix_prompt = \
        '''Your task is to extract departure city from user request. Examples:
        Q: "Планирую сгонять в Хабаровск через три недели."
        A: Departure: "None"

        Q: "Хочу уехать из Москвы куда-нибудь на три дня"
        A: Departure: "Москва"

        Q: "Уеду в Питер из Казани в июле с 12 по 17 числа"
        A: Departure: "Казань"

        Q: "Уеду в Москву из Рязани в августе с 10 по 30. Бюджет 70 тысяч."
        A: Departure: "Рязань"

        Q: "Уеду из Рязани в августе с 10 по 30. Бюджет 70 тысяч."
        A: Departure: "Рязань"

        Q: "Я в Тольятти. Мне срочно надо достать билеты в Кисловодск"
        A: Departure: "Тольятти"

        Q: "USER_REQUEST"
        A: Departure: "'''

    def retrieve(self, request: str) -> str:
        """
        Generates a response from the VLLM based on 
        the user's travel request, aiming to extract 
        the departure city.

        Args:
            request (str): The user's travel request 
                           as a string.

        Returns:
            str: The extracted departure city as a 
                 string, or a message indicating the
                 departure city could not be determined.
        """
        # Replace the placeholder in the prompt template 
        # with the actual user request
        prompt = self.prefix_prompt.replace("USER_REQUEST",
                                            request)
        # Generate a response from the VLLM using the 
        # customized prompt and sampling parameters
        vllm_output = self.llm.generate(prompt, 
                                        self.sampling_params)
        # Extract and return the generated text as 
        # the departure city
        return vllm_output[0].outputs[0].text
