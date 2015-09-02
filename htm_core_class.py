from spooler import SpatialPooler
import htm__region as tp
from settings import *
from spatialPooler.mappers.sp_square_mapper import SquareMapper
from spatialPooler.sp_region import Region


def to_vector(m):
    output = []
    for i in m:
        for j in i:
            output.append(j)
    return output


def to_matrix(region):
    return [[region.get_columns()[j * region.get_col_h() + i].get_is_active() for i in range(region.get_col_h())] for j
            in range(region.get_col_w())]


class HTMCore:
    def __init__(self):
        self.generator = MakeBubble(temporal_settings.GENERATOR, temporal_settings.REGION_SIZE_N,
                                    temporal_settings.SCALE)

        setting = spatial_settings

        setting.xinput = temporal_settings.REGION_SIZE_N * temporal_settings.SCALE
        setting.yinput = temporal_settings.REGION_SIZE_N * temporal_settings.SCALE
        setting.xdimension = temporal_settings.REGION_SIZE_N
        setting.ydimension = temporal_settings.REGION_SIZE_N

        # TODO написать человеческие имена для переменных
        self.r = Region(setting, SquareMapper)
        self.temporal_pooler = tp.Region(setting.xdimension, setting.cells_per_column)
        # не стоит это сереализовывать
        self.spatial_pooler = SpatialPooler(setting)
        self.input = None
        self.compress_input = None

    def move(self):
        self.input = self.generator.get_data()
        inp = to_vector(self.generator.get_data())

        ov = self.spatial_pooler.update_overlaps(self.r.get_columns(), inp)
        self.spatial_pooler.inhibition_phase(self.r.get_columns(), ov)

        self.compress_input = to_matrix(self.r)

        self.temporal_pooler.step_forward(self.compress_input)
        self.generator.move()

if __name__ == "__main__":
    htm = HTMCore()
    htm.move()
