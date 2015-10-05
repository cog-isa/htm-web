import sp_region as sp
import htm__region as tp
from settings import *

class HTMCore:
    def __init__(self, inset, spset, tpset):
        self.generator = MakeBubble(inset.GENERATOR, spset.xinput,
                                    inset.SCALE)

        spset.xinput=spset.xinput*inset.SCALE
        spset.yinput=spset.xinput*inset.SCALE

        self.spatial_pooler = sp.Region(spset, inset.MAPPER)
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
