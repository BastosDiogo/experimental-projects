import json


class Cnab():
    """Classe for read CNABs."""
    def __init__(self, cnab_size:str):
        self._cnab_size = cnab_size

    @property
    def cnab_size(self):
        return self._cnab_size


    def data_manipulation(self, file_red: list | tuple, action:dict={'remove': '\n'}):
        """Funtion for revome a specific word."""
        remove = action['remove']

        remove_function = lambda x: x.replace(remove, '')
        return tuple(remove_function(row) for row in file_red)


    def assests(self, cnab_parts: dict):
        list_asserted = []

        for parts in tuple(cnab_parts.values()):
            if isinstance(parts, str):
                asserted = len(parts) == self.cnab_size

            else:
                asserted = next((False for part in parts if len(part) != self.cnab_size), True)
            
            list_asserted.append(asserted)

        return False if False in list_asserted else True


    def read(self, file:str, total_header:int, total_trailer:int):
        with open(file, mode='r') as arq:
            file_red = self.data_manipulation(arq.readlines(), action={'remove': '\n'})

            cnab_parts = {
                'header': file_red[0] if total_header == 1 else file_red[0: total_header],
                'detalhes': file_red[total_header: -total_trailer],# file_red[1:-1],
                'trailer': file_red[-total_trailer:]
            }

            if not self.assests(cnab_parts):
                raise Exception(f'Follow file there is not match with CNAB file. Cnab size: {self.cnab_size}')

        return cnab_parts


class CnabManipulation(Cnab):
    """Class to manipulate Cnab's data."""
    def __init__(self, file:str, cnab_size:int, cnab_fields:dict):
        super().__init__(cnab_size)
        self._cnab_fields = cnab_fields
        self._file = file

    @property
    def cnab_fields(self):
        return self._cnab_fields

    @property
    def file(self):
        return self._file


    def extract_fields(self, lines, transformations):
        result = {}

        for field_transformation, trans_field in transformations.items():
            position = trans_field['position']

            if isinstance(lines, str):
                cnab_data = lines[(position[0] - 1): position[1]]
            else:
                cnab_data = [
                    line[(position[0] - 1): position[1]]
                    for line in lines
                ]

            result[field_transformation] = cnab_data
            result[f'{field_transformation}_position'] = position

        return result


    def run(self, total_header: int = 1, total_trailer: int = 1):
        file_red = self.read(self.file, total_header, total_trailer)
        print(f'CNAB has been red:\n{json.dumps(file_red, indent=4)}')

        cnab_fields_red = {}

        for field, lines in file_red.items():
            transformations = self.cnab_fields[field]
            cnab_fields_red[field] = self.extract_fields(lines, transformations)

        return cnab_fields_red
