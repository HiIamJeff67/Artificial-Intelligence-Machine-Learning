from dotenv import load_dotenv
from procedures.prepare_dataset import DatasetPreparer

if __name__ == "__main__":
    dataset_preparer = DatasetPreparer(number_of_coworker=1, worker_number=0, dataset_index_start_with=101)
    # dataset_preparer.concatenate_informations_to_predatasets()
    # dataset_preparer.estimate_dataset_token_usage()
    # dataset_preparer.compress_predataset()
    # load_dotenv()
    # conversation = dataset_preparer._generate_conversation_io(index=1, api_key=os.getenv("OPEN_ROUTER_API_KEY"), system_prompt_file_path="prompts/medieval_system_prompt.txt")
    # print(conversation.choices[0])
    # output_path = "data" + f"/conversation_io-{1}.json"
    # with open(output_path, "w", encoding="utf-8") as f:
    #     json.dump(conversation.choices[0].message.content, f, ensure_ascii=False, indent=2)
    # dataset_preparer._prettier_json_file(index=1, input_json_file_path="data/conversation_io-1.json")
    # dataset_preparer.generate_conversation_ios()
    # dataset_preparer.prettier_json_files()
    # dataset_preparer.merge_conversation_and_predataset_to_dataset(output_path="train_dataset.json")
    # data = dataset_preparer.get_dataset_data_with_index(index=0, dataset_path="dataset.json")
    dataset_preparer.convert_to_alpaca(input_path="train_dataset.json", output_path="alpaca_train_dataset.json")
    pass
