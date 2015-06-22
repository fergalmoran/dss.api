from rest_framework.fields import Field


class DisplayNameField(Field):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        if not value:
            return self.parent.data['first_name'] + ' ' + self.parent.data['last_name']
        return value

