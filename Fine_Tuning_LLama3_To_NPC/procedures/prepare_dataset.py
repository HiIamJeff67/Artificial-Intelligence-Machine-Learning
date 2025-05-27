import re
import os
import json
from typing import *
from logs.loggers import Logger
from util.txt_to_list import txt_to_py_list
from util.combine_keywords_to_sentence import combine_keywords_to_sentences
from util.generate_npcs import generate_npcs
from util.generate_environments import generate_environments
from util.concatenate_infomations_to_dataset import concatenate_informations_to_dataset
from util.estimate_token_usage import estimate_token_usage
from util.compress import compress_json_file
from api.ask_model_api import ask_api_model_with_key
from constants.amount import Total_Number_Of_Conversations, Generate_Conversations_Batch_Size
from constants.available_models import AvailableModels
from constants.keys import OPEN_ROUTER_API_KEYS

class DatasetPreparer:
    def __init__(
        self, 
        number_of_coworker: int = 2, 
        worker_number: int = 0, 
        dataset_index_start_with: int = 1, 
    ):
        self.logger = Logger(
            title="Preparing Dataset", 
            number_of_progress_bars=10, # reserve 10 progress bars
        )
        self.temporary_output_path = "data/"
        self.plain_txt_files_path = "enums/@generated/"
        self.enum_python_files_path = "enums/"
        self.datasets_path = "datasets/"
        self.prompts_path = "prompts/"
        
        self.max_number_of_iterations = (Total_Number_Of_Conversations // Generate_Conversations_Batch_Size)
        self.iteration_count = self.max_number_of_iterations // number_of_coworker
        self.number_of_conversation_per_size = Generate_Conversations_Batch_Size
        
        self.number_of_coworker = number_of_coworker
        self.worker_number = worker_number
        
        self.dataset_index = dataset_index_start_with
    
    def convert_generated_txt_to_list_file(self, attribute_names: List[str] = []) -> None:
        if len(attribute_names) == 0:
            self.logger.log_error("Please provide at least one attribute name as the parameter of attribute_names", raise_exception=True)
        
        for attribute_name in attribute_names:
            self.logger.log_progress(
                progress_bar_index=0, 
                description=f"Generate enum of {attribute_name}", 
                total=len(attribute_names), 
            )
            txt_to_py_list(f"{self.plain_txt_files_path}{attribute_name}.txt", f"{self.enum_python_files_path}{attribute_name}.py", f"All{attribute_name[0].upper() + attribute_name[1:]}")
            
    def combine_requests_from_keywords_to_sentences(self, max_per_role: int = 100) -> None:
        if max_per_role < 0:
            self.logger.log_error("Please provide a positive parameter of max_per_role", raise_exception=True)
        combine_keywords_to_sentences(max_per_role, f"{self.temporary_output_path}/role_with_requests.json")
        
    def generate_informations(self, npc_information_count: int = 100, environment_information_count: int = 100) -> None:
        if npc_information_count < 0:
            self.logger.log_error("Please provide a positive parameter of npc_information_count", raise_exception=True)
        if environment_information_count < 0:
            self.logger.log_error("Please provide a positive parameter of environment_information_count", raise_exception=True)
        
        generate_npcs(npc_information_count, f"{self.temporary_output_path}/npc_informations.json") # using the default value of role_with_request_json_path and config
        generate_environments(environment_information_count, f"{self.temporary_output_path}/environment_information.json")
    
    def concatenate_informations_to_predatasets(self) -> None:
        self.logger.log_info(f"Starting generating {self.iteration_count} iterations of dataset with each containing {self.number_of_conversation_per_size} conversations")
        for i in range(self.dataset_index, self.dataset_index + self.iteration_count):
            self.logger.log_progress(
                progress_bar_index=1, 
                description=f"Concatenating informations as {i}-th predataset", 
                total=self.iteration_count, 
                unit="json file", 
                leave_in_console=True, 
                ncols=100
            )
            concatenate_informations_to_dataset(
                count=self.number_of_conversation_per_size, 
                output_path=f"{self.datasets_path}/predataset-{i}.json"
            )
        self.logger.clear_progress(progress_bar_index=1)
        
    def estimate_dataset_token_usage(self) -> None:
        all_token_counts = []
        for i in range(self.dataset_index, self.dataset_index + self.iteration_count):
            self.logger.log_progress(
                progress_bar_index=2, 
                description=f"Estimating informations in {i}-th predataset", 
                total=self.iteration_count, 
                unit="json file", 
                leave_in_console=True, 
                ncols=100
            )
            all_token_counts.append(estimate_token_usage(f"{self.datasets_path}/predataset-{i}.json"))
        
        max_total_token_counts = 0
        for token_counts in all_token_counts:
            self.logger.log_seperator(length=50)
            self.logger.log_info(f"🔢 Average tokens per entry: {sum(token_counts) / len(token_counts):.2f}")
            self.logger.log_info(f"📈 Max tokens in an entry: {max(token_counts)}")
            self.logger.log_info(f"📉 Min tokens in an entry: {min(token_counts)}")
            self.logger.log_info(f"🧮 Total tokens: {sum(token_counts)}")
            max_total_token_counts = max(max_total_token_counts, sum(token_counts))
            
        self.logger.clear_progress(progress_bar_index=2)
        self.logger.log_info(f"The maximum total tokens in all the generated predatasets are: {max_total_token_counts}")
        
    def compress_predataset(self) -> None:
        for i in range(self.dataset_index, self.dataset_index + self.iteration_count):
            self.logger.log_progress(
                progress_bar_index=3, 
                description=f"Compressing informations in {i}-th predataset", 
                total=self.iteration_count, 
                unit="json file", 
                leave_in_console=True, 
                ncols=100
            )
            compress_json_file(
                input_path=f"{self.datasets_path}/predataset-{i}.json", 
                output_path=f"{self.prompts_path}/conversation_user_prompt-{i}.json", 
            )
        self.logger.clear_progress(progress_bar_index=3)
    
    def _generate_conversation_io(
        self, 
        index: int, 
        api_key: str = None, 
        system_prompt_file_path: str = None, 
        model: AvailableModels = "meta-llama/llama-3.3-70b-instruct:free", 
    ) -> None:
        if not api_key:
            raise Exception("Please provide a api key as the parameter of api_key")
        if system_prompt_file_path is None:
            self.logger.log_error("Please provide the system prompt file path as the parameter of system_prompt_file_path")

        if not os.path.exists(system_prompt_file_path):
            self.logger.log_error(f"System prompt file not found: {system_prompt_file_path}", raise_exception=True)
        user_prompt_path = self.prompts_path + f"/conversation_user_prompt-{index}.json"
        if not os.path.exists(user_prompt_path):
            self.logger.log_error(f"User prompt file not found: {user_prompt_path}", raise_exception=True)
        
        with open(system_prompt_file_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
        
        with open(user_prompt_path, "r", encoding="utf-8") as f:
            user_prompt_obj = json.load(f)
            user_prompt = json.dumps(user_prompt_obj, ensure_ascii=False)
        
        return ask_api_model_with_key(
            api_key=api_key,
            system_prompt=system_prompt, 
            user_prompt=user_prompt, 
            model=model, 
        )
        
    def generate_conversation_ios(self, model: AvailableModels = "meta-llama/llama-3.3-70b-instruct:free") -> None:
        try:
            system_prompt_file_path: str = self.prompts_path + "/medieval_system_prompt.txt"
            _iteration_count = self.iteration_count // len(OPEN_ROUTER_API_KEYS)
            index = self.dataset_index
            
            for key in OPEN_ROUTER_API_KEYS:
                for _ in range(_iteration_count):
                    self.logger.log_progress(
                        progress_bar_index=9, 
                        description="Generating player inputs and NPC outputs", 
                        total=self.iteration_count, 
                        unit="conversation", 
                        leave_in_console=True, 
                        ncols=100
                    )
                    
                    conversation = self._generate_conversation_io(
                        index=index,
                        api_key=key,
                        system_prompt_file_path=system_prompt_file_path, 
                        model=model
                    )
                    
                    output_path = self.temporary_output_path + f"/conversation_io-{index}.json"
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(conversation.choices[0].message.content, f, ensure_ascii=False, indent=2)
                    
                    index += 1
                    
            self.logger.clear_progress(progress_bar_index=9)
            
        except Exception as error:
            raise Exception(error)
    
    def _prettier_json_file(
        self,  
        input_json_file_path: str = None, 
        output_json_file_path: str = None, 
    ) -> None:
        if input_json_file_path is None:
            raise Exception("Please provide a json file path as the input")
        if output_json_file_path is None:
            output_json_file_path = input_json_file_path

        with open(input_json_file_path, "r", encoding="utf-8") as f:
            raw = f.read().strip()
            if raw.startswith('"'):
                try:
                    first = json.loads(raw)
                    data = json.loads(first)
                except Exception as e:
                    self.logger.log_error(f"Parsing JSON Failed: {e}", raise_exception=True)
            else:
                data = json.loads(raw)

        pretty = json.dumps(data, ensure_ascii=False, indent=2)
        with open(output_json_file_path, "w", encoding="utf-8") as f:
            f.write(pretty)
        
        return pretty
    
    def prettier_json_files(self) -> None:  
        for i in range(self.dataset_index, self.dataset_index + self.iteration_count):
            self.logger.log_progress(
                progress_bar_index=4, 
                description="Generating player inputs and NPC outputs", 
                total=self.iteration_count, 
                unit="conversation", 
                leave_in_console=True, 
                ncols=100
            )
            
            self._prettier_json_file(
                input_json_file_path=f"{self.temporary_output_path}/conversation_io-{i}.json"
            )
        
        self.logger.clear_progress(progress_bar_index=4)
        
    def merge_conversation_and_predataset_to_dataset(self, output_path="dataset.json"):
        merged = []
        for i in range(self.dataset_index, min(self.max_number_of_iterations, self.dataset_index + self.iteration_count)):
            with open(f"{self.temporary_output_path}/conversation_io-{i}.json", "r", encoding="utf-8") as f:
                conversations = json.load(f)[:Generate_Conversations_Batch_Size]

            with open(f"{self.datasets_path}/predataset-{i}.json", "r", encoding="utf-8") as f:
                predataset = json.load(f)[:Generate_Conversations_Batch_Size]

            # merge player_input and npc_output together
            for conv, pred in zip(conversations, predataset):
                npc_output = conv.get("npc_output", "")
                requests = pred.get("npc_informations", {}).get("requests", [])

                def replace_request(match):
                    idx = int(match.group(1)) - 1
                    if 0 <= idx < len(requests):
                        return requests[idx]
                    return ""

                npc_output = re.sub(r"\|r(\d+)\|", replace_request, npc_output)

                pred["player_input"] = conv.get("player_input", "")
                pred["npc_output"] = npc_output
                merged.append(pred)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)

    def get_dataset_data_with_index(self, index: int, dataset_path="dataset.json"):
        with open(dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if 0 <= index < len(data):
            item = data[index]
            
            # compress
            if "npc_informations" in item:
                compressed = json.dumps(item["npc_informations"], ensure_ascii=False, separators=(',', ':'))
                item["npc_informations"] = compressed.replace('"', "'")
            if "environment_informations" in item:
                compressed = json.dumps(item["environment_informations"], ensure_ascii=False, separators=(',', ':'))
                item["environment_informations"] = compressed.replace('"', "'")
            return item
        else:
            raise IndexError(f"Index {index} out of range (dataset size: {len(data)})")
        
    def convert_to_alpaca(self, input_path="dataset.json", output_path="alpaca_dataset.json"):
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        alpaca_data = []
        for item in data:
            # 合併 informations
            npc_info = item.get("npc_informations", {})
            env_info = item.get("environment_informations", {})
            # 轉成單一 JSON 字串
            input_str = json.dumps({
                "npc_informations": npc_info,
                "environment_informations": env_info
            }, ensure_ascii=False, separators=(',', ':'))
            alpaca_item = {
                "instruction": item.get("player_input", ""),
                "input": input_str,
                "output": item.get("npc_output", "")
            }
            alpaca_data.append(alpaca_item)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(alpaca_data, f, ensure_ascii=False, indent=2)