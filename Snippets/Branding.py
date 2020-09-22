from PySense import PySense

# Authenticate
py_client = PySense.PySense('host', 'username', 'password')

# Get the current branding object
branding = py_client.get_branding()

# Get the JSON for the branding
branding_json = branding.get_json()

# Set the new branding attribute
branding_json['contactUsText'] = 'New contact us text'

# Update the branding object
branding.set_json(branding_json)

# Update PySense with new branding
py_client.set_branding(branding)