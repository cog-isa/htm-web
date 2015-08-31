from spatialPooler import sp_settings
from spooler import SpatialPooler
import htm__region as tp
from settings import temporal_settings, spatial_settings
from htm__region import Region as TemporalPoolerRegion
from gens.input_generators import MakeBubble


class HTMCore:
    def __init__(self):
        self.generator = MakeBubble(temporal_settings.GENERATOR, temporal_settings.REGION_SIZE_N, temporal_settings.SCALE)
        self.temporal_settings = temporal_settings
        self.spatial_settings = spatial_settings

        setting = sp_settings.HTMSettings.get_default_settings()
        setting.debug = True

        setting.activationThreshold = 1
        setting.minOverlap = 1
        setting.desiredLocalActivity = 3
        setting.connectedPct = 1
        setting.xInput = temporal_settings.REGION_SIZE_N * temporal_settings.SCALE
        setting.yInput = temporal_settings.REGION_SIZE_N * temporal_settings.SCALE
        setting.potentialRadius = 2
        setting.xDimension = 1
        setting.yDimension = 1
        setting.initialInhibitionRadius = 1
        setting.cellsPerColumn = 5

        self.temporal_pooler = TemporalPoolerRegion(temporal_settings.REGION_SIZE_N * temporal_settings.SCALE, temporal_settings.COLUMN_SIZE)


        r_t = tp.Region(setting.xDimension, setting.cellsPerColumn)
        self.spatial_pooler = SpatialPooler(setting)



