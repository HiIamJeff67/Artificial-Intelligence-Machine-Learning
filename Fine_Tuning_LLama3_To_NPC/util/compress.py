import json

def compress_json_file(
    input_path: str = None, 
    output_path: str = None,
) -> None:
    """
    Compress json file to one line form
    
    Args:
        input_path: original JSON file path
        output_path: compressed JSON file path
    """
    if input_path is None or output_path is None:
        raise Exception("Please provide an input path and a output path as the parameters of input_path and output_path")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise TypeError("TypeError：The data inside json file should be list of conversations")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'), ensure_ascii=False)

    print(f"Compressing json file done at {output_path}")