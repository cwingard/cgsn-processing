# CG and EA Mooring Configuration Templates

The Coastal and Global (CG) and Endurance Array (EA) instrument teams use sets of templates to configure moorings
for use in the OMS++ system and elsewhere. These templates are stored in the `templates` directory of the `utilities`
folder. The templates are written in the [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/) templating language
and are used to produce YAML configuration files filling in the specific details of the mooring configuration
such as the instrument serial numbers, deployment dates, and other details specific to that mooring deployment 
from the Roundabout database (RDB) used by CG and EA to record mooring build details.

