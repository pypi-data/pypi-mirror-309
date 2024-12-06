
class DataType:
    @staticmethod
    def is_list_of_tuples(data):
        """
        Verifies if data is a list of tuples.

        :param data: Data to verify
        :return: True if list of tuples, False otherwise
        """
        if not isinstance(data, list):
            return False

        for element in data:
            if not isinstance(element, tuple) or len(element) != 2:
                return False

        return True
