import json

test_path = "/data/arc-agi_test_challenges.json"

# build dummy dictionary of solutions
def build_dummy_sub_file(test_path):
    sub_dict = {}
    with open(test_path,'r') as f:
        tasks = json.load(f)
    tasks_name, tasks_file = list(tasks.keys()), list(tasks.values())

    for n in range(len(tasks_name)):
        task = tasks_file[n]
        t = tasks_name[n]

        sub_dict[t] = []
        for i in range(len(task['test'])): 
            sub_dict[t].append({
                "attempt_1": [
                    [0, 0],
                    [0, 0]
                ],
                "attempt_2": [
                    [0, 0],
                    [0, 0]
                ]
                })

    with open('submission.json', 'w') as file:
        json.dump(sub_dict, file, indent=4)
    return sub_dict
