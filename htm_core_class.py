import sp_region as sp
import htm__region as tp
from settings import *
from spatialPooler.mappers.sp_square_mapper import SquareMapper

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
        self.spatial_pooler = sp.Region(spset, SquareMapper)
        self.temporal_pooler = tp.Region(spset.xdimension, tpset.COLUMN_SIZE)
        # не стоит это сереализовывать
        self.input = None
        self.compress_input = None

    def move(self):
        # get data from generator
        self.input=self.generator.get_data()

        # Spatial Pooler step
        self.compress_input = self.spatial_pooler.step_forward(self.input)

        # Temporal Pooler step
        self.temporal_pooler.step_forward(self.compress_input)

        # Input generator step
        self.generator.move()

if __name__ == "__main__":
    htm = HTMCore()
    htm.move()
