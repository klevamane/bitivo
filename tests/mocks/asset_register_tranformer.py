# System Imports
from collections import OrderedDict

# Constants
from api.utilities.constants import HEADERS

SHEET_HEADERS = [
    '', 'Date of Purchase', 'Code ID Ref.', 'Description', 'Location',
    'Initial cost /NBV', '2015 Dep', '2016 Dep', '2017 Dep', 'NBV', '', '', ''
]

TRANSFORMED_HEADERS = [
    'Date of Purchase', 'Tag', 'Description', 'Assignee', 'Initial cost /NBV',
    '2015 Dep', '2016 Dep', '2017 Dep', 'NBV', 'Status'
]

ASSET_REGISTER_MOCK = {
    'Insured Assets': [
        SHEET_HEADERS,
        [
            'FUNITURE', '07/15/2015', 'AND/UT/00-001',
            '3 18U Mega Rack Cabinets', 'Amity', '16000', '11', '11', '11',
            '1200'
        ],
        [
            'FUNITURE', '07/15/2015', 'AND/UT/002', '3 18U Mega Rack Cabinets',
            'Amity', '16000', '11', '11', '11', '1200'
        ],
        [
            'FUNITURE', '07/15/2015', 'AND/UT/003', '3 18U Mega Rack Cabinets',
            'Amity', '16000', '11', '11', '11', '1200'
        ],
        [
            'FUNITURE', '07/15/2015', 'AND/UT/004', '3 18U Mega Rack Cabinets',
            'Amity', '16000', '11', '11', '11', '1200'
        ],
        [
            'GENERATOR', '07/15/2015', 'AND/UT/005',
            '3 18U Mega Rack Cabinets', 'Amity', '16000', '11', '11', '11',
            '1200'
        ],
        [
            'GENERATOR', '07/15/2015', 'AND/UT/006',
            '3 18U Mega Rack Cabinets', 'Amity', '16000', '11', '11', '11',
            '1200'
        ],
        [
            'GENERATOR', '07/15/2015', 'AND/UT/007',
            '3 18U Mega Rack Cabinets', 'Amity', '16000', '11', '11', '11',
            '1200'
        ],
        [
            'OFFICE EQUIPMENT', '07/15/2015', 'AND/UT/008',
            '3 18U Mega Rack Cabinets', 'Amity', '16000', '11', '11', '11',
            '1200'
        ],
        [
            'OFFICE EQUIPMENT', '07/15/2015', 'AND/UT/009',
            '3 18U Mega Rack Cabinets', 'Amity', '16000', '11', '11', '11',
            '1200'
        ],
        [
            'OFFICE EQUIPMENT', '07/15/2015', 'AND/UT/010-11',
            '3 18U Mega Rack Cabinets', 'Amity', '16000', '11', '11', '11',
            '1200'
        ],
        [
            'OFFICE EQUIPMENT', '07/15/2015', 'AND/UT/013-12, 014',
            '3 18U Mega Rack Cabinets', 'Amity', '16000', '11', '11', '11',
            '1200'
        ],
        [
            'OFFICE EQUIPMENT', '07/15/2015', 'AND/UT/T015-16',
            '3 18U Mega Rack Cabinets', 'Amity', '16000', '11', '11', '11',
            '1200'
        ],
    ]
}

