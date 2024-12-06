class OutputIntegrator:
    @staticmethod
    def integrate_outputs(responses):
        """
        Combines outputs from different agents.

        This method integrates responses from different agents into a single output. 
        The current implementation concatenates responses with a separator, but 
        this can be customized to merge outputs in other ways as needed.

        Parameters
        ----------
        responses : list of AgentResponse
            A list of responses from different agents. Each response is expected 
            to have a `response` attribute containing the agent's output text.

        Returns
        -------
        str
            The integrated output, which is a concatenation of all agent responses 
            separated by a " | " delimiter.
        """
        integrated_output = " | ".join(
            r.response for r in responses)
        return integrated_output
