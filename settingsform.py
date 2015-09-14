from gens.input_generators import TestSimpleSteps, ConstantActiveBit
from settings import SpatialSettings, TemporalSettings, InputSettings

__author__ = 'AVPetrov'

from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, FloatField, SelectField


class SettingsForm(Form):
    # SpatialPooler Settings
    setname = StringField('Settings name', [validators.Length(min=4, max=35)], default="Default name")
    debug = BooleanField('Debug', [validators.DataRequired()], default=True)
    activation_threshold = IntegerField('activation_threshold', [validators.DataRequired()], default=1)
    min_overlap = IntegerField('min_overlap', [validators.DataRequired()], default=1)
    desired_local_activity = IntegerField('desired_local_activity', [validators.DataRequired()], default=3)
    connected_pct = IntegerField('connected_pct', [validators.DataRequired()], default=1)
    connected_perm = FloatField('connected_perm', [validators.DataRequired()], default=0.01)
    xinput = IntegerField('xinput', [validators.DataRequired()], default=1)
    yinput = IntegerField('yinput', [validators.DataRequired()], default=1)
    potential_radius = IntegerField('potential_radius', [validators.DataRequired()], default=4)
    xdimension = IntegerField('xdimension', [validators.DataRequired()], default=10)
    ydimension = IntegerField('ydimension', [validators.DataRequired()], default=10)
    initial_inhibition_radius = IntegerField('initial_inhibition_radius', [validators.DataRequired()], default=1)
    permanence_inc = FloatField('permanence_inc', [validators.DataRequired()], default=0.1)
    permanence_dec = FloatField('permanence_dec', [validators.DataRequired()], default=0.1)
    max_boost = IntegerField('max_boost', [validators.DataRequired()], default=1)
    min_duty_cycle_fraction = IntegerField('min_duty_cycle_fraction', [validators.DataRequired()], default=2)

    # TemporalPooler Settings
    region_size_n = IntegerField('region_size_n', [validators.DataRequired()], default=3)
    column_size = IntegerField('column_size', [validators.DataRequired()], default=3)
    initial_permanence =  FloatField('initial_permanence', [validators.DataRequired()], default=0.30)
    synapse_threshold =  FloatField('synapse_threshold', [validators.DataRequired()], default=0.25)
    dendrite_permanence_inc_delta =  FloatField('dendrite_permanence_inc_delta', [validators.DataRequired()], default=0.02)
    dendrite_permanence_dec_delta =  FloatField('dendrite_permanence_dec_delta', [validators.DataRequired()], default=-0.1)
    dendrite_activate_threshold =  FloatField('dendrite_activate_threshold', [validators.DataRequired()], default=1)
    passive_time_to_active_threshold = IntegerField('passive_time_to_active_threshold', [validators.DataRequired()], default=2000)

    # Input Settings
    scale = IntegerField('scale', [validators.DataRequired()], default=3)
    steps_number = IntegerField('steps_number', [validators.DataRequired()], default=100)
    # generator = HardSteps
    # generator = ConstantActiveBit
    # generator = TestSimpleSteps
    generator = SelectField('generator', choices = [(TestSimpleSteps, "TestSimpleSteps"), (ConstantActiveBit, "ConstantActiveBit")], default=1, validators = [validators.DataRequired()])

    def getSpatialSettings(self):
        spset = SpatialSettings()
        spset.debug = self.debug.data
        spset.activation_threshold = self.activation_threshold.data
        spset.min_overlap = self.min_overlap.data
        spset.desired_local_activity = self.desired_local_activity.data
        spset.connected_pct = self.connected_pct.data
        spset.connected_perm = self.connected_perm.data
        spset.xinput = self.xinput
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
        tpset.region_size_n = self.region_size_n.data
        tpset.column_size = self.column_size.data
        tpset.initial_permanence = self.initial_permanence.data
        tpset.synapse_threshold = self.synapse_threshold.data
        tpset.dendrite_permanence_inc_delta = self.dendrite_permanence_inc_delta.data
        tpset.dendrite_permanence_dec_delta = self.dendrite_permanence_dec_delta.data
        tpset.dendrite_activate_threshold = self.dendrite_activate_threshold.data
        tpset.passive_time_to_active_threshold = self.passive_time_to_active_threshold.data
        return tpset

    def getInputSettings(self):
        inset = InputSettings()
        inset.scale = self.scale.data
        inset.steps_number = self.steps_number.data
        inset.generator = self.generator.data
        return inset


