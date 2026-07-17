import os
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

class LogisticsAgentFactory:
    """Isolates high-context corporate agent personas for supply chain mitigation"""
    
    def __init__(self, agent_persona: str):
        # Using gpt-4o-mini as a high-speed, cost-efficient enterprise engine
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, timeout=15)
        self.agent_persona = agent_persona

    def process_task(self, state_context: str) -> str:
        if self.agent_persona == "ingestor":
            system_prompt = (
                "You are an Enterprise Supply Chain Ingestion Specialist. Your job is to extract "
                "critical component details, affected factory regions, and vendor parameters from raw incoming data streams. "
                "Output your findings cleanly in unstructured text using precise technical labels."
            )
        elif self.agent_persona == "finops_analyst":
            system_prompt = (
                "You are a Corporate FinOps & Logistics Cost Optimizer. Analyze the current vendor "
                "shortage profiles and alternative component options. Compute direct financial trade-offs, "
                "estimate shipping premiums, and determine a running operational budget matrix."
            )
        elif self.agent_persona == "self_healer":
            system_prompt = (
                "You are an Automated Database SRE Remediation Specialist. Your job is to analyze "
                "failed tool function schema parameters or database exceptions. You must diagnose the structural "
                "mismatch, rewrite the query arguments into a correct JSON format, and document the self-healing step."
            )
        else:
            system_prompt = "You are a Logistics Operations Director. Compile a definitive mitigation playbook."

        response = self.llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=state_context)])
        return response.content