import json
import random
from typing import *
from dataclasses import dataclass
from faker import Faker
from enums.role import AllRoles
from enums.mood import AllMoods
from enums.interset import AllInterests
from enums.playerRelationship import AllPlayerRelationships
from enums.gender import AllGenders
from enums.personality import AllPersonalities
from constants.unique_roles import unique_roles
from constants.amount import (
    Min_Number_Of_Moods, Max_Number_Of_Moods, 
    Min_Number_Of_Interests, Max_Number_Of_Interests, 
    Min_Number_Of_Personalities, Max_Number_Of_Personalities, 
    Min_Number_Of_Requests, Max_Number_Of_Requests, 
)

@dataclass
class NPCLimitConfig:
    mood_range: Tuple[int, int]
    interest_range: Tuple[int, int]
    personalitiy_range: Tuple[int, int]
    request_range: Tuple[int, int]
    
DefaultNPCLimitConfig = NPCLimitConfig(
    mood_range=(Min_Number_Of_Moods, Max_Number_Of_Moods),
    interest_range=(Min_Number_Of_Interests, Max_Number_Of_Interests),
    personalitiy_range=(Min_Number_Of_Personalities, Max_Number_Of_Personalities),
    request_range=(Min_Number_Of_Requests, Max_Number_Of_Requests)
)

def generate_npc(
    index: int, 
    faker: Faker, 
    role_with_request_json_path: str,
    config: NPCLimitConfig
) -> Dict[str, Any]:
    selected_role = random.choice(AllRoles)
    
    result = {
        "index": str(index),
        "name": faker.name(), 
        "role": selected_role, 
        "moods": random.sample(AllMoods, random.randint(config.mood_range[0], config.mood_range[1])), 
        "interests": random.sample(AllInterests, random.randint(config.interest_range[0], config.interest_range[1])), 
        "playerRelationship": random.choice(AllPlayerRelationships), 
        "gender": random.choice(AllGenders), 
        "personalities": random.sample(AllPersonalities, random.randint(config.personalitiy_range[0], config.personalitiy_range[1])), 
        "requests": []
    }
    
    with open(role_with_request_json_path, 'r') as f:
        data = json.load(f)
        if selected_role in data:
            request_list = data[selected_role]
            result["requests"] = random.sample(request_list, random.randint(config.request_range[0], config.request_range[1]))
        else:
            raise Exception("No any data in the given role_with_request_json_path")
    
    return result

def generate_npcs(
    count: int = 100,
    output_path: str = None,
    role_with_request_json_path: str = "data/role_with_requests.json",
    config: NPCLimitConfig = DefaultNPCLimitConfig
) -> List[Dict[str, any]]:
    """
    Generate a list of NPCs with random attributes and requests, and optionally save to a JSON file.

    Args:
        count (int): Number of NPCs to generate.
        output_path (str): File path to save the generated NPCs as JSON.
        role_with_request_json_path (str): Path to the role-to-requests mapping JSON.
        config (dict): Optional configuration for generation.

    Returns:
        List[dict]: A list of generated NPC dictionaries.
    """
    if not output_path:
        raise Exception("Please provide a output file as a parameter of output_file")
    
    faker = Faker()
    result = []
    used_roles = set()
    
    for i in range(1, count + 1):
        generated_npc = None
        # retry if the role of generated npc is used role
        while generated_npc == None or generated_npc["role"] in used_roles:
            generated_npc = generate_npc(
                index=i, 
                faker=faker, 
                role_with_request_json_path=role_with_request_json_path, 
                config=config
            )
        if generated_npc["role"] in unique_roles:
            used_roles.add(generated_npc["role"])
        
        result.append(generated_npc)
        
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result
