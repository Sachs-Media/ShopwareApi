class Convert:
    """
        A very basic converter class
    """

    @staticmethod
    def to_string(client, data, field, key):
        """
            Converts input value to string
            :return:
        """
        return (field.attribute_name, str(data[key]))

    @staticmethod
    def to_int(client, data, field, key):
        """
            Converts input value to int
            :return:
        """
        return field.attribute_name, int(data[key])

    @staticmethod
    def to_float(client, data, field, key):
        """
            Converts input value to float
            :return:
        """
        return field.attribute_name, float(data[key])

    @staticmethod
    def to_boolean(client, data, field, key):
        """
            Converts input value to float
            :return:
        """
        return field.attribute_name, bool(data[key])
