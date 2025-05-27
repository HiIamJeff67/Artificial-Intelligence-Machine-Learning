import json
import random
from typing import *
from enums.weather import AllWeathers
from enums.time import AllTimes

def generate_environment() -> Dict[str, str]:
    """
    Generate a random environment with weather and time.

    Returns:
        Dict[str, str]: A dictionary with keys 'weather' and 'time', each randomly selected from AllWeathers and AllTimes.
    """
    result = {
        "weather": random.choice(AllWeathers), 
        "time": random.choice(AllTimes)
    }
    return result

def generate_environments(
    count: int = 500, 
    output_path: str = None, 
) -> List[Dict[str, str]]:
    """
    Generate a list of random environments and optionally save to a JSON file.

    Args:
        count (int): Number of environments to generate.
        output_path (str): File path to save the generated environments as JSON.

    Returns:
        List[Dict[str, str]]: A list of environment dictionaries.
    Raises:
        Exception: If output_path is not provided.
    """
    if not output_path:
        raise Exception("Please provide a output file as a parameter of output_file")
    
    result = []
    # Generate environments
    for i in range(count):
        result.append(generate_environment())
    # Save to file if output_path is provided
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    return result