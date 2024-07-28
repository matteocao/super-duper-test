""" loading the tasks from the json """

import json
import os
from typing import Tuple, List, Dict
from grid import Grid


class TaskSinglePair:
    """The single pair of input and output grid

    the parameters are:
    :param input: the input grid
    :param output: the output grid
    """

    def __init__(self, input: Grid, output: Grid):
        self.input = input
        self.output = output

    def output_grids(self) -> Tuple[Grid, Grid]:
        return self.input, self.output

    def to_dict(self) -> Dict[str, List[List[int]]]:
        output = {}
        output["input"] = self.input.to_list()
        output["output"] = self.output.to_list()
        return output

    def plot(self, show_input: bool = True, show_output=True):
        if show_input:
            self.input.plot()[0].show()
        if show_output:
            self.output.plot()[0].show()

    def __str__(self) -> str:
        in_grid_str = self.input.plot()[1]
        out_grid_str = self.output.plot()[1]
        return f"Input Grid: {in_grid_str}\n\nOutput Grid: {out_grid_str}"

    def __repr__(self) -> str:
        return str(self)


class TrainTestExample:
    """The object of the training task

    :param pairs: the list of pairs of a input and output for either the
        training or the test
    """

    def __init__(self, pairs: List[TaskSinglePair]):
        self.pairs = pairs

    def __getitem__(self, ind) -> TaskSinglePair:
        return self.pairs[ind]

    def __len__(self) -> int:
        return len(self.pairs)

    def __iter__(self) -> "TrainTestExample":
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self):
            x = self.pairs[self.current_index]
            self.current_index += 1
            return x
        raise StopIteration

    def __str__(self) -> str:
        return f"The train/test example: {self.pairs}"

    def __repr__(self) -> str:
        return str(self)


class FullExample:
    """
    This class models the full example, training and test included

    :param train: the list of pairs for the entire training example
    :param test: the list of pairs for the entire test example
    """

    def __init__(self, train: TrainTestExample, test: TrainTestExample):
        self.train = train
        self.test = test

    def split(self) -> Tuple[TrainTestExample, TrainTestExample]:
        return self.train, self.test

    def to_dict(self) -> Dict[str, List[Dict[str, List[List[int]]]]]:
        output = {}
        output["train"] = [self.train[i].to_dict() for i in range(len(self.train))]
        output["test"] = [self.test[i].to_dict() for i in range(len(self.test))]
        return output

    def __str__(self) -> str:
        return f"Train: {self.train}\nTest: {self.test}\n"

    def __repr__(self) -> str:
        return str(self)


