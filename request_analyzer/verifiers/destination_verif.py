from typing import Tuple
from request_analyzer.verifiers.abstract_verif import *

class DestinationVerif(BaseVerifier):
    
    def __init__(self) -> None:
        super().__init__()
    
    def verify(self, retrieved_value: str) -> Tuple[ValueStages, str]:
        if retrieved_value == "None":
            return (ValueStages.FIELD_NOT_FOUND, "The user has not entered this field")
        return (ValueStages.OK, "Everything is good")