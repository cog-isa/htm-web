import pickle
import HTMSettings
from mappers.VerySimpleMapper import verySimpleMapper
from socketModule import socketModule
from spooler import SpatialPooler
import temporalPooler.htm__region as tp
from region import Region
from settings import *

__author__ = 'AVPetrov'

# реализует ответ на запрос - Дай состояние и сделай шаг вперед
class htm_server:
    def __init__(self,port):
        self.port=port

    def handle(self,data,answer):
        if(data.decode('utf-8')=="get"):
            return answer
        else:
            return {"status":404}

    def toVector(self,m):
        output=[]
        for i in m:
            for j in i:
                output.append(j)
        return output

    def toMatrix(self,region):
        return [[region.getColumns()[j*region.getColH() + i].getIsActive() for i in range(region.getColH())] for j in range(region.getColW())]

    def start(self):
        server=socketModule()
        server.openLocalPort(self.port)

        generator = MakeBubble(GENERATOR, REGION_SIZE_N, SCALE)

        setting = HTMSettings.HTMSettings.getDefaultSettings()
        setting.debug = True

        setting.activationThreshold = 1
        setting.minOverlap = 1
        setting.desiredLocalActivity = 3
        setting.connectedPct = 1
        setting.xInput = REGION_SIZE_N*SCALE
        setting.yInput = REGION_SIZE_N*SCALE
        setting.potentialRadius = 2
        setting.xDimension = 1
        setting.yDimension = 1
        setting.initialInhibitionRadius=1
        setting.cellsPerColumn=5

        r = Region(setting,verySimpleMapper())
        r_t=tp.Region(setting.xDimension, setting.cellsPerColumn)
        sp=SpatialPooler(setting)

        for i in range(STEPS_NUMBER):
            inp=self.toVector(generator.get_data())
            # generator.out()

            ov=sp.updateOverlaps(r.getColumns(), inp)
            sp.inhibitionPhase(r.getColumns(), ov)
            # sp.learningPhase(r.getColumns(), inp, ov)

            inp_t=self.toMatrix(r)

            for j in inp_t:
                print(j)

            r_t.step_forward(inp_t)
            r_t.out_prediction()
            generator.move()
            server.waitForRqst(lambda data: self.handle(data,r_t))
