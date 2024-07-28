from typing import List, Tuple, Type, Dict, ClassVar, Set
import plotly.graph_objects as go  # type: ignore
from plotly.graph_objs._figure import Figure as FigureType  # type: ignore
import numpy as np
import copy
from enum import Enum
from collections import Counter


class SymmetryType(Enum):
    VERTICAL = "x-middle"
    HORIZONTAL = "y-middle"
    CENTRAL = "center"
    MAIN_DIAGONAL = "main diagonal"
    OPPOSITE_DIAGONAL = "opposite diagonal"


class Symbol:
    """Symbol on a grid (number and associated color)

    :param number: the number which represent the symbol
    """

    colors = [
        "#000000",  # Black for 0
        "#0074D9",  # Blue for 1
        "#FF4136",  # Red for 2
        "#2ECC40",  # Green for 3
        "#FFDC00",  # Yellow for 4
        "#AAAAAA",  # Grey for 5
        "#F012BE",  # Fucsha for 6
        "#FF851B",  # Orange for 7
        "#7FDBFF",  # Teal for 8
        "#870C25",  # Brown for 9
        "#FFC0CB",  # Pink for 10, joker symbol for outer boundaries
        "#FFFFFF",  # White for 11, joker symbol for emptiness
    ]

    colors_names = [
        "Black",
        "Blue",
        "Red",
        "Green",
        "Yellow",
        "Grey",
        "Fucsha",
        "Orange",
        "Teal",
        "Brown",
        "Pink",
        "White",
    ]
    num_symbols = len(colors)
    num_off_symbols = 10  # number of official symbols

    background_color = colors.index("#000000")
    undefined_color = colors.index("#FFC0CB")
    white = colors.index("#FFFFFF")
    num_joker_colors = 2

    _instances: ClassVar[Dict[int, "Symbol"]] = dict()
    _number: int  # Explicitly declare _number with a type annotation, for mypy

    def __new__(cls: Type["Symbol"], number: int) -> "Symbol":
        if number in cls._instances:
            return cls._instances[number]

        if 0 <= number < cls.num_symbols:
            instance = super().__new__(cls)
            instance._number = number
            cls._instances[number] = instance
            return instance
        else:
            raise ValueError(
                f"Number must be between 0 and {cls.num_symbols - 1} inclusive."
            )

    @property
    def number(self) -> int:
        return self._number

    def get_color(self) -> str:
        return Symbol.colors[self._number]

    def get_color_name(self) -> str:
        return Symbol.colors_names[self._number]

    def __hash__(self):
        return hash(self.number)

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.number == other.number
        return NotImplemented

    def __str__(self) -> str:
        return str(self.number)

    def __repr__(self) -> str:
        return str(self)

    def __deepcopy__(self, memo):
        # Return the instance itself, not a copy
        return self


