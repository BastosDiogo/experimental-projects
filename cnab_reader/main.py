import json
from cnab import CnabManipulation

file = '<file path>'

cnab_fields = {
    'header': {
        'field_1_name': {
            'name': 'cabecalho',
            'description': 'Type of descripition',
            'position': (12, 17)
        },
        'field_2_file_type': {
            'name': 'file_type',
            'description': 'File type',
            'position': (19, 23)
        }
    },
    'detalhes': {
        'field_1_info_name': {
            'name': 'info_name',
            'description': 'Name form info',
            'position': (12, 20)
        },
        'field_2_row_count': {
            'name': 'row_count',
            'description': 'Count total of rows.',
            'position': (27, 30)
        }
    },
    'trailer': {
        'field_1_doc_number': {
            'name': 'doc_number',
            'description': 'Number of document.',
            'position': (1, 1)
        },
        'field_2_total_rows': {
            'name': 'total_rows',
            'description': 'File total rows',
            'position': (27, 30)
        }
    }
}

cnab = CnabManipulation(file, 400, cnab_fields).run()
print(json.dumps(cnab, indent=4))
