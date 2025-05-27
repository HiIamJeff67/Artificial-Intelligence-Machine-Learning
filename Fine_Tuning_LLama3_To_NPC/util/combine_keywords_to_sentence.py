import json
import random
import itertools
from typing import Dict, List, Any
from mapping.role_with_request_keywords import (
    role_with_request_nouns,
    role_with_request_verbs,
    role_with_request_adjectives,
    role_with_request_conditions,
)

def combine_keywords_to_sentences(
    max_per_role: int = 1000,
    output_path: str = None,
    sentence_template: str = "{verb} the {adjective} {noun} {condition}"
) -> Dict[str, List[str]]:
    """
    Combine role-related keywords (verbs, adjectives, nouns, conditions) into request sentences for each role.

    Args:
        max_per_role (int): Maximum number of request sentences to generate for each role.
        output_path (str): If specified, the generated result will be saved as a JSON file at this path.
        sentence_template (str): Template for combining keywords into a sentence.

    Returns:
        Dict[str, List[str]]: A dictionary where each key is a role and the value is a list of generated request sentences for that role.
    """
    result = {}
    for role in role_with_request_nouns:
        nouns = role_with_request_nouns[role]
        verbs = role_with_request_verbs[role]
        adjs = role_with_request_adjectives[role]
        conds = role_with_request_conditions[role]
        # Generate all possible combinations
        all_combos = list(itertools.product(verbs, adjs, nouns, conds))
        # Randomly sample max_per_role combinations
        if len(all_combos) > max_per_role:
            combos = random.sample(all_combos, max_per_role)
        else:
            combos = all_combos
        # Generate sentences
        sentences = []
        for (verb, adj, noun, cond) in combos:
            verb = verb[0].upper() + verb[1:]
            s = sentence_template.format(
                verb=verb,
                adjective=adj,
                noun=noun,
                condition=cond
            ).replace("  ", " ").strip()
            sentences.append(s)
        result[role] = sentences
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    return result
