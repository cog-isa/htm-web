from spooler import SpatialPooler
from sp_region import Region
import htm__region as tp
from settings import *
from spatialPooler.mappers.sp_square_mapper import SquareMapper


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
    def __init__(self, inset, spset, tpset):
        self.generator = MakeBubble(inset.GENERATOR, tpset.REGION_SIZE_N,
                                    inset.SCALE)

        spset.xinput = tpset.REGION_SIZE_N * inset.SCALE
        spset.yinput = tpset.REGION_SIZE_N * inset.SCALE
        spset.xdimension = tpset.REGION_SIZE_N
        spset.ydimension = tpset.REGION_SIZE_N

        # TODO все-таки нужно найти где этот радиус задается в настройках и как передается...
        # может быть проблема в синхронизации htm-core
        spset.potential_radius = 1
        self.spatial_region = Region(spset, SquareMapper)
        self.temporal_pooler = tp.Region(spset.xdimension, temporal_settings.COLUMN_SIZE)
        # не стоит это сереализовывать
        self.spatial_pooler = SpatialPooler(spset)
        self.input = None
        self.compress_input = None

    def move(self):
        # Spatial Pooler step
        self.input=self.generator.get_data()
        inp = to_vector(self.generator.get_data())
        ov = self.spatial_pooler.update_overlaps(self.spatial_region.get_columns(), inp)
        self.spatial_pooler.inhibition_phase(self.spatial_region.get_columns(), ov)
        self.compress_input = to_matrix(self.spatial_region)

        # Temporal Pooler step
        self.temporal_pooler.step_forward(self.compress_input)

        # Input generator step
        self.generator.move()

if __name__ == "__main__":
    htm = HTMCore()
    htm.move()
