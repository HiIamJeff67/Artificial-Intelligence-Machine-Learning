import json
import tiktoken

def estimate_token_usage(json_path: str, model_encoding: str = "cl100k_base"):
    """
    Read a JSON file and estimate the token usage for each entry.

    Args:
        json_path: Path to the compressed JSON file
        model_encoding: Tokenizer encoding to use (default: cl100k_base)
    """
    enc = tiktoken.get_encoding(model_encoding)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    token_counts = []
    for item in data:
        json_str = json.dumps(item, separators=(',', ':'), ensure_ascii=False)
        tokens = enc.encode(json_str)
        token_counts.append(len(tokens))

    return token_counts