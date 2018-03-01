def validate_business_type(type):
  valid_resource_types = ["restaurant", "shul", "mikvah", "store", "other"]
  if type in valid_resource_types:
    return type
  raise Exception(type + " not in " + str(valid_resource_types))

class Resource:
  def __init__(self, name, type, contact, lat, long, other):
    self.name = name
    self.type = validate_business_type(type)
    self.contact = contact
    self.lat = lat
    self.long = long
    self.other = other

