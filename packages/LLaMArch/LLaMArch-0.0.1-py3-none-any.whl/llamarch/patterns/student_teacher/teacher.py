from llamarch.common.llm import LLM

EVALUATION_PROMPT = "Evaluate the following response based on relevance, accuracy, and clarity and suggest a better answer:"


class Teacher:
    def __init__(self, llm, evaluation_prompt=EVALUATION_PROMPT):
        """
        Initialize the Teacher class with a language model and an optional evaluation prompt.

        Parameters
        ----------
        llm : LLM
            An instance of the LLM class used to generate evaluation feedback.
        evaluation_prompt : str, optional
            The prompt template for evaluating student responses, by default EVALUATION_PROMPT.
        """
        self.llm = llm
        self.evaluation_prompt = evaluation_prompt

    def evaluate_response(self, student_response):
        """
        Evaluates the student's response by providing feedback or a score.

        Parameters
        ----------
        student_response : str
            The student's response to be evaluated.

        Returns
        -------
        str
            The generated evaluation feedback or score based on the student's response.
        """
        # Construct an evaluation prompt
        prompt = f"{self.evaluation_prompt} {student_response}"
        evaluation_text = self.llm.generate(prompt)
        return evaluation_text