class Grid:
    """List of list of symbols, of specified size.

    :param list_int: the grid given as double list of integers
        (then transformed in a double list of :class:`Symbol`)
    :param size: the size of the grid (pair of integers)
    """

    min_pos = 0
    max_pos = 29

    def __init__(self, list_int: List[List[int]], size: Tuple[int, int] | None = None):
        if size is None:
            size = (len(list_int), len(list_int[0]))
        # check that the list is indeed a grid of good size
        assert len(list_int) == size[0]
        for sub_list in list_int:
            assert len(sub_list) == size[1]

        self.size = size
        # make the grid into symbols
        self.symbols: List[List[Symbol]] = []
        for i in range(self.size[0]):
            sub_list_sym = []
            for j in range(self.size[1]):
                sub_list_sym.append(Symbol(list_int[i][j]))
            self.symbols.append(sub_list_sym)
        self.current_index = 0

    def __getitem__(self, pos: Tuple[int, int]) -> Symbol:
        return self.symbols[pos[0]][pos[1]]

    def __setitem__(self, pos: Tuple[int, int], sym: Symbol):
        self.symbols[pos[0]][pos[1]] = sym

    def get_symbol(self, pos: Tuple[int, int]) -> Symbol:
        # assert (0 <= pos[0] < self.size[0]) and (0 <= pos[1] < self.size[1])
        try:
            return self.symbols[pos[0]][pos[1]]
        except IndexError:
            print("Position to retrieve symbol out of bounds")
            return Symbol(0)

    def get_color_set(self, without_white: bool = False) -> Set[int]:
        """The function returns the set of colors in the grid, with the exception of the White color (if requested)

        :param without_white: whether white should be in the set or not, defaults to False
        :returns: the set of integers, corresponding to the colors
        """
        symbol_set = set()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if not self.symbols[i][j] == Symbol(11) or without_white == False:
                    symbol_set.add(self.symbols[i][j].number)
        return symbol_set

    def get_most_used_symbol(self) -> Tuple[int, float]:
        """The function computes and returns the most used symbol and its percentage of usage in the grid.

        :returns: the most used symbol (if it exists, it is likely the background color)
        """

        symbol_counter = Counter(
            symbol.number for row in self.symbols for symbol in row
        )

        most_common_symbol, frequency = symbol_counter.most_common(1)[0]

        return most_common_symbol, frequency

    def update(self, pos: Tuple[int, int], new_symbol: Symbol):
        # assert (0 <= pos[0] < self.size[0]) and (0 <= pos[1] < self.size[1])
        self.symbols[pos[0]][pos[1]] = new_symbol

    def to_list(self) -> List[List[int]]:
        """convert grid to List[List[int]]"""
        ans: List[List[int]] = []
        for i in range(self.size[0]):
            sub_list: List[int] = []
            for j in range(self.size[1]):
                sub_list.append(int(self.symbols[i][j].number))
            ans.append(sub_list)
        return ans

    def plot(self) -> Tuple[FigureType, str]:
        fig = go.Figure()

        colors = Symbol.colors

        dcolorscale = [[i / (len(colors) - 1), c] for i, c in enumerate(colors)]
        rev_lst = self.to_list()
        rev_lst.reverse()
        matrix = np.array(rev_lst)
        # Create heatmap for each matrix
        fig.add_trace(
            go.Heatmap(
                z=matrix,
                colorscale=dcolorscale,
                zmin=0,
                zmax=len(colors) - 1,
                xgap=3,
                ygap=3,
                colorbar=dict(
                    thickness=25,
                    tickvals=[i for i in range(len(colors))],
                    ticktext=colors,
                ),
            )
        )
        fig.update_layout(
            xaxis=dict(
                showgrid=True,
                zeroline=False,
                showline=False,
                showticklabels=True,
            ),
            yaxis=dict(
                showgrid=True,
                zeroline=False,
                showline=False,
                showticklabels=True,
            ),
        )
        fig.update_layout(
            width=max(matrix.shape[1] * 30 + 100, 300),  # Number of columns for width
            height=max(matrix.shape[0] * 30 + 100, 300),  # Number of rows for height
        )

        return fig, str(np.array(self.to_list()))

    def __str__(self) -> str:
        return self.plot()[1]

    """
    def __getitem__(self, ind: int) -> List[Symbol]:
        return self.symbols[ind]
    """

    def __len__(self) -> int:
        return len(self.symbols)

    def __iter__(self) -> "Grid":
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self):
            x = self.symbols[self.current_index]
            self.current_index += 1
            return x
        raise StopIteration

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Grid):
            return self.symbols == other.symbols
        return False

    def __sub__(self, other_grid: "Grid") -> "Grid":
        """The function creates the difference betweeen two grids. It returns a grid of the same size as of self.
        When the symbols are equal in the two grids, the pixel is replaced with a white pixel.

        :param other_grid: The other grid for the difference
        :returns: the difference grid
        """
        difference_grid = copy.deepcopy(self)
        for i in range(difference_grid.size[0]):
            for j in range(difference_grid.size[1]):
                if i < other_grid.size[0] and j < other_grid.size[1]:
                    if other_grid.symbols[i][j] == self.symbols[i][j]:
                        difference_grid.update(pos=(i, j), new_symbol=Symbol(11))
                else:
                    difference_grid.update(pos=(i, j), new_symbol=Symbol(11))
        return difference_grid

    def similarity_score(self, grid: "Grid") -> float:
        """The function computes the percentage of equal pixels between self and another grid.

        :param grid: the other grid
        :returns: the percentage (between 0 and 1). If the grids do not have the same sizes, 0 is returned.
        """
        if self.size != grid.size:
            return 0
        else:
            same_symbols = 0
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    if self.symbols[i][j] == grid.symbols[i][j]:
                        same_symbols = same_symbols + 1
            return same_symbols / (self.size[0] * self.size[1])

    def overlapping_pixels(self, grid: "Grid") -> List[Tuple[int, int]]:
        """The function returns the list of pixels that are equal between self and another grid

        :param grid: the other grid
        :returns: the list of pixels that are equal
        """
        difference_grid = self - grid
        list_of_overlapping_pixels: List[Tuple[int, int]] = []
        for i in range(difference_grid.size[0]):
            for j in range(difference_grid.size[1]):
                if difference_grid.symbols[i][j].number == 11:
                    list_of_overlapping_pixels.append((i, j))
        return list_of_overlapping_pixels

    def get_contiguous_coordinate_sets(self) -> List[List[Tuple]]:
        """The function partitions the grid into a list of lists of contiguous pixels of the same color.

        :returns: the list of list of pixels
        """
        visited = set()
        coordinate_sets: List[List[Tuple]] = []
        grid: List[List[Symbol]] = self.symbols

        def dfs(i, j, color):
            """the function is used to search for the contiguous pixels of the same color.

            :param i: row-index
            :param j: col-index
            :param color: the color of the partition
            """
            if (
                (i, j) in visited
                or i < 0
                or i >= len(grid)
                or j < 0
                or j >= len(grid[0])
                or grid[i][j] != color
            ):
                return
            visited.add((i, j))
            coordinate_sets[-1].append((i, j))
            dfs(i + 1, j, color)  # Down
            dfs(i - 1, j, color)  # Up
            dfs(i, j + 1, color)  # Right
            dfs(i, j - 1, color)  # Left
            dfs(i + 1, j + 1, color)  # Down-Right
            dfs(i + 1, j - 1, color)  # Down-Left
            dfs(i - 1, j + 1, color)  # Up-Right
            dfs(i - 1, j - 1, color)  # Up-Left

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if (i, j) not in visited:
                    coordinate_sets.append([])
                    dfs(i, j, grid[i][j])

        return coordinate_sets

    def is_symmetric(
        self, symmetry_type: SymmetryType = SymmetryType.CENTRAL
    ) -> List[int]:
        """
        The function evaluates whether the grid satisfies a given symmetry. There are 5 types of symmetry
        considered: 4 axial symmetry, and 1 point symmetry. Horizontal and Vertical symmetry are evaluated
        with respect to a general axis, i.e., offsets with respect to the mid-axis are also considered.
        :param symmetry_type: the type of symmetry
        :returns: the list of axis that satisfy the symmetry condition. Except for vertical and horizontal
                  symmetry, only the default option is considered, hence either [0] or [] is returned.
        """

        symmetric_axis: List[int] = []
        rows = self.size[0]
        cols = self.size[1]
        if (
            symmetry_type == SymmetryType.MAIN_DIAGONAL
            or symmetry_type == SymmetryType.OPPOSITE_DIAGONAL
        ):
            if not (rows == cols):
                return symmetric_axis
        if symmetry_type == SymmetryType.HORIZONTAL:
            max_offset = rows // 2 - 1
        elif symmetry_type == SymmetryType.VERTICAL:
            max_offset = cols // 2 - 1
        elif (
            symmetry_type == SymmetryType.MAIN_DIAGONAL
            or symmetry_type == SymmetryType.OPPOSITE_DIAGONAL
            or symmetric_axis == SymmetryType.CENTRAL
        ):
            max_offset = (
                cols // 2 - 1
            )  # Assuming number of rows is equal to the number of cols
        else:
            max_offset = 0

        offsets = list(range(-max_offset, max_offset + 1))

        def symmetric_point(
            pos: Tuple[int, int],
            rows: int,
            cols: int,
            offset: int,
            symmetry_type: SymmetryType,
        ) -> Tuple[int, int] | None:
            """The function returns the symmetric point in the grid, according to the symmetry type and the offset.

            :param pos: the position of the first pixel
            :param rows: the number of rows of the grid
            :param cols: the number of columns of the grid
            :param offset: a possible offset with respect to the mid-axis symmetry
            :param symmetry_type: the type of symmetry
            :returns: the position in the grid of the symmetric point
            """
            if symmetry_type == SymmetryType.MAIN_DIAGONAL:
                x_sym = pos[1] + 2 * offset
                y_sym = pos[0] + 2 * offset
            elif symmetry_type == SymmetryType.OPPOSITE_DIAGONAL:
                x_sym = rows - pos[1] - 1 + 2 * offset
                y_sym = cols - pos[0] - 1 + 2 * offset
            elif symmetry_type == SymmetryType.VERTICAL:
                x_sym = pos[0]
                y_sym = cols - pos[1] - 1 + 2 * offset
            elif symmetry_type == SymmetryType.HORIZONTAL:
                x_sym = rows - pos[0] - 1 + 2 * offset
                y_sym = pos[1]
            elif symmetry_type == SymmetryType.CENTRAL:
                x_sym = rows - pos[0] - 1 + 2 * offset
                y_sym = cols - pos[1] - 1 + 2 * offset
            else:
                print("not implementd")
                return None
            if 0 <= x_sym and x_sym < rows and 0 <= y_sym and y_sym < cols:
                return (x_sym, y_sym)
            else:
                return None

        for offset in offsets:
            symmetric = True
            color_set = set()
            for i in range(rows):
                for j in range(cols):
                    sym_point: Tuple[int, int] | None = symmetric_point(
                        (i, j), rows, cols, offset, symmetry_type
                    )
                    if sym_point is not None:
                        if not (
                            self.symbols[i][j]
                            == self.symbols[sym_point[0]][sym_point[1]]
                        ):
                            symmetric = False
                        else:
                            color_set.add(self.symbols[i][j])
            if (
                symmetric and len(color_set) > 1
            ):  # The second check is to exclude the case when the symmetry is trivial (just uniform colors)
                symmetric_axis.append(offset)
        return symmetric_axis

    def get_subgrid(self, start_row, start_col, height, width) -> "Grid":
        """Extracts a rectangular subgrid from the given grid starting at (start_row, start_col) with the specified height and width.
        :param start_row: index of the starting row
        :param start_col: index of the starting column
        :param height: height of the 2d subgrid
        :param width: width of the 2d subgrid
        :returns: the required subgrid
        """

        subgrid_list: List[List[int]] = []
        for i in range(start_row, start_row + height):
            row: List[int] = []
            for j in range(start_col, start_col + width):
                row.append(self.symbols[i][j].number)
            subgrid_list.append(row)
        return Grid(subgrid_list)

    def find_all_subgrids(
        self, subgrid_size: Tuple[int, int]
    ) -> Tuple[List["Grid"], List[Tuple[int, int]]]:
        """
        Finds all subgrids of the specified size within the given grid
        :param subgrid_size: the heigth (number of rows) and width (number of columns) of the subgrid
        :returns: A tuple containing, for each pair, the subgrid and the index of the top-left pixel in the original grid.
        """
        num_rows = self.size[0]
        num_cols = self.size[1]
        subgrids: List[Grid] = []
        top_left_corners: List[Tuple[int, int]] = []
        for start_row in range(num_rows - subgrid_size[0] + 1):
            for start_col in range(num_cols - subgrid_size[1] + 1):
                subgrid = self.get_subgrid(
                    start_row, start_col, subgrid_size[0], subgrid_size[1]
                )
                subgrids.append(subgrid)
                top_left_corners.append((start_row, start_col))
        return subgrids, top_left_corners
