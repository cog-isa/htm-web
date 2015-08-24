import HTMSettings
from spooler import SpatialPooler
import htm__region as tp
from settings import *
from htm__region import Region as TemporalPoolerRegion


class HTMCore:
    def __init__(self):
        self.generator = MakeBubble(GENERATOR, REGION_SIZE_N, SCALE)

        setting = HTMSettings.HTMSettings.getDefaultSettings()
        setting.debug = True

        setting.activationThreshold = 1
        setting.minOverlap = 1
        setting.desiredLocalActivity = 3
        setting.connectedPct = 1
        setting.xInput = REGION_SIZE_N * SCALE
        setting.yInput = REGION_SIZE_N * SCALE
        setting.potentialRadius = 2
        setting.xDimension = 1
        setting.yDimension = 1
        setting.initialInhibitionRadius = 1
        setting.cellsPerColumn = 5

        self.temporal_pooler = TemporalPoolerRegion(REGION_SIZE_N * SCALE, COLUMN_SIZE)


        r_t = tp.Region(setting.xDimension, setting.cellsPerColumn)
        self.spatial_pooler = SpatialPooler(setting)



