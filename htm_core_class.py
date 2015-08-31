from spooler import SpatialPooler
import htm__region as tp
from settings import *
from htm__region import Region as TemporalPoolerRegion


class HTMCore:
    def __init__(self):
        self.generator = MakeBubble(GENERATOR, REGION_SIZE_N, SCALE)

        setting = SpatialSettings.get_default_settings()
        setting.debug = True

        setting.activation_threshold = 1
        setting.min_overlap = 1
        setting.desired_local_activity = 3
        setting.connectet_Pct = 1
        setting.xinput = REGION_SIZE_N * SCALE
        setting.yinput = REGION_SIZE_N * SCALE
        setting.potential_radius = 2
        setting.xdimension = 1
        setting.ydimension = 1
        setting.initial_inhibition_radius = 1
        setting.cells_per_column = 5

        self.temporal_pooler = TemporalPoolerRegion(REGION_SIZE_N * SCALE, COLUMN_SIZE)


        r_t = tp.Region(setting.xdimension, setting.cells_per_column)
        self.spatial_pooler = SpatialPooler(setting)



