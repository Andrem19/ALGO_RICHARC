import helpers.profit as pr
import shared_vars as sv
import helpers.util as util
import coins

deals = [{"type_of_signal": "ham_60c"}, {"type_of_signal": "ham_60c"}, {"type_of_signal": "ham_60cc"}, {"type_of_signal": "ham_1b"}, {"type_of_signal": "ham_60cc"}, {"type_of_signal": "ham_60c"}]


deals.sort(key=lambda d: ('ham_60cc' == d["type_of_signal"], 'ham_60c' == d["type_of_signal"], 'ham_1b' in d["type_of_signal"]))

print(deals)