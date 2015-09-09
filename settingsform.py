__author__ = 'AVPetrov'

from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, FloatField


class SettingsForm(Form):
    name = StringField('Settings name', [validators.Length(min=4, max=35)])
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



