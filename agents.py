# agents.py
import autogen
from autogen import AssistantAgent, UserProxyAgent
from config import llm_config
from system_messages import *
from utils import *

def create_agents():
    # User Proxy Agent
    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="TERMINATE",
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={"use_docker": False},
        llm_config=llm_config,
        system_message=USER_PROXY_MSG
    )

    # Data Source Manager Agent
    data_source_manager = AssistantAgent(
        name="data_source_manager",
        llm_config=llm_config,
        system_message=DATA_SOURCE_MANAGER_MSG
    )

    # Data Quality Assessment Agent
    data_quality_agent = AssistantAgent(
        name="data_quality_agent",
        llm_config=llm_config,
        system_message=DATA_QUALITY_AGENT_MSG
    )

    # Statistical Analysis Agent
    statistical_agent = AssistantAgent(
        name="statistical_agent",
        llm_config=llm_config,
        system_message=STATISTICAL_AGENT_MSG
    )

    # Qualitative Analysis Agent
    qualitative_agent = AssistantAgent(
        name="qualitative_agent",
        llm_config=llm_config,
        system_message=QUALITATIVE_AGENT_MSG
    )

    # Visualization Agent
    visualization_agent = AssistantAgent(
        name="visualization_agent",
        llm_config=llm_config,
        system_message=VISUALIZATION_AGENT_MSG
    )

    # Report Generation Agent
    report_generation_agent = AssistantAgent(
        name="report_generation_agent",
        llm_config=llm_config,
        system_message=REPORT_GENERATION_MSG
    )

    # Register functions for each agent
    user_proxy.register_for_execution()(download_dataset_via_git)
    user_proxy.register_for_execution()(get_dataset_file_paths)
    user_proxy.register_for_execution()(assess_data_quality)
    user_proxy.register_for_execution()(perform_statistical_analysis)
    user_proxy.register_for_execution()(perform_qualitative_analysis)
    user_proxy.register_for_execution()(create_visualizations)
    user_proxy.register_for_execution()(generate_pdf_report)

    return {
        'user_proxy': user_proxy,
        'data_source_manager': data_source_manager,
        'data_quality_agent': data_quality_agent,
        'statistical_agent': statistical_agent,
        'qualitative_agent': qualitative_agent,
        'visualization_agent': visualization_agent,
        'report_generation_agent': report_generation_agent
    }