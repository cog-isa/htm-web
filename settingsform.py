import sys

sys.path.insert(0, "htm-web/")
sys.path.insert(0, "htm-core/")
sys.path.insert(0, "htm-core/spatialPooler")
sys.path.insert(0, "htm-core/temporalPooler")
sys.path.insert(0, "htm-core/gens")
sys.path.insert(0, "htm-core/apps")

from settings import SpatialSettings, TemporalSettings, InputSettings
from gens.input_generators import *

from spatialPooler.mappers.sp_simple_mapper import SimpleMapper
from spatialPooler.mappers.sp_square_mapper import SquareMapper
from spatialPooler.mappers.sp_square_mapper_auto_radius import SquareMapperAutoRadius
from spatialPooler.mappers.sp_very_simple_mapper import VerySimpleMapper


__author__ = 'AVPetrov'

from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, FloatField, SelectField

gens = {
        "TestSimpleSteps" : TestSimpleSteps , "ConstantActiveBit" : ConstantActiveBit,
        "TooTestSimpleSteps" : TooTestSimpleSteps, "Too2TestSimpleSteps" : Too2TestSimpleSteps,
        "HardSteps" : HardSteps, "HardStepsLen2" : HardStepsLen2, "Cross" : Cross, "Snake":Snake
       }

mappers = {
        "SquareMapperAutoRadius" :  SquareMapperAutoRadius, "SquareMapper" : SquareMapper,
        "SimpleMapper" : SimpleMapper, "VerySimpleMapper" : VerySimpleMapper
       }

class SettingsForm(Form):
    # SpatialPooler Settings
    setname = StringField('Settings name', [validators.Length(min=4, max=35)], default="Default name")
    debug = BooleanField('Debug', [validators.DataRequired()], default=True)
    activation_threshold = IntegerField('ActivationThreshold', [validators.DataRequired()], default=1)
    min_overlap = IntegerField('MinOverlap', [validators.DataRequired()], default=1)
    desired_local_activity = IntegerField('DesiredLocalActivity', [validators.DataRequired()], default=3)
    connected_pct = IntegerField('ConnectedPercent', [validators.DataRequired()], default=1)
    connected_perm = FloatField('PermanenceThreshold', [validators.DataRequired()], default=0.01)
    xinput = IntegerField('InputWidth', [validators.DataRequired()], default=3)
    yinput = IntegerField('InputHeight', [validators.DataRequired()], default=3)
    potential_radius = IntegerField('PotentialRadius', [validators.DataRequired()], default=4)
    xdimension = IntegerField('ColumnsWidth', [validators.DataRequired()], default=3)
    ydimension = IntegerField('ColumnsHeight', [validators.DataRequired()], default=3)
    initial_inhibition_radius = IntegerField('InitialInhibitionRadius', [validators.DataRequired()], default=1)
    permanence_inc = FloatField('PermanenceInc', [validators.DataRequired()], default=0.1)
    permanence_dec = FloatField('PermanenceDec', [validators.DataRequired()], default=0.1)
    max_boost = IntegerField('MaxBoost', [validators.DataRequired()], default=1)
    min_duty_cycle_fraction = FloatField('MinDutyCycleFraction', [validators.DataRequired()], default=0.2)

    # TemporalPooler Settings
    column_size = IntegerField('CellsPerColumn', [validators.DataRequired()], default=3)
    initial_permanence =  FloatField('InitialPermanence', [validators.DataRequired()], default=0.30)
    synapse_threshold =  FloatField('SynapseThreshold', [validators.DataRequired()], default=0.25)
    dendrite_permanence_inc_delta =  FloatField('DendritePermanenceIncDelta', [validators.DataRequired()], default=0.02)
    dendrite_permanence_dec_delta =  FloatField('DendritePermanenceDecDelta', [validators.DataRequired()], default=-0.1)
    dendrite_activate_threshold =  FloatField('DendriteActivateThreshold', [validators.DataRequired()], default=1)
    passive_time_to_active_threshold = IntegerField('PassiveTimeToActiveThreshold', [validators.DataRequired()], default=2000)

    # Input Settings
    scale = IntegerField('InputScale', [validators.DataRequired()], default=2)
    steps_number = IntegerField('GeneratorStepsNumber', [validators.DataRequired()], default=100)
    # generator = HardSteps
    # generator = ConstantActiveBit
    # generator = TestSimpleSteps
    generator = SelectField('Generator', choices = [(list(gens.keys())[i],list(gens.keys())[i]) for i in range(len(gens.keys()))], default=1, validators = [validators.DataRequired()])
    mapper = SelectField('Mapper', choices = [(list(mappers.keys())[i],list(mappers.keys())[i]) for i in range(len(mappers.keys()))], default="SquareMapperAutoRadius", validators = [validators.DataRequired()])

    def getSpatialSettings(self):
        spset = SpatialSettings()
        spset.debug = self.debug.data
        spset.activation_threshold = self.activation_threshold.data
        spset.min_overlap = self.min_overlap.data
        spset.desired_local_activity = self.desired_local_activity.data
        spset.connected_pct = self.connected_pct.data
        spset.connected_perm = self.connected_perm.data
        spset.xinput = self.xinput.data
        spset.yinput = self.yinput.data
        spset.potential_radius = self.potential_radius.data
        spset.xdimension = self.xdimension.data
        spset.ydimension = self.ydimension.data
        spset.initial_inhibition_radius = self.initial_inhibition_radius.data
        spset.permanence_inc = self.permanence_inc.data
        spset.permanence_dec = self.permanence_dec.data
        spset.max_boost = self.max_boost.data
        spset.min_duty_cycle_fraction = self.min_duty_cycle_fraction.data
        return spset

    def getTemporalSettings(self):
        tpset = TemporalSettings()
        tpset.COLUMN_SIZE = self.column_size.data
        tpset.INITIAL_PERMANENCE = self.initial_permanence.data
        tpset.SYNAPSE_THRESHOLD = self.synapse_threshold.data
        tpset.DENDRITE_PERMANENCE_INC_DELTA = self.dendrite_permanence_inc_delta.data
        tpset.DENDRITE_PERMANENCE_DEC_DELTA = self.dendrite_permanence_dec_delta.data
        tpset.DENDRITE_ACTIVATE_THRESHOLD = self.dendrite_activate_threshold.data
        tpset.PASSIVE_TIME_TO_ACTIVE_THRESHOLD = self.passive_time_to_active_threshold.data
        return tpset

    def getInputSettings(self):
        inset = InputSettings()
        inset.SCALE = self.scale.data
        inset.STEPS_NUMBER = self.steps_number.data
        inset.GENERATOR = gens[self.generator.data]
        inset.MAPPER = mappers[self.mapper.data]
        return inset


