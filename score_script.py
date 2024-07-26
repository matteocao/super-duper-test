import json
import os
from sensors import Sensors, FullExample

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the JSON file
file_name = "submission.json"
directory_path = "data"


def find_file(directory_path, file_name):
    # Create the full path to the file within the current working directory
    full_path = os.path.join(os.getcwd(), directory_path, file_name)
    return os.path.isfile(full_path)

# test find_file
file_name_example = "1f876c06" + ".json"
print(file_name_example)
print(find_file(directory_path=directory_path, file_name=file_name_example))

# TODO: convert kaggle format to single filess

# start sensors
sensor_train = Sensors(os.path.join("data", "training"))
sensor_eval = Sensors(os.path.join("data", "evaluation"))
sensor_test = Sensors(os.path.join("test_data", "evaluation"))
sensors = [sensor_train, sensor_eval, sensor_test]


def score(file_name):
    file = open(file_name, "r")
    data = json.load(file)
    attempted, score = 0, 0
    for task_name in data:
        file_name = task_name + ".json"
        for i, directory_path in enumerate(directories):
            if find_file(directory_path, file_name):
                attempted += 1
                local_score = 0
                examples, _ = sensors[i].load_single_task(task_name)
                full_example: FullExample = examples[0]
                for j, pair in enumerate(full_example.test):
                    grid_expected = pair.output.to_list()
                    if (data[task_name][j]["attempt_1"] == grid_expected) or (
                        data[task_name][j]["attempt_2"] == grid_expected
                    ):
                        local_score += 1
                score += local_score / len(full_example.test)
    return attempted, score, score / attempted


print(score(file_name))
