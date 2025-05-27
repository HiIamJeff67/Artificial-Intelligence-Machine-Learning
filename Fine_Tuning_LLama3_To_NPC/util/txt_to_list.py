from typing import *

def txt_to_py_list(
    txt_path: str, 
    py_path: str, 
    list_name: str
) -> None:
    lines = []
    with open(txt_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            if "#" in line:
                value, comment = line.split("#", 1)
                value = value.strip()
                comment = "#" + comment.strip()
                if value:
                    lines.append(f'    "{value}", {comment}')
            else:
                value = line.strip()
                if value:
                    lines.append(f'    "{value}",')
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(f"{list_name} = [\n")
        for l in lines:
            f.write(l + "\n")
        f.write("]\n")