class Sensors:
    """This class loads the grid data from all files

    :param path: the path to the data folder. It is expected to contain the
        ``training`` and the ``evaluation`` folders. Each file in these folders is a full example
    """

    def __init__(self, path: str):
        self.path = path

    def load_tasks_kaggle(
        self, is_kaggle_test_mode: bool, add_evaluation: bool = False
    ) -> Tuple[List[FullExample], List[str]]:
        """
        Function to load the .json files with the tasks of kaggle
        :param is_kaggle_test_mode: a boolean flag to decide which json file to load
        :param add_evaluation: add evaluation file and tasks

        :returns: the return tuple contains
            - training and test tasks separated into a list of :class:`FullExample`
            where each entry is a pair of the train and associated test
            - list of file names
        """
        # Load Tasks
        # Path to tasks
        tasks_path = self.path
        # Initialize list to store file names of tasks
        tasks_file_names: List[str] = []
        tasks: Dict[str, Dict[str, List[Dict[str, List[List[int]]]]]] = {}
        solutions: Dict[str, List[List[List[int]]]] = {}
        # open file
        if is_kaggle_test_mode:
            with open(
                os.path.join(tasks_path, "arc-agi_test_challenges.json"), "r"
            ) as f:
                tasks.update(json.load(f))
        else:
            with open(
                os.path.join(tasks_path, "arc-agi_training_challenges.json"), "r"
            ) as f:
                tasks.update(json.load(f))
            with open(
                os.path.join(tasks_path, "arc-agi_training_solutions.json"), "r"
            ) as f:
                solutions.update(json.load(f))
            if add_evaluation:
                with open(
                    os.path.join(tasks_path, "arc-agi_evaluation_challenges.json"), "r"
                ) as f:
                    tasks.update(json.load(f))
                with open(
                    os.path.join(tasks_path, "arc-agi_evaluation_solutions.json"), "r"
                ) as f:
                    solutions.update(json.load(f))
        full_train_test_examples: List[FullExample] = []
        # build the proper classes
        for task_name, task in tasks.items():
            tasks_file_names.append(task_name)
            train_ex: List[TaskSinglePair] = []
            test_ex: List[TaskSinglePair] = []
            for t in task["train"]:
                t_in = t["input"]
                t_out = t["output"]
                train_ex.append(
                    TaskSinglePair(
                        Grid(t_in),
                        Grid(t_out),
                    )
                )
            for i, t in enumerate(task["test"]):
                t_in = t["input"]
                if is_kaggle_test_mode:
                    t_out = [[0]]
                else:
                    t_out = solutions[task_name][i]
                test_ex.append(
                    TaskSinglePair(
                        Grid(t_in),
                        Grid(t_out),
                    )
                )
            a = TrainTestExample(train_ex)
            b = TrainTestExample(test_ex)
            full_train_test_examples.append(FullExample(a, b))
        return full_train_test_examples, tasks_file_names

    def load_tasks(self) -> Tuple[List[FullExample], List[str]]:
        """
        Function to load all the .json files of the tasks

        :returns: the return tuple contains
            - training and test tasks separated into a list of :class:`FullExample`
            where each entry is a pair of the train and associated test
            - list of file names
        """
        # Load Tasks
        # Path to tasks
        tasks_path = self.path
        # Initialize list to s
        # tore file names of tasks
        tasks_file_names: List[str] = []
        # Initialize lists of lists of dictionaries to store training and test tasks
        # Format of items will be [{'input': array,'output': array},...,
        # {'input': array,'output': array}]
        # Read in tasks and store them in lists initialized above
        full_train_test_examples: List[FullExample] = []
        for file in os.listdir(tasks_path):
            with open(os.path.join(tasks_path, file), "r") as f:
                task = json.load(f)
                tasks_file_names.append(file)
                train_ex: List[TaskSinglePair] = []
                test_ex: List[TaskSinglePair] = []
                for t in task["train"]:
                    t_in = t["input"]
                    t_out = t["output"]
                    train_ex.append(
                        TaskSinglePair(
                            Grid(t_in),
                            Grid(t_out),
                        )
                    )
                for t in task["test"]:
                    t_in = t["input"]
                    t_out = t["output"]
                    test_ex.append(
                        TaskSinglePair(
                            Grid(t_in),
                            Grid(t_out),
                        )
                    )
                a = TrainTestExample(train_ex)
                b = TrainTestExample(test_ex)
            full_train_test_examples.append(FullExample(a, b))
        return full_train_test_examples, tasks_file_names

    def load_single_task(self, task_name: str) -> Tuple[List[FullExample], List[str]]:
        """
        Function to load the .json file of the given task

        :param task: the name of the task to analyse

        :returns: the return tuple contains
            - training and test tasks separated into a list of :class:`FullExample`
            where each entry is a pair of the train and associated test
            - list of file names
            - note that in practice the lists contain a single object
        """
        # path to task
        tasks_path = self.path

        # there is only elemnt in the list, but we use lists for architecture reasons
        tasks_file_names: List[str] = []
        full_train_test_examples: List[FullExample] = []

        # create the FullExample
        file = task_name + ".json"
        with open(os.path.join(tasks_path, file), "r") as f:
            task = json.load(f)
            tasks_file_names.append(file)
            train_ex: List[TaskSinglePair] = []
            test_ex: List[TaskSinglePair] = []
            for t in task["train"]:
                t_in = t["input"]
                t_out = t["output"]
                train_ex.append(
                    TaskSinglePair(
                        Grid(t_in),
                        Grid(t_out),
                    )
                )
            for t in task["test"]:
                t_in = t["input"]
                t_out = t["output"]
                test_ex.append(
                    TaskSinglePair(
                        Grid(t_in),
                        Grid(t_out),
                    )
                )
            a = TrainTestExample(train_ex)
            b = TrainTestExample(test_ex)
        full_train_test_examples.append(FullExample(a, b))
        return full_train_test_examples, tasks_file_names
