from llamarch.common.llm import LLM
from llamarch.common.fine_tuner import FineTuner


class Student:
    def __init__(self, llm):
        """
        Initialize the Student class with a language model and fine-tuner.

        Parameters
        ----------
        llm : LLM
            An instance of the LLM class that the student will use to generate responses 
            and for fine-tuning.
        """
        self.llm = llm
        self.fine_tuner = FineTuner(llm)

    def generate_response(self, query):
        """
        Generates a response for the given query using the student LLM.

        Parameters
        ----------
        query : str
            The input query for which the student LLM generates a response.

        Returns
        -------
        str
            The generated response based on the input query.
        """
        return self.llm.generate(query)

    def fine_tune(self, data):
        """
        Fine-tunes the student LLM on the given data.

        Parameters
        ----------
        data : list
            The data used to fine-tune the student LLM. This can include various text 
            examples or datasets for training.

        Returns
        -------
        None
            The method modifies the LLM instance in place, replacing it with the fine-tuned version.
        """
        self.llm = self.fine_tuner.fine_tune(data)
