

dict_parse = [{'type_of_signal': 'ham_1bz'}, {'type_of_signal': 'ham_1a'}, {'type_of_signal': 'ham_1bz'}, {'type_of_signal': 'ham_1aa'},{'type_of_signal': 'ham_1aa'}]

dict_parse.sort(key=lambda d: ('ham_1b' in d["type_of_signal"], 'ham_1aa' in d["type_of_signal"],))
print(dict_parse)