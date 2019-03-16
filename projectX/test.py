from TagConfig import TagConfig, Identifier
import Sparkassenparser

def tag_config_test(csv_file, tc_file):
    if not csv_file or not tc_file:
        return

    tc = TagConfig()
    tc.add_category('Grundausgaben')
    tc.add_booking_type('Grundausgaben', 'Miete')
    tc.add_booking_type('Grundausgaben', 'Strom')
    i0 = Identifier('comment', 'MIETE')
    i1 = Identifier('from_to', 'Vattenfall')
    tc.add_identifier('Grundausgaben', 'Miete', i0)
    tc.add_identifier('Grundausgaben', 'Strom', i1)
    tc.save(tc_file)

    
    tc = TagConfig.from_file(tc_file)
    bookings = Sparkassenparser.parse_from_filename(csv_file)
    for b in bookings:
        r = tc.infer_category(b)
        if r['success']:
            print('Found category+booking:', r['r'],'for:', b)
        else:
            print(r['m'], b)