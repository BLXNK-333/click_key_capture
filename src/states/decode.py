# Палка в жопу.

decode_map = {
    # DIGIT PUNC
    33: {'ru': {'lower': "1", 'upper': "!"},
         'us': {'lower': "1", 'upper': "!"}},
    34: {'ru': {'lower': "2", 'upper': "\""},
         'us': {'lower': "2", 'upper': "@"}},
    37: {'ru': {'lower': "5", 'upper': "%"},
         'us': {'lower': "5", 'upper': "%"}},
    39: {'ru': {'lower': "э", 'upper': "Э"},
         'us': {'lower': "\'", 'upper': "\""}},
    40: {'ru': {'lower': "9", 'upper': "("},
         'us': {'lower': "9", 'upper': "("}},
    41: {'ru': {'lower': "0", 'upper': ")"},
         'us': {'lower': "0", 'upper': ")"}},
    42: {'ru': {'lower': "8", 'upper': "*"},
         'us': {'lower': "8", 'upper': "*"}},
    43: {'ru': {'lower': "=", 'upper': "+"},
         'us': {'lower': "=", 'upper': "+"}},
    44: {'ru': {'lower': "б", 'upper': ","},
         'us': {'lower': ",", 'upper': "?"}},
    45: {'ru': {'lower': "-", 'upper': "_"},
         'us': {'lower': "-", 'upper': "_"}},
    46: {'ru': {'lower': "ю", 'upper': "Ю"},
         'us': {'lower': ".", 'upper': ">"}},
    47: {'ru': {'lower': ".", 'upper': "/"},
         'us': {'lower': "/", 'upper': "?"}},
    48: {'ru': {'lower': "0", 'upper': ")"},
         'us': {'lower': "0", 'upper': ")"}},
    49: {'ru': {'lower': "1", 'upper': "!"},
         'us': {'lower': "1", 'upper': "!"}},
    50: {'ru': {'lower': "2", 'upper': "\""},
         'us': {'lower': "2", 'upper': "@"}},
    51: {'ru': {'lower': "3", 'upper': "№"},
         'us': {'lower': "3", 'upper': "#"}},
    52: {'ru': {'lower': "4", 'upper': ";"},
         'us': {'lower': "4", 'upper': "$"}},
    53: {'ru': {'lower': "5", 'upper': "%"},
         'us': {'lower': "5", 'upper': "%"}},
    54: {'ru': {'lower': "6", 'upper': ":"},
         'us': {'lower': "6", 'upper': "^"}},
    55: {'ru': {'lower': "7", 'upper': "?"},
         'us': {'lower': "7", 'upper': "&"}},
    56: {'ru': {'lower': "8", 'upper': "*"},
         'us': {'lower': "8", 'upper': "*"}},
    57: {'ru': {'lower': "9", 'upper': "("},
         'us': {'lower': "9", 'upper': "("}},
    58: {'ru': {'lower': "6", 'upper': ":"},
         'us': {'lower': "6", 'upper': "^"}},
    59: {'ru': {'lower': "ж", 'upper': ";"},
         'us': {'lower': ";", 'upper': "$"}},
    61: {'ru': {'lower': "=", 'upper': "+"},
         'us': {'lower': "=", 'upper': "+"}},
    63: {'ru': {'lower': "7", 'upper': "?"},
         'us': {'lower': "7", 'upper': "&"}},
    91: {'ru': {'lower': "х", 'upper': "Х"},
         'us': {'lower': "[", 'upper': "{"}},
    92: {'ru': {'lower': "\\", 'upper': "/"},
         'us': {'lower': "\\", 'upper': "|"}},
    93: {'ru': {'lower': "ъ", 'upper': "Ъ"},
         'us': {'lower': "]", 'upper': "}"}},
    95: {'ru': {'lower': "-", 'upper': "_"},
         'us': {'lower': "-", 'upper': "_"}},

    # LOWER
    96: {'ru': {'lower': "ё", 'upper': "Ё"},
         'us': {'lower': "`", 'upper': "~"}},
    97: {'ru': {'lower': "ф", 'upper': "Ф"},
         'us': {'lower': "a", 'upper': "A"}},
    98: {'ru': {'lower': "и", 'upper': "И"},
         'us': {'lower': "b", 'upper': "B"}},
    99: {'ru': {'lower': "с", 'upper': "С"},
         'us': {'lower': "c", 'upper': "C"}},
    100: {'ru': {'lower': "в", 'upper': "В"},
          'us': {'lower': "d", 'upper': "D"}},
    101: {'ru': {'lower': "у", 'upper': "У"},
          'us': {'lower': "e", 'upper': "E"}},
    102: {'ru': {'lower': "а", 'upper': "А"},
          'us': {'lower': "f", 'upper': "F"}},
    103: {'ru': {'lower': "п", 'upper': "П"},
          'us': {'lower': "g", 'upper': "G"}},
    104: {'ru': {'lower': "р", 'upper': "Р"},
          'us': {'lower': "h", 'upper': "H"}},
    105: {'ru': {'lower': "ш", 'upper': "Ш"},
          'us': {'lower': "i", 'upper': "I"}},
    106: {'ru': {'lower': "о", 'upper': "О"},
          'us': {'lower': "j", 'upper': "J"}},
    107: {'ru': {'lower': "л", 'upper': "Л"},
          'us': {'lower': "k", 'upper': "K"}},
    108: {'ru': {'lower': "д", 'upper': "Д"},
          'us': {'lower': "l", 'upper': "L"}},
    109: {'ru': {'lower': "ь", 'upper': "Ь"},
          'us': {'lower': "m", 'upper': "M"}},
    110: {'ru': {'lower': "т", 'upper': "Т"},
          'us': {'lower': "n", 'upper': "N"}},
    111: {'ru': {'lower': "щ", 'upper': "Щ"},
          'us': {'lower': "o", 'upper': "O"}},
    112: {'ru': {'lower': "з", 'upper': "З"},
          'us': {'lower': "p", 'upper': "P"}},
    113: {'ru': {'lower': "й", 'upper': "Й"},
          'us': {'lower': "q", 'upper': "Q"}},
    114: {'ru': {'lower': "к", 'upper': "К"},
          'us': {'lower': "r", 'upper': "R"}},
    115: {'ru': {'lower': "ы", 'upper': "Ы"},
          'us': {'lower': "s", 'upper': "S"}},
    116: {'ru': {'lower': "е", 'upper': "Е"},
          'us': {'lower': "t", 'upper': "T"}},
    117: {'ru': {'lower': "г", 'upper': "Г"},
          'us': {'lower': "u", 'upper': "U"}},
    118: {'ru': {'lower': "м", 'upper': "М"},
          'us': {'lower': "v", 'upper': "V"}},
    119: {'ru': {'lower': "ц", 'upper': "Ц"},
          'us': {'lower': "w", 'upper': "W"}},
    120: {'ru': {'lower': "ч", 'upper': "Ч"},
          'us': {'lower': "x", 'upper': "X"}},
    121: {'ru': {'lower': "н", 'upper': "Н"},
          'us': {'lower': "y", 'upper': "Y"}},
    122: {'ru': {'lower': "я", 'upper': "Я"},
          'us': {'lower': "z", 'upper': "Z"}},

    # UPPER
    1712: {'ru': {'lower': "3", 'upper': "№"},
           'us': {'lower': "3", 'upper': "#"}},
    1715: {'ru': {'lower': "ё", 'upper': "Ё"},
           'us': {'lower': "`", 'upper': "~"}},
    1760: {'ru': {'lower': "ю", 'upper': "Ю"},
           'us': {'lower': ">", 'upper': ">"}},
    1761: {'ru': {'lower': "а", 'upper': "А"},
           'us': {'lower': "f", 'upper': "F"}},
    1762: {'ru': {'lower': "б", 'upper': "Б"},
           'us': {'lower': "<", 'upper': "<"}},
    1763: {'ru': {'lower': "ц", 'upper': "Ц"},
           'us': {'lower': "w", 'upper': "W"}},
    1764: {'ru': {'lower': "д", 'upper': "Д"},
           'us': {'lower': "l", 'upper': "L"}},
    1765: {'ru': {'lower': "е", 'upper': "Е"},
           'us': {'lower': "t", 'upper': "T"}},
    1766: {'ru': {'lower': "ф", 'upper': "Ф"},
           'us': {'lower': "a", 'upper': "A"}},
    1767: {'ru': {'lower': "г", 'upper': "Г"},
           'us': {'lower': "u", 'upper': "U"}},
    1768: {'ru': {'lower': "х", 'upper': "Х"},
           'us': {'lower': "[", 'upper': "{"}},
    1769: {'ru': {'lower': "и", 'upper': "И"},
           'us': {'lower': "b", 'upper': "B"}},
    1770: {'ru': {'lower': "й", 'upper': "Й"},
           'us': {'lower': "q", 'upper': "Q"}},
    1771: {'ru': {'lower': "к", 'upper': "К"},
           'us': {'lower': "r", 'upper': "R"}},
    1772: {'ru': {'lower': "л", 'upper': "Л"},
           'us': {'lower': "k", 'upper': "K"}},
    1773: {'ru': {'lower': "м", 'upper': "М"},
           'us': {'lower': "v", 'upper': "V"}},
    1774: {'ru': {'lower': "н", 'upper': "Н"},
           'us': {'lower': "y", 'upper': "Y"}},
    1775: {'ru': {'lower': "о", 'upper': "О"},
           'us': {'lower': "j", 'upper': "J"}},
    1776: {'ru': {'lower': "п", 'upper': "П"},
           'us': {'lower': "g", 'upper': "G"}},
    1777: {'ru': {'lower': "я", 'upper': "Я"},
           'us': {'lower': "z", 'upper': "Z"}},
    1778: {'ru': {'lower': "р", 'upper': "Р"},
           'us': {'lower': "h", 'upper': "H"}},
    1779: {'ru': {'lower': "с", 'upper': "С"},
           'us': {'lower': "c", 'upper': "C"}},
    1780: {'ru': {'lower': "т", 'upper': "Т"},
           'us': {'lower': "n", 'upper': "N"}},
    1781: {'ru': {'lower': "у", 'upper': "У"},
           'us': {'lower': "e", 'upper': "E"}},
    1782: {'ru': {'lower': "ж", 'upper': "Ж"},
           'us': {'lower': ";", 'upper': ":"}},
    1783: {'ru': {'lower': "в", 'upper': "В"},
           'us': {'lower': "d", 'upper': "D"}},
    1784: {'ru': {'lower': "ь", 'upper': "Ь"},
           'us': {'lower': "m", 'upper': "M"}},
    1785: {'ru': {'lower': "ы", 'upper': "Ы"},
           'us': {'lower': "s", 'upper': "S"}},
    1786: {'ru': {'lower': "з", 'upper': "З"},
           'us': {'lower': "p", 'upper': "P"}},
    1787: {'ru': {'lower': "ш", 'upper': "Ш"},
           'us': {'lower': "i", 'upper': "I"}},
    1788: {'ru': {'lower': "э", 'upper': "Э"},
           'us': {'lower': "\'", 'upper': "\""}},
    1789: {'ru': {'lower': "щ", 'upper': "Щ"},
           'us': {'lower': "o", 'upper': "O"}},
    1790: {'ru': {'lower': "ч", 'upper': "Ч"},
           'us': {'lower': "x", 'upper': "X"}},
    1791: {'ru': {'lower': "ъ", 'upper': "Ъ"},
           'us': {'lower': "]", 'upper': "}"}}
}
