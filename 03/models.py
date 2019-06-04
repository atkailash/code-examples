from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import InputRequired, NumberRange


class CoordinateForm(FlaskForm):
    lat = DecimalField(label="Latitude: ",
                       validators=[InputRequired(),
                                   NumberRange(min=-90.0,
                                               max=90.0,
                                               message="Should be between -90.0 and 90.0")
                                   ]
                       )
    long = DecimalField(label="Longitude: ",
                        validators=[InputRequired(),
                                    NumberRange(min=-180.0,
                                                max=180.0,
                                                message="Should be between -180.0 and 180.0")
                                    ]
                        )
    submit = SubmitField("Submit")
