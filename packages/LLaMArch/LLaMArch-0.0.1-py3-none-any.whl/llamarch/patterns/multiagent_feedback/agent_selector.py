class AgentSelector:
    def __init__(self, agents):
        """
        Initialize with a list of available agents.

        Parameters
        ----------
        agents : list
            A list of available agent objects to select from.
        """
        self.agents = agents

    def select_agents(self, query):
        """
        Select agents based on the query.

        Parameters
        ----------
        query : str
            The query used to select agents. The selection logic can be customized based on the query content.

        Returns
        -------
        list
            A list of selected agents based on the query. If no specific selection is made, all agents are returned.
        """
        selected_agents = [
            agent for agent in self.agents if "some_condition" in query]
        if not selected_agents:
            selected_agents = self.agents  # Fallback to all agents if no specific selection
        return selected_agents
