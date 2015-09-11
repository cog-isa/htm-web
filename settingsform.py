__author__ = 'AVPetrov'

from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, FloatField, SelectField


class SettingsForm(Form):
    # SpatialPooler Settings
    setname = StringField('Settings name', [validators.Length(min=4, max=35)])
    debug = BooleanField('Debug', [validators.DataRequired()])
    activation_threshold = IntegerField('activation_threshold', [validators.DataRequired()])
    min_overlap = IntegerField('min_overlap', [validators.DataRequired()])
    desired_local_activity = IntegerField('desired_local_activity', [validators.DataRequired()])
    connected_pct = IntegerField('connected_pct', [validators.DataRequired()])
    connected_perm = FloatField('connected_perm', [validators.DataRequired()])
    xinput = IntegerField('xinput', [validators.DataRequired()])
    yinput = IntegerField('yinput', [validators.DataRequired()])
    potential_radius = IntegerField('potential_radius', [validators.DataRequired()])
    xdimension = IntegerField('xdimension', [validators.DataRequired()])
    ydimension = IntegerField('ydimension', [validators.DataRequired()])
    initial_inhibition_radius = IntegerField('initial_inhibition_radius', [validators.DataRequired()])
    permanence_inc = FloatField('permanence_inc', [validators.DataRequired()])
    permanence_dec = FloatField('permanence_dec', [validators.DataRequired()])
    cells_per_column = IntegerField('cells_per_column', [validators.DataRequired()])
    max_boost = IntegerField('max_boost', [validators.DataRequired()])
    min_duty_cycle_fraction = IntegerField('min_duty_cycle_fraction', [validators.DataRequired()])

    # TemporalPooler Settings
    region_size_n = IntegerField('region_size_n', [validators.DataRequired()])
    column_size = IntegerField('column_size', [validators.DataRequired()])
    initial_permanence =  FloatField('initial_permanence', [validators.DataRequired()])
    synapse_threshold =  FloatField('synapse_threshold', [validators.DataRequired()])
    dendrite_permanence_inc_delta =  FloatField('dendrite_permanence_inc_delta', [validators.DataRequired()])
    dendrite_permanence_dec_delta =  FloatField('dendrite_permanence_dec_delta', [validators.DataRequired()])
    dendrite_activate_threshold =  FloatField('dendrite_activate_threshold', [validators.DataRequired()])
    passive_time_to_active_threshold = IntegerField('passive_time_to_active_threshold', [validators.DataRequired()])

    # Input Settings
    scale = IntegerField('scale', [validators.DataRequired()])
    steps_number = IntegerField('steps_number', [validators.DataRequired()])
    # generator = HardSteps
    # generator = ConstantActiveBit
    # generator = TestSimpleSteps
    generator = SelectField('generator', choices = [("TestSimpleSteps", "TestSimpleSteps"), ("ConstantActiveBit", "ConstantActiveBit")], default=1, validators = [validators.DataRequired()])




