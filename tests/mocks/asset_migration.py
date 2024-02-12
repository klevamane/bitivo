""" Mock data for Migrating assets """
# System Imports
from collections import OrderedDict
INVALID_CATEGORY_NAME = 'lorem ipsum'
MOCK_BOOK_DATA = OrderedDict([('Test devices', [
    ['Device', 'Serial Number', 'Tag', 'Assignee', 'Date Assigned', 'Status'],
    ['Iphone 5C', 'DX3V7JTYHG7A', 'AND/TST/001', 'RESERVE - OPS', '', 'ok'],
    ['Iphone 5C', 'DX3V7JTYHG7B', 'AND/TST/001', 'RESERVE - OPS', '', 'ok'],
    ['Iphone 5C', 'DX3V7JTYHG7C', 'AND/TST/003', 'RESERVE - OPS', '', 'ok'],
    ['Iphone 5C', 'F72V514SHHG7D', '', 'OPS', '', 'bad status']
]),
                              (INVALID_CATEGORY_NAME,
                               [[
                                   'Device', 'Serial Number', 'Tag',
                                   'Assignee', 'Date Assigned', 'Status'
                               ],
                                [
                                    'Iphone 5C', 'DX3V7JTYHG7A', 'AND/TST/001',
                                    'RESERVE - OPS', '', 'ok'
                                ]])])

RAW_ET_OTHERS_DATA = [
    [
        'S/N', 'Code ID Ref.', 'Date of Purchase', 'Item description',
        'Name of Manufacturer', 'Quantity',
        'Model/Series/Colour/Material and Manufacturer\'s Ref. no',
        'Location/Areas served', 'Maintenance period/History',
        'Operation Maintenance Instructions', 'Warranty/Guarantee data',
        'Condition', 'Other Relevant info', 'Initial cost'
    ],
    [
        '1', 'AND/LA/ET/WD/001', '', 'Water dispenser', 'CWAY', '1',
        'BYB87516100148', 'LAGOS TRAFFIC', '', '', '', '', '', ''
    ],
    [
        '1', 'AND/LA/ET/WD/002', '', 'Water dipenser', 'CWAY', '1',
        'BYB87516100148', 'LAGOS TRAFFIC', '', '', '', '', '', ''
    ],
    [
        '3', 'AND/LA/ET/WD/003-004', '', 'Water dipenser', 'CWAY', '1',
        'BYB87516100148', 'LAGOS TRAFFIC', '', '', '', '', '', ''
    ]
]

CLEAN_ET_OTHERS_DATA = {
    'Water dispenser': [
        [
            'Tag', 'Date of Purchase', 'Item description',
            'Name of Manufacturer',
            "Model/Series/Colour/Material and Manufacturer's Ref. no",
            'Assignee', 'Maintenance period/History',
            'Operation Maintenance Instructions', 'Warranty/Guarantee data',
            'Condition', 'Other Relevant info', 'Initial cost', 'Status'
        ],
        [
            'AND/LA/ET/WD/001', '', 'Water dispenser', 'CWAY',
            'BYB87516100148', 'LAGOS TRAFFIC', '', '', '', '', '', '', 'ok'
        ],
        [
            'AND/LA/ET/WD/002', '', 'Water dipenser', 'CWAY', 'BYB87516100148',
            'LAGOS TRAFFIC', '', '', '', '', '', '', 'ok'
        ],
        [
            'AND/LA/ET/WD/003', '', 'Water dipenser', 'CWAY', 'BYB87516100148',
            'LAGOS TRAFFIC', '', '', '', '', '', '', 'ok'
        ],
        [
            'AND/LA/ET/WD/004', '', 'Water dipenser', 'CWAY', 'BYB87516100148',
            'LAGOS TRAFFIC', '', '', '', '', '', '', 'ok'
        ],
    ]
}

RAW_TEST_DEVICES_DATA = [
    [
        '', 'S/N', 'Model', 'Serial Number/IMEI', 'Tag', 'Custodians',
        'Partner name', 'TSM', 'Date Collected', 'Date returned'
    ],
    [
        '', 1, 'Iphone 5C', 'DX3V7JTYHG7F', 'AND/TST/001', 'RESERVE - OPS', '',
        '', '', ''
    ],
    [
        '', 2, 'Iphone 5C', 'F72V514SHHG7H', 'AND/TST/002', 'OPS', '', '', '',
        ''
    ],
    [
        'PARTNER DEVICES', 7, 'iPad 4 (with Retina display)', 'DMPNC42BF182',
        'AND/TST/007', 'Abubakar Oladeji', '', '', '', ''
    ],
    [
        '', 7, 'iPad 4 (with Retina display)', 'DMPNC42BF182', 'AND/TST/007',
        'Abubakar Oladeji', '', '', '', ''
    ],
    [
        '', 7, 'iPad 4 (with Retina display)', 'DMPNC42BF182', 'AND/TST/007',
        'Abubakar Oladeji', '', '', '', ''
    ]
]

CLEAN_TEST_DEVICES_DATA = {
    'Test Devices': [[
        'Model', 'Serial Number/IMEI', 'Tag', 'Assignee', 'Partner name',
        'TSM', 'Date Collected', 'Date returned', 'Status'
    ],
                     [
                         'Iphone 5C', 'DX3V7JTYHG7F', 'AND/TST/001',
                         'RESERVE - OPS', '', '', '', '', 'Inventory'
                     ],
                     [
                         'Iphone 5C', 'F72V514SHHG7H', 'AND/TST/002', 'OPS',
                         '', '', '', '', 'Availabe'
                     ]],
    'Partner Devices':
    [[
        'Model', 'Serial Number/IMEI', 'Tag', 'Assignee', 'Partner name',
        'TSM', 'Date Collected', 'Date returned', 'Status'
    ],
     [
         'iPad 4 (with Retina display)', 'DMPNC42BF182', 'AND/TST/007',
         'Abubakar Oladeji', '', '', '', '', 'Assigned'
     ]]
}

DATA = [['', 'Tag', 'Custodian', 'Designation', '', ''],
        [1, 'AND/UCD/001', '', 'Fellow', 'Prev User: Raphael Etim', 'Faulty'],
        [2, 'AND/UCD/002', 'Temitope Joloko', 'Fellow', '', 'Changed'],
        [3, 'AND/UCD/003', 'Gbenga Oyetade', 'Fellow', 'Faulty', ''],
        [4, 'AND/UCD/004', 'Aaron Biliyok', 'Fellow', '', 'Changed'],
        [5, 'AND/UCD/005', '', 'Staff', 'Slim Momoh', 'Faulty'],
        [6, 'AND/UCD/006', 'Enodi Audu', 'Fellow', '', 'Changed']]

CLEAN_MOCK_USB_DATA = [
    ['Tag', 'Assignee', 'Designation', 'Prev User', 'Status'],
    ['AND/UCD/001', '', 'Fellow', ' Raphael Etim', 'Faulty'],
    ['AND/UCD/002', 'Temitope Joloko', 'Fellow', '', 'Changed'],
    ['AND/UCD/003', 'Gbenga Oyetade', 'Fellow', '', ''],
    ['AND/UCD/004', 'Aaron Biliyok', 'Fellow', '', 'Changed'],
    ['AND/UCD/005', '', 'Staff', 'Slim Momoh', 'Faulty'],
    ['AND/UCD/006', 'Enodi Audu', 'Fellow', '', 'Changed']
]
