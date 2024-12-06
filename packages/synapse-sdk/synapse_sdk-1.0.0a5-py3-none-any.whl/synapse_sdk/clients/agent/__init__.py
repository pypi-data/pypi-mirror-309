from synapse_sdk.clients.agent.service import ServiceClientMixin


class AgentClient(ServiceClientMixin):
    name = 'Agent'
    agent_token = None
    user_token = None
    tenant = None

    def __init__(self, base_url, agent_token, user_token, tenant):
        super().__init__(base_url)
        self.agent_token = agent_token
        self.user_token = user_token
        self.tenant = tenant

    def _get_headers(self):
        return {
            'Authorization': self.agent_token,
            'SYNAPSE-User': f'Token {self.user_token}',
            'SYNAPSE-Tenant': f'Token {self.tenant}',
        }
