# super-duper-test

This repo is used as a tool to evaluate candidacies to our Research team.

## Description of the challenge

Current AI systems can not generalize to new problems outside their training data, despite extensive training on large datasets. LLMs have brought AI to the mainstream for a large selection of known tasks. However, progress towards Artificial General Intelligence (AGI) has stalled. Improvements in AGI could enable AI systems that think and invent alongside humans.

The Abstraction and Reasoning Corpus for Artificial General Intelligence (ARC-AGI) benchmark measures an AI system's ability to efficiently learn new skills. Humans easily score 85% in ARC, whereas the best AI systems only score 43%. The ARC Prize competition encourages researchers to explore ideas beyond LLMs, which depend heavily on large datasets and struggle with novel problems.

Your work could contribute to new AI problem-solving applicable across industries. Vastly improved AGI will likely reshape human-machine interactions.

## The challenge

The challenge data can be found at this repo [/data](https://github.com/matteocao/super-duper-test/tree/main/data) folder. The best way to get familiarised with the data and tasks is to look at [this website](https://arc-editor.lab42.global/playground). Simply put, each one of the tasks consists of a few demo examples explaining the rule to go from input to output - they are needed by the solver to be able to infer the rule to transform the input into the output - and a test task, where one validates whether the rule was inferred correctly.

### How to participate

In order to participate to the Research team candidacy challenge, in a separated repo owned by you, prepare your solution code and ship it in a docker. The docker shall be put on [dockerhub](https://hub.docker.com/) - the account on dockerhub for personal use is free - and shall be public. This will make the `docker pull` command work on your image as well. Once you have your docker prepared, you can make a PR to this repo.

### Make your PR

Once your docker image is ready, you need to create a PR to this repo. Fork this repo and make a PR to the `main` branch. Your PR shall only modify the file [docker_image.txt](https://github.com/matteocao/super-duper-test/blob/main/docker_image.txt) and shall put the name of your docker image containing your solver.

Your docker shall have a final instruction `CMD` that runs your script that solves the tasks: the test files are accessible via a volume binding, putting the test files inside the `/data` folder inside your container. Please make sure that you have an empty `/data` folder in your docker and that your script reaches that folder to analyse the data.

For more details on what is the run command that runs your docker, feel free to check the [GitHub action script](https://github.com/matteocao/super-duper-test/blob/main/.github/workflows/main.yml).

Finally, make sure to write a one-pager description of you PR (directly in the PR). This will also be evaluated. Additioanlly, make sure to write **high-quality code**, with decent docstrings and proper code design: the **code quality** will be analysed manually for the top candidates before they are called for hte final interview.

### Computational constraints

The total running time of your script on 100 test tasks shall not pass the 4 hours on a standard github action VM: 10% exceptions are tolerated, longer running times will be penalised. The maximum running time for the CI is 6h: beyond that time, the CI will timeout and fail.

### Test data

What you will see in the Evaluation step of the CI of your PR will be a good proxy of the score you will get, but it is not the actual test score: the test set is secret and not available to the public. In case your PR is successful, we may run your docker in a sandbox environment for the actual test score. Note that simply copy-pasting the solutions of the [test tasks](https://github.com/matteocao/super-duper-test/blob/main/data/arc-agi_test_challenges.json) taken from the training and evaluation solution files is pointless: this will certainly score 0 in the actual test and does not contain any relevant logic.

### Dummy example

Inside the [/dummy](https://github.com/matteocao/super-duper-test/tree/main/dummy) folder you will find a simple python script `main.py` that generates a random `submission.json` file (that is, of course, unable to generalise to any novel task that may be encountered in the actual test set and has no logic) and a `Dockerfile` that is used to build the corresponding docker. [This PR](https://github.com/matteocao/super-duper-test/pull/1) is just an example for your reference: you can check the CI run and see the score (`= 2` in this example case, when run on the provided test, not the real secret one).

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
