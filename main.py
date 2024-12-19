# main.py
from autogen import GroupChat, GroupChatManager
from agents import create_agents
from config import llm_config
from system_messages import ORCHESTRATOR_MSG

def setup_group_chat():
    agents = create_agents()
    
    group_chat = GroupChat(
        agents=[
            agents['user_proxy'],
            agents['data_source_manager'],
            agents['data_quality_agent'],
            agents['statistical_agent'],
            agents['qualitative_agent'],
            agents['visualization_agent'],
            agents['report_generation_agent']
        ],
        messages=[],
        max_round=50
    )

    orchestrator = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config,
        system_message=ORCHESTRATOR_MSG
    )

    return agents['user_proxy'], orchestrator

def process_dataset(url: str):
    """
    Main function to initiate the chat with the orchestrator
    """
    user_proxy, orchestrator = setup_group_chat()
    user_proxy.initiate_chat(
        orchestrator,
        message=url,
        summary_method="reflection_with_llm"
    )

if __name__ == "_main_":
    dataset_url = "https://huggingface.co/datasets/scikit-learn/iris"
    process_dataset(dataset_url)
