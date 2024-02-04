import csv
import pandas as pd
import json


def process_csv_to_json(input_file, output_file):

    f = open(input_file, 'r', encoding='utf-8')
    reader = csv.reader(f, delimiter=',')

    # Initialize the output data structure
    output_data = []

    conversation = {
        "system": "你是一个对名人生平研究颇深的学者。你总是可以根据提问给出准确且详细的答案",
        "input": "请介绍一下你自己",
        "output": "您好，我是一个对名人生平略有研究的学者小光，有想要了解的名人都可以问我哦~（示例：请介绍一下李白的生平）"
    }

    for _ in range(5000):
        output_data.append({"conversation": [conversation]})

    for row in reader:
        system_value = "你是一个对名人生平研究颇深的学者。你总是可以根据提问给出准确且详细的答案"

        # Create the conversation dictionary
        conversation = {
            "system": system_value,
            "input": row[0],
            "output": row[1]
        }

        # Append the conversation to the output data
        for _ in range(1000):
            output_data.append({"conversation": [conversation]})

    # Write the output data to a JSON file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(output_data, json_file, indent=4)

    print(f"Conversion complete. Output written to {output_file}")


# Replace 'poets.csv' and 'poets.json' with your actual input and output file names
process_csv_to_json('life_of_poets.csv', 'dataset.json')