TRANSFORMED_INSURED_ASSET_MOCK = {
    'FUNITURE': [
        TRANSFORMED_HEADERS,
        [
            '07/15/2015', 'AND/UT/000', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
        [
            '07/15/2015', 'AND/UT/001', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
        [
            '07/15/2015', 'AND/UT/002', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
        [
            '07/15/2015', 'AND/UT/003', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
        [
            '07/15/2015', 'AND/UT/004', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
    ],
    'GENERATOR': [
        TRANSFORMED_HEADERS,
        [
            '07/15/2015', 'AND/UT/005', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
        [
            '07/15/2015', 'AND/UT/006', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
        [
            '07/15/2015', 'AND/UT/007', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
    ],
    'OFFICE EQUIPMENT': [
        TRANSFORMED_HEADERS,
        [
            '07/15/2015', 'AND/UT/008', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
        [
            '07/15/2015', 'AND/UT/009', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
        [
            '07/15/2015', 'AND/UT/010', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
        [
            '07/15/2015', 'AND/UT/011', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
        [
            '07/15/2015', 'AND/UT/012', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
        [
            '07/15/2015', 'AND/UT/013', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
        [
            '07/15/2015', 'AND/UT/014', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
        [
            '07/15/2015', 'AND/UT/T/015', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
        [
            '07/15/2015', 'AND/UT/T/016', '3 18U Mega Rack Cabinets', 'Amity',
            '16000', '11', '11', '11', '1200', 'ok'
        ],
    ]
}

MOCK_ET_AIRCONDITIONER_DATA = OrderedDict(
    [('ET AIRCONDITIONERS',
      [[
          'SN', 'Code ID Ref.', 'Date of Purchase', 'Item description',
          'Name of Manufacturer',
          "Model/Series/Colour/Material and Manufacturer's Ref. no",
          'Location/Areas served', 'Maintenance period/History',
          'Operation Maintenance Instructions', 'Warranty/Guarantee data',
          'Condition', 'Other Relevant info', 'Initial cost'
      ],
       [
           ' EKO WING', ' EKO WING', ' EKO WING', ' EKO WING', ' EKO WING',
           ' EKO WING', ' EKO WING', ' EKO WING', ' EKO WING', ' EKO WING',
           ' EKO WING', ' EKO WING', ' EKO WING'
       ],
       [
           '1', 'AND/LA/ET/AC/001', 2017.0, '2HP Split Unit Air Conditioner',
           'DIAKIN', 'COO3219', 'CAFETERIA/ BAY 1', 'Test', 'Quarterly',
           'Warranty', 'Good', '', 193000.0
       ],
       [
           2, 'AND/LA/ET/AC/002', 2017.0, '2HP Split Unit Air Conditioner',
           'DIAKIN', 'COO7440', 'CAFETERIA/ BAY 1', 'Test', 'Quarterly',
           'Warranty', 'Good', '', 193000.0
       ],
       [
           3, 'AND/LA/ET/AC/003', 2017.0, '2HP Split Unit Air Conditioner',
           'DIAKIN', 'COO3221', 'CAFETERIA/ BAY 2', 'Test', 'Quarterly',
           'Warranty', 'Good', '', 193000.0
       ],
       [
           4, 'AND/LA/ET/AC/004', 2017.0, '2HP Split Unit Air Conditioner',
           'DIAKIN', 'COO2078', 'CAFETERIA/ BAY 2', 'Test', 'Quarterly',
           'Warranty', 'Good', '', 193000.0
       ],
       [
           5, 'AND/LA/ET/AC/005', 2017.0, '2HP Split Unit Air Conditioner',
           'DIAKIN', 'COO3O71', 'CAFETERIA/ BAY 3', 'Test', 'Quarterly',
           'Warranty', 'Good', '', 193000.0
       ],
       [
           6, 'AND/LA/ET/AC/006', 2017.0, '2HP Split Unit Air Conditioner',
           'DIAKIN', 'COO1850', 'CAFETERIA/ BAY 3', 'Test', 'Quarterly',
           'Warranty', 'Good', '', 193000.0
       ],
       [
           8, 'AND/LA/ET/AC/008', 2017, '2HP Split Unit Air Conditioner',
           'DIAKIN', 'COO7400', 'BAY 1', 'Test', 'Quarterly', 'Warranty',
           'Good', '', 193000
       ]])])

CLEAN_MOCK_ET_AIRCONDITIONER_DATA = OrderedDict([('ET AIRCONDITIONERS', [
    [
        'Tag', 'Date of Purchase', 'Item description', 'Name of Manufacturer',
        'Model', 'Assignee', 'Maintenance Period',
        'Operation Maintenance Instructions', 'Warranty', 'Status',
        'Initial cost'
    ],
    [
        'AND/LA/ET/AC/001', 2017.0, '2HP Split Unit Air Conditioner', 'DIAKIN',
        'COO3219', 'CAFETERIA', 'Test', 'Quarterly', 'Warranty', 'ok', 193000.0
    ],
    [
        'AND/LA/ET/AC/002', 2017.0, '2HP Split Unit Air Conditioner', 'DIAKIN',
        'COO7440', 'CAFETERIA', 'Test', 'Quarterly', 'Warranty', 'ok', 193000.0
    ],
    [
        'AND/LA/ET/AC/003', 2017.0, '2HP Split Unit Air Conditioner', 'DIAKIN',
        'COO3221', 'CAFETERIA', 'Test', 'Quarterly', 'Warranty', 'ok', 193000.0
    ],
    [
        'AND/LA/ET/AC/004', 2017.0, '2HP Split Unit Air Conditioner', 'DIAKIN',
        'COO2078', 'CAFETERIA', 'Test', 'Quarterly', 'Warranty', 'ok', 193000.0
    ],
    [
        'AND/LA/ET/AC/005', 2017.0, '2HP Split Unit Air Conditioner', 'DIAKIN',
        'COO3O71', 'CAFETERIA', 'Test', 'Quarterly', 'Warranty', 'ok', 193000.0
    ],
    [
        'AND/LA/ET/AC/006', 2017.0, '2HP Split Unit Air Conditioner', 'DIAKIN',
        'COO1850', 'CAFETERIA', 'Test', 'Quarterly', 'Warranty', 'ok', 193000.0
    ],
    [
        'AND/LA/ET/AC/008', 2017, '2HP Split Unit Air Conditioner', 'DIAKIN',
        'COO7400', ' EKO WING', 'Test', 'Quarterly', 'Warranty', 'ok', 193000
    ]
])])

CLEAN_AMITY_DATA = OrderedDict(
    [('1HP Split Unit Air Conditioner', [
        HEADERS,
        [
            'AND/LOS/AM/AC/001', 2017, '1HP Split Unit Air Conditioner',
            'DIAKIN', 'C009853', 'OBECHE ROOM 1', 'Test', 'Quarterly',
            'Warranty', 'ok', 100000
        ]
    ]),
     ('Swivel Chair', [
         HEADERS,
         [
             'AND/LOS/AM/CH/0031', 2017, 'Swivel Chair', 'LIFEMATE',
             'BLACK MESH', 'HACKSAW SITTING ROOM', 'Cleaning and Wiping down',
             'Weekly', 'Warranty', 'ok', '25,000'
         ],
         [
             'AND/LOS/AM/CH/0032', 2017, 'Swivel Chair', 'LIFEMATE',
             'BLACK MESH', 'HACKSAW SITTING ROOM', 'Cleaning and Wiping down',
             'Weekly', 'Warranty', 'ok', '25,000'
         ]
     ]), ('Gascooker', [HEADERS]), ('Fridge', [HEADERS]),
     ('Water dispenser', [HEADERS]), ('Microwave', [HEADERS]),
     ('Gas cylinder', [HEADERS]), ('FUEL TANK 1500litres', [HEADERS]),
     ('Fire Extinguisher', [HEADERS]), ('7.5kva Inverter', [HEADERS]),
     ('3.5Kva', [HEADERS]),
     ('Generators', [
         HEADERS,
         [
             'AND/LOS/AM/AC/004', 2017, 'Generator', 'DIAKIN', 'C008594',
             'OBECHE SITTING ROOM', 'Tests', 'Quarterly', 'Warranty', 'ok',
             100000
         ]
     ])])

MOCK_AMITY_DATA = OrderedDict(
    [('AMITY 2.0',
      [[
          'SN', 'Code ID Ref.', 'Date of Purchase', 'Item description',
          'Name of Manufacturer',
          "Model/Series/Colour/Material and Manufacturer's Ref. no",
          'Location/Areas served', 'Maintenance period/History',
          'Operation Maintenance Instructions', 'Warranty/Guarantee data',
          'Condition', 'Other Relevant info', 'Initial cost'
      ],
       [
           '1', 'AND/LOS/AM/AC/001', 2017, '1HP Split Unit Air Conditioner',
           'DIAKIN', 'C009853', 'OBECHE ROOM 1', 'Test', 'Quarterly',
           'Warranty', 'Good', '', 100000
       ],
       [
           4, 'AND/LOS/AM/AC/004', 2017, 'Generator', 'DIAKIN', 'C008594',
           'OBECHE SITTING ROOM', 'Tests', 'Quarterly', 'Warranty', 'Good', '',
           100000
       ],
       [
           64, 'AND/LOS/AM/CH/0031-0032', 2017, 'Swivel Chair', 'LIFEMATE',
           'BLACK MESH', 'HACKSAW SITTING ROOM', 'Cleaning and Wiping down',
           'Weekly', 'Warranty', 'Good', '', '25,000'
       ]])])
MOCK_UNCLEAN_IT_DATA = OrderedDict(
    [('IT Devices',
      [['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
       [
           '', 'SN', 'Code ID Ref.', 'Date of Purchase', 'Item description',
           'Name of Manufacturer', 'Model',
           "Model/Series/Colour/Material and Manufacturer's Ref. no",
           'Location/Areas served', 'Maintenance period/History',
           'Operation Maintenance Instructions', 'Warranty/Guarantee data',
           'Condition', 'Router', 'Initial Cost'
       ],
       [
           '', '1', 'AND/LA/ET/IT/001', '', 'ET - appliance', '', 'MX100',
           'Q2JN-CJB7-DUQF', 'MX100', '', '', 'Warranty', '', '', ''
       ],
       [
           '', '2', 'AND/LA/ET/IT/002', '', 'ET - wireless', 'CISCO', 'MR18',
           'Q2GD-4EDB-WV9S', '4TH-RW-AP3', '', '', 'Warranty', 'Good',
           'Access Point', ''
       ],
       [
           '', '3', 'AND/LA/ET/IT/003', '', 'ET - wireless', 'CISCO', 'MR18',
           'Q2GD-4FCH-CVTX', '3RD-FLR-FATHOM', '', '', 'Warranty', 'Good',
           'Access Point', ''
       ],
       [
           '', '4'
           'AND/LA/ET/IT/004', '', 'ET - wireless', 'CISCO', 'MR18',
           'Q2GD-4FT8-SCU3', 'FLR5-RW-AP2', '', '', 'Warranty', 'Good',
           'Access Point', ''
       ]])])

MOCK_CLEAN_IT_DATA = OrderedDict([('IT Devices', [
    [
        'Tag', 'Date of Purchase', 'Item description', 'Name of Manufacturer',
        'Model', "Manufacturer's Ref. no", 'Assignee', 'Maintenance period',
        'Operation Maintenance Instructions', 'Warranty', 'Status', 'Router',
        'Initial Cost'
    ],
    [
        'AND/LA/ET/IT/001', '', 'ET - appliance', '', 'MX100',
        'Q2JN-CJB7-DUQF', 'MX100', '', '', 'Warranty', '', '', ''
    ],
    [
        'AND/LA/ET/IT/002', '', 'ET - wireless', 'CISCO', 'MR18',
        'Q2GD-4EDB-WV9S', '4TH-RW-AP3', '', '', 'Warranty', 'OK',
        'Access Point', ''
    ],
    [
        'AND/LA/ET/IT/003', '', 'ET - wireless', 'CISCO', 'MR18',
        'Q2GD-4FCH-CVTX', '3RD-FLR-FATHOM', '', '', 'Warranty', 'OK',
        'Access Point', ''
    ],
    [
        '', 'ET - wireless', 'CISCO', 'MR18', 'Q2GD-4FT8-SCU3', 'FLR5-RW-AP2',
        '', '', 'Warranty', 'OK', 'Access Point', '', ''
    ]
])])

DATA = [[
    '',
    'SN',
    'Tag',
    'warranty',
    'serial',
    'model',
    'Device',
    'Serial Number',
    'Location/Areas served',
    'Date Assigned',
    'Condition',
    '',
    're',
    '',
    'rem',
    'Extra Col',
],
        [
            '', 1, 'AND/TST/001', 'warranty', 'serial', 'model', 'Iphone 5C',
            'DX3V7JTYHG7A', 'RESERVE - OPS', '', 'ok', '', 'col', 'r', ''
        ],
        [
            '', 2, 'AND/TST/002-3', 'warranty', 'serial', 'model', 'Iphone 5C',
            'DX3V7JTYHG7B', 'RESERVE - OPS', '', 'ok', 'ol', '', '_col', ''
        ],
        [
            '', 3, 'AND/TST/T004-5', 'warranty', 'serial', 'model',
            'Iphone 5C', 'DX3V7JTYHG7C', 'RESERVE - OPS', '', 'ok', '', 'ol',
            'col', ''
        ], ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', 'SAFARI', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        [
            '', 5, 'AND/TST/0016', 'warranty', 'serial', 'model', 'Iphone 5C',
            'F72V514SHHG7D', 'OPS', '', 'bad status', '', '', '', ''
        ]]

CLEAN_DATA = {
    'ET WORKSTATIONS':
    [[
        'Tag', 'warranty', 'serial', 'model', 'Serial Number', 'Assignee',
        'Date Assigned', 'Status', '', 're', 'Extra Col', 'New Column'
    ],
     [
         'AND/TST/001', 'warranty', 'serial', 'model', 'DX3V7JTYHG7A',
         'RESERVE - OPS', '', 'ok', '', 'col'
     ],
     [
         'AND/TST/002', 'warranty', 'serial', 'model', 'DX3V7JTYHG7B',
         'RESERVE - OPS', '', 'ok', 'ol', ''
     ],
     [
         'AND/TST/003', 'warranty', 'serial', 'model', 'DX3V7JTYHG7B',
         'RESERVE - OPS', '', 'ok', 'ol', ''
     ],
     [
         'AND/TST/T/004', 'warranty', 'serial', 'model', 'DX3V7JTYHG7C',
         'RESERVE - OPS', '', 'ok', '', 'ol'
     ],
     [
         'AND/TST/T/005', 'warranty', 'serial', 'model', 'DX3V7JTYHG7C',
         'RESERVE - OPS', '', 'ok', '', 'ol'
     ],
     [
         'AND/TST/0016', 'warranty', 'serial', 'model', 'F72V514SHHG7D', 'OPS',
         '', 'bad status', '', ''
     ]]
}

UNCLEAN_JM1_BOOK_DATA = OrderedDict([('JM 1', [
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    [
        '',
        'SN',
        'Code ID Ref.',
        'Date of Purchase',
        'Item Description',
        'Quantity',
        'Name of Manufacturer',
        "Model/Series/Colour/Material and Manufacturer's Ref. no",
        'Initial location',
        'Areas served',
        'Maintenance period/History',
        'Operation Maintenance Instructions',
        'Warranty/Guarantee data',
        'Condition',
        'Other Relevant info',
        'Initial cost',
        'NBV Value',
    ],
    [
        '', 1, 'AND/LA/JMA/AC/001', 'September,2014',
        '1.5HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKC9NKH-3 / 2497313265 / White ', '2nd Floor', 'Ojuelegba',
        'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', 93750, 43750
    ],
    [
        '', 2, 'AND/LA/JMA/AC/002', 'September,2014',
        '1.5HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKCI8NKF-3 / 2497526043 / White ', '2nd Floor', 'Ajegunle',
        'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', '', ''
    ],
    [
        '', 3, 'AND/LA/JMA/AC/003', 'September,2014',
        '1.5HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKC9NKH-3 / 2497313379 / White ', '1st Floor', 'Victoria Island',
        'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', '', ''
    ],
    [
        '', 4, 'AND/LA/JMA/AC/004', 'September,2014',
        '1.5HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKC18NKF-3 / 2497312710/ White ', '1st Floor', 'Ikeja', 'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', '', ''
    ],
    [
        '', 5, 'AND/LA/JMA/AC/005', 'September,2014',
        '2 HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKC18NKF-3 / 2497525908 / White ', '1st Floor', 'Lobby', 'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', '', ''
    ],
    [
        '', 6, 'AND/LA/JMA/AC/006', 'September,2014',
        '1.5HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKC9NKH-3 / 2497313450 / White', 'Ground floor', 'Kitchen',
        'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', '', ''
    ],
    [
        '', 7, 'AND/LA/JMA/AC/007', 'September,2014',
        '1 HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKCN9KH-3 / 2497313459 / White ', 'Ground floor', 'Sitting room',
        'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', '', ''
    ],
    [
        '', 8, 'AND/LA/JMA/AC/008', 'September,2014',
        '1 HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKC9NKH-3 / 2497313117 / White', 'Ground floor', 'Sitting room',
        'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', '', ''
    ], ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    [
        '', '', '', '', 'EQUIPMENTS', '', '', '', '', '', '', '', '', '', '',
        '', ''
    ],
    [
        '', 1, 'AND/LA/JMA/F/01', '', 'Freezer', 1, 'SKY',
        'AZQ2085108B10133 / 3HH1400926 -03309 / White / Steel', 'Ground Floor',
        'Kitchen', 'Weekly', 'Washing and Cleaning', 'Warranty', 'Fair', '',
        '', 'Expense to P & L'
    ],
    [
        '', 2, 'AND/LA/JMA/FR/01', '', 'Fridge', 1, 'Nexus',
        'DF2-231/CNX / 114723G14200160 / Silver / Steel', 'Ground Floor',
        'Kitchen', 'Weekly', 'Washing and Cleaning', 'Warranty', 'OK', '', '',
        ''
    ],
    [
        '', 5, 'AND/LA/JMA/K/01-06', '', ' Kettle', 1, 'Essential',
        'FK-0901A-5 / 701614-5 / White / Plastic', 'Ground Floor', 'Kitchen',
        'Weekly', 'Washing and Cleaning', '', 'Fair', '', '', ''
    ],
    [
        '', 6, 'AND/LA/JMA/B/01', '', 'Blender', 1, 'Philips',
        'HR2161 / 120069-12/ White/ Plastic', 'Ground Floor', 'Kitchen',
        'Daily', 'Washing and Cleaning', 'Warranty', 'Fair', '', '', ''
    ],
    [
        '', 7, 'AND/LA/JMA/M/01', '', 'Microwave', 1, 'Nexus',
        '261831237754 / 04412701000223 / White / Steel', 'Ground Floor',
        'Kitchen', 'Daily', 'Washing and Cleaning', 'Warranty', 'Fair', '', '',
        ''
    ],
    [
        '', 8, 'AND/LA/JMA/WD/01', '', 'Water Dispenser', 1, 'Cway',
        'BY87514070567 / Silver/ Steel', 'Ground Floor', 'Sitting Room',
        'Daily', 'Washing and Cleaning', 'Warranty', 'OK', '', '', ''
    ],
    [
        '', 9, 'AND/LA/JMA/WF/01', '', 'Wall Fan', 1, 'TMT', '', '2nd Floor',
        'Ikorodu', 'Weekly', 'Cleaning and dusting ', 'Warranty', 'OK', '', '',
        ''
    ]
])])


UNCLEAN_JM1_BOOK_DATA2 = OrderedDict([('JM 1', [
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    [
        '',
        'SN',
        'Code ID Ref.',
        'Date of Purchase',
        'Item Description',
        'Quantity',
        'Name of Manufacturer',
        "Model/Series/Colour/Material and Manufacturer's Ref. no",
        'Initial location',
        'Areas served',
        'Maintenance period/History',
        'Operation Maintenance Instructions',
        'Warranty/Guarantee data',
        'Condition',
        'Other Relevant info',
        'Initial cost',
        'NBV Value',
    ],
    [
        '', 1, 'AND/LA/JMA/AC/001', 'September,2014',
        '1.5HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKC9NKH-3 / 2497313265 / White ', '2nd Floor', 'Ojuelegba',
        'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', 93750, 43750
    ],
    [
        '', 2, 'AND/LA/JMA/AC/002', 'September,2014',
        '1.5HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKCI8NKF-3 / 2497526043 / White ', '2nd Floor', 'Ajegunle',
        'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', '', ''
    ],
    [
        '', 3, 'AND/LA/JMA/AC/003', 'September,2014',
        '1.5HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKC9NKH-3 / 2497313379 / White ', '1st Floor', 'Victoria Island',
        'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', '', ''
    ],
    [
        '', 4, 'AND/LA/JMA/AC/004', 'September,2014',
        '1.5HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKC18NKF-3 / 2497312710/ White ', '1st Floor', 'Ikeja', 'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', '', ''
    ],
    [
        '', 5, 'AND/LA/JMA/AC/005', 'September,2014',
        '2 HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKC18NKF-3 / 2497525908 / White ', '1st Floor', 'Lobby', 'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', '', ''
    ],
    [
        '', 6, 'AND/LA/JMA/AC/006', 'September,2014',
        '1.5HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKC9NKH-3 / 2497313450 / White', 'Ground floor', 'Kitchen',
        'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', '', ''
    ],
    [
        '', 7, 'AND/LA/JMA/AC/007', 'September,2014',
        '1 HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKCN9KH-3 / 2497313459 / White ', 'Ground floor', 'Sitting room',
        'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', '', ''
    ],
    [
        '', 8, 'AND/LA/JMA/AC/008', 'September,2014',
        '1 HP Split Unit Air Conditional', 1, 'Panasonic',
        'CSKC9NKH-3 / 2497313117 / White', 'Ground floor', 'Sitting room',
        'Quarterly',
        'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
        'Warranty', 'OK', '', '', ''
    ], ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    [
        '', '', '', '', 'EQUIPMENTS', '', '', '', '', '', '', '', '', '', '',
        '', ''
    ],
    [
        '', 1, 'AND/LA/JMA/F/01', '', 'Freezer', 1, 'SKY',
        'AZQ2085108B10133 / 3HH1400926 -03309 / White / Steel', 'Ground Floor',
        'Kitchen', 'Weekly', 'Washing and Cleaning', 'Warranty', 'Fair', '',
        '', 'Expense to P & L'
    ],
    [
        '', 2, 'AND/LA/JMA/FR/01', '', 'Fridge', 1, 'Nexus',
        'DF2-231/CNX / 114723G14200160 / Silver / Steel', 'Ground Floor',
        'Kitchen', 'Weekly', 'Washing and Cleaning', 'Warranty', 'OK', '', '',
        ''
    ],
    [
        '', 5, 'AND/LA/JMA/K/01-06', '', ' Kettle', 1, 'Essential',
        'FK-0901A-5 / 701614-5 / White / Plastic', 'Ground Floor', 'Kitchen',
        'Weekly', 'Washing and Cleaning', '', 'Fair', '', '', ''
    ],
    [
        '', 6, 'AND/LA/JMA/B/01', '', 'Blender', 1, 'Philips',
        'HR2161 / 120069-12/ White/ Plastic', 'Ground Floor', 'Kitchen',
        'Daily', 'Washing and Cleaning', 'Warranty', 'Fair', '', '', ''
    ],
    [
        '', 7, 'AND/LA/JMA/M/01', '', 'Microwave', 1, 'Nexus',
        '261831237754 / 04412701000223 / White / Steel', 'Ground Floor',
        'Kitchen', 'Daily', 'Washing and Cleaning', 'Warranty', 'Fair', '', '',
        ''
    ],
    [
        '', 8, 'AND/LA/JMA/WD/01', '', 'Water Dispenser', 1, 'Cway',
        'BY87514070567 / Silver/ Steel', 'Ground Floor', 'Sitting Room',
        'Daily', 'Washing and Cleaning', 'Warranty', 'OK', '', '', ''
    ],
    [
        '', 9, 'AND/LA/JMA/WF/01', '', 'Wall Fan', 1, 'TMT', '', '2nd Floor',
        'Ikorodu', 'Weekly', 'Cleaning and dusting ', 'Warranty', 'OK', '', '',
        ''
    ]
])])

CLEAN_JM1_DATA = {
    'JM 1':
    [[
        'Tag', 'Date of Purchase', 'Item Description', 'Name of Manufacturer',
        "Manufacturer's Ref. no", 'Initial location', 'Assignee',
        'Maintenance period', 'Operation Maintenance Instructions', 'Warranty',
        'Status'
    ],
     [
         'AND/LA/JMA/AC/001', 'September,2014',
         '1.5HP Split Unit Air Conditional', 'Panasonic',
         'CSKC9NKH-3 / 2497313265 / White ', '2nd Floor', 'Ojuelegba',
         'Quarterly',
         'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
         'Warranty', 'OK'
     ],
     [
         'AND/LA/JMA/AC/002', 'September,2014',
         '1.5HP Split Unit Air Conditional', 'Panasonic',
         'CSKCI8NKF-3 / 2497526043 / White ', '2nd Floor', 'Ajegunle',
         'Quarterly',
         'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
         'Warranty', 'OK'
     ],
     [
         'AND/LA/JMA/AC/003', 'September,2014',
         '1.5HP Split Unit Air Conditional', 'Panasonic',
         'CSKC9NKH-3 / 2497313379 / White ', '1st Floor', 'Victoria Island',
         'Quarterly',
         'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
         'Warranty', 'OK'
     ],
     [
         'AND/LA/JMA/AC/004', 'September,2014',
         '1.5HP Split Unit Air Conditional', 'Panasonic',
         'CSKC18NKF-3 / 2497312710/ White ', '1st Floor', 'Ikeja', 'Quarterly',
         'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
         'Warranty', 'OK'
     ],
     [
         'AND/LA/JMA/AC/005', 'September,2014',
         '2 HP Split Unit Air Conditional', 'Panasonic',
         'CSKC18NKF-3 / 2497525908 / White ', '1st Floor', 'Lobby',
         'Quarterly',
         'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
         'Warranty', 'OK'
     ],
     [
         'AND/LA/JMA/AC/006', 'September,2014',
         '1.5HP Split Unit Air Conditional', 'Panasonic',
         'CSKC9NKH-3 / 2497313450 / White', 'Ground floor', 'Kitchen',
         'Quarterly',
         'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
         'Warranty', 'OK'
     ],
     [
         'AND/LA/JMA/AC/007', 'September,2014',
         '1 HP Split Unit Air Conditional', 'Panasonic',
         'CSKCN9KH-3 / 2497313459 / White ', 'Ground floor', 'Sitting room',
         'Quarterly',
         'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
         'Warranty', 'OK'
     ],
     [
         'AND/LA/JMA/AC/008', 'September,2014',
         '1 HP Split Unit Air Conditional', 'Panasonic',
         'CSKC9NKH-3 / 2497313117 / White', 'Ground floor', 'Sitting room',
         'Quarterly',
         'Cleaning of air fitter, Cleaning of triple filter, Use a soft, Dry cloth. Do not use use  bleach or abrasive.',
         'Warranty', 'OK'
     ], ['', '', '', '', '', '', '', '', '', '', ''],
     [
         'AND/LA/JMA/F/01', '', 'Freezer', 'SKY',
         'AZQ2085108B10133 / 3HH1400926 -03309 / White / Steel',
         'Ground Floor', 'Kitchen', 'Weekly', 'Washing and Cleaning',
         'Warranty', 'Fair'
     ],
     [
         'AND/LA/JMA/FR/01', '', 'Fridge', 'Nexus',
         'DF2-231/CNX / 114723G14200160 / Silver / Steel', 'Ground Floor',
         'Kitchen', 'Weekly', 'Washing and Cleaning', 'Warranty', 'OK'
     ],
     [
         'AND/LA/JMA/SM/01', '', 'Sandwich maker', '',
         'FS-40/ SSJ / 230VM50HZ/ White / steel', 'Ground Floor', 'Kitchen',
         'Daily', 'Washing and Cleaning', '', 'Fair'
     ],
     [
         'AND/LA/JMA/K/01', '', ' Kettle', 'Essential',
         'FK-0901A-5 / 701614-5 / White / Plastic', 'Ground Floor', 'Kitchen',
         'Weekly', 'Washing and Cleaning', '', 'Fair'
     ],
     [
         'AND/LA/JMA/B/01', '', 'Blender', 'Philips',
         'HR2161 / 120069-12/ White/ Plastic', 'Ground Floor', 'Kitchen',
         'Daily', 'Washing and Cleaning', 'Warranty', 'Fair'
     ],
     [
         'AND/LA/JMA/M/01', '', 'Microwave', 'Nexus',
         '261831237754 / 04412701000223 / White / Steel', 'Ground Floor',
         'Kitchen', 'Daily', 'Washing and Cleaning', 'Warranty', 'Fair'
     ],
     [
         'AND/LA/JMA/WD/01', '', 'Water Dispenser', 'Cway',
         'BY87514070567 / Silver/ Steel', 'Ground Floor', 'Sitting Room',
         'Daily', 'Washing and Cleaning', 'Warranty', 'OK'
     ],
     [
         'AND/LA/JMA/WF/01', '', 'Wall Fan', 'TMT', '', '2nd Floor', 'Ikorodu',
         'Weekly', 'Cleaning and dusting ', 'Warranty', 'OK'
     ]]
}
