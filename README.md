# super-duper-test

This repo is used as a tool to evaluate candidacies to our Research team.

## Description of the challenge

Current AI systems can not generalize to new problems outside their training data, despite extensive training on large datasets. LLMs have brought AI to the mainstream for a large selection of known tasks. However, progress towards Artificial General Intelligence (AGI) has stalled. Improvements in AGI could enable AI systems that think and invent alongside humans.

The Abstraction and Reasoning Corpus for Artificial General Intelligence (ARC-AGI) benchmark measures an AI system's ability to efficiently learn new skills. Humans easily score 85% in ARC, whereas the best AI systems only score 43%. The ARC Prize competition encourages researchers to explore ideas beyond LLMs, which depend heavily on large datasets and struggle with novel problems.

Your work could contribute to new AI problem-solving applicable across industries. Vastly improved AGI will likely reshape human-machine interactions.

## How to participate

In order to participate to the Research team candidate challenge, in a separated repo, prepare your solution code and ship it in a docker. The docker shall be put on [dockerhub](https://hub.docker.com/) - the account on dockerhub for personal use is free - and shall be public. This will make the `docker pull` command work on your image as well. Once you have your docker prepared, you can make a PR to this repo.

### Make your PR

Once your docker is ready, you need to create a PR to this repo. Your PR shall only modify the file [docker_image.txt](https://github.com/matteocao/super-duper-test/blob/main/docker_image.txt) and shall put the name of your docker image containing your solver.

Your docker shall have a final instruction `CMD` that runs your script that solves the tasks: the test files are accessible via a volume binding, putting the test files inside the `/data` folder inside your container. Please make sure that you have an empty `/data` folder in your docker and that your script reaches that folder to analyse the data.

For more details on what are the commands that run your docker, feel free to check the [GitHub action script](https://github.com/matteocao/super-duper-test/blob/main/.github/workflows/main.yml).

### Computational constraints

The total running time of your script on 100 test challenges shall not pass the 4 hours on a standard github action VM: 10% exceptions are tolerated, more running time will be penalised. The maximum running time for the CI is 6h: beyond that time, the CI will timeout and fail.

### Test data

What you will see in the CI of your PR will be a good proxy of the score you will get, but it is not the actual test score: the test set is secret and not available to the public. In case your PR is successful, we will run your docker in a sandbox environment for the actual test score.

## Evaluation

This competition evaluates submissions on the percentage of correct predictions. For each task, you should predict exactly 2 outputs for every test input grid contained in the task. (Tasks can have more than one test input that needs a predicted output). Each task test output has one ground truth. For a given task output, any of the 2 predicted outputs matches the ground truth exactly, you score 1 for that task test output, otherwise 0. The final score is the sum averaged of the highest score per task output divided by the total number of task test outputs.

## Submission File

The submission file for this competition must be a json named `submission.json`.

For each task output in the evaluation set, you should make exactly 2 predictions (`attempt_1`, `attempt_2`). The structure of predictions is shown below. Most tasks only have a single output (a single dictionary enclosed in a list), although some tasks have multiple outputs that must be predicted. These should contain two dictionaries of predictions enclosed in a list, as is shown by the example below. When a task has multiple test outputs that need to be predicted (e.g., task `12997ef3` below), they must be in the same order as the corresponding test inputs.
```json
{"00576224": [{"attempt_1": [[0, 0], [0, 0]], "attempt_2": [[0, 0], [0, 0]]}],
 "009d5c81": [{"attempt_1": [[0, 0], [0, 0]], "attempt_2": [[0, 0], [0, 0]]}],
 "12997ef3": [{"attempt_1": [[0, 0], [0, 0]], "attempt_2": [[0, 0], [0, 0]]},
              {"attempt_1": [[0, 0], [0, 0]], "attempt_2": [[0, 0], [0, 0]]}],
 ...
}
```

## TL;DR

1. Prepare your solver and ship it to [dockerhub](https://hub.docker.com/)
2. Make a PR with your solver by just replacing the name here [docker_image.txt](https://github.com/matteocao/super-duper-test/blob/main/docker_image.txt)
3. The submission.json file shall be structured as described above

Good luck!!

## Citation

Francois Chollet, Mike Knoop, Bryan Landers, Greg Kamradt, Hansueli Jud, Walter Reade, Addison Howard. (2024). ARC Prize 2024. Kaggle. https://kaggle.com/competitions/arc-prize-2024
