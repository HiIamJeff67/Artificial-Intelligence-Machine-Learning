import json
import random
from typing import *

def concatenate_informations_to_dataset(
    count: int = 100,
    output_path = None, 
    npc_informations_json_path: str = "data/npc_informations.json", 
    environment_informations_json_path: str = "data/environment_informations.json", 
) -> List[Dict[str, Any]]:
    """
    Concatenate NPC and environment information into a dataset for conversations.

    Args:
        count (int): Number of conversation samples to generate.
        output_path (str): File path to save the generated dataset as JSON.
        npc_informations_json_path (str): Path to the NPC information JSON file.
        environment_informations_json_path (str): Path to the environment information JSON file.

    Returns:
        List[Dict[str, Any]]: A list of conversation dictionaries, each containing player input, NPC info, environment info, and NPC output.
    Raises:
        Exception: If output_path is not provided or if input files are empty.
    """
    if not output_path:
        raise Exception("Please provide a output file as a parameter of output_file")
    
    result = []
    # Randomly select NPC and environment information for each sample
    for _ in range(count):
        selected_npc_information = None
        selected_environment_information = None
        with open(npc_informations_json_path, 'r') as f:
            data = json.load(f)
            selected_npc_information = random.choice(data)
        with open(environment_informations_json_path, 'r') as f:
            data = json.load(f)
            selected_environment_information = random.choice(data)
        if not selected_npc_information or not selected_environment_information:
            raise Exception("No any data in the npc_informations_json_path or environment_informations_json_path")
        conversation = {
            "player_input": "",
            "npc_informations": selected_npc_information, 
            "environment_informations": selected_environment_information, 
            "npc_output": "", 
        }
        result.append(conversation)
    # Save to file if output_path is provided
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result


