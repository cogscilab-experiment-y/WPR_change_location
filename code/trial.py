from os.path import join
import psychopy.visual
from psychopy import visual

from code.matrix import Matrix


class Trial:
    def __init__(self, win: visual.Window, config: dict, n: int, change: bool, size: [int, int] = (3, 3), group_elements: bool = False):
        self.change = change
        self.matrix_1 = Matrix(n=n,
                               size=size,
                               group_elements=group_elements,
                               stimulus_dist=config["stimulus_dist"],
                               stimulus_size=config["stimulus_size"],
                               stimulus_color=config["stimulus_color"],
                               central_pos=config["stimulus_central_pos"])

        mask_size_x = (size[1] - 1) * config["stimulus_dist"] + config["stimulus_size"] + config["extra_mask_size"]
        mask_size_y = (size[0] - 1) * config["stimulus_dist"] + config["stimulus_size"] + config["extra_mask_size"]
        self.mask = visual.ImageStim(win, image=join('images', 'mask.png'), interpolate=True,
                                     size=(mask_size_x, mask_size_y), pos=config['mask_pos'])

        self.matrix_2 = None
        self.changed_element = None

    @staticmethod
    def copy_matrix(matrix_to_copy: Matrix) -> Matrix:
        new_matrix = Matrix(n=matrix_to_copy.n,
                            size=[matrix_to_copy.size_y, matrix_to_copy.size_x],
                            group_elements=matrix_to_copy.group_elements,
                            stimulus_dist=matrix_to_copy.stimulus_dist,
                            stimulus_size=matrix_to_copy.stimulus_size,
                            stimulus_color=matrix_to_copy.stimulus_color,
                            central_pos=matrix_to_copy.central_pos)
        new_matrix.matrix = matrix_to_copy.matrix[:]
        new_matrix.stimulus_to_draw = matrix_to_copy.stimulus_to_draw[:]
        new_matrix.stimulus_list = matrix_to_copy.stimulus_list[:]
        return new_matrix

    def change_stimulus(self, win: psychopy.visual.Window, new_stimulus: str, stimulus_type: str, border_color: str, border_width: int):
        if self.change:
            self.matrix_2.replace_stimulus(new_stimulus=new_stimulus, stimulus_type=stimulus_type, win=win,
                                           border_color=border_color, border_width=border_width)
            self.changed_element = [elem for elem in self.matrix_2.stimulus_list if elem not in self.matrix_1.stimulus_list][0]
