import re
import pytest
from pyap import utils
from pyap.packages import six
import pyap.source_NA_STREET.data as data_ns


def execute_matching_test(input, expected, pattern):
    match = utils.match(pattern, input, re.VERBOSE)
    is_found = match is not None
    if expected:
        assert is_found == expected and match.group(0) == input
    else:
        """we check that:
           - input should not to match our regex
           - our match should be partial if regex matches some part of string
        """
        assert (is_found == expected) or (match.group(0) != input)

@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("ZERO ", True),
    ("one ", True),
    ("two ", True),
    ("Three ", True),
    ("FoUr ", True),
    ("FivE ", True),
    ("six ", True),
    ("SEvEn ", True),
    ("Eight ", True),
    ("Nine ", True),
    # negative assertions
    ("Nidnes ", False),
    ("One.", False),
    ("two.", False),
    ("onetwothree ", False),
])
def test_zero_to_nine(input, expected):
    ''' test string match for zero_to_nine '''
    execute_matching_test(input, expected, data_ns.zero_to_nine)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("tEN ", True),
    ("TWENTY ", True),
    ("tHirtY ", True),
    ("FOUrty ", True),
    ("fifty ", True),
    ("sixty ", True),
    ("seventy ", True),
    ("eighty ", True),
    ("NINety ", True),
    # negative assertions
    ("ten.", False),
    ("twenTY.", False),
    ("sixtysixsty ", False),
    ("one twenty ", False),
])
def test_ten_to_ninety(input, expected):
    ''' test string match for ten_to_ninety '''
    execute_matching_test(input, expected, data_ns.ten_to_ninety)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Hundred ", True),
    ("HuNdred ", True),
    # negative assertions
    ("HuNDdred.", False),
    ("HuNDdred hundred ", False),
])
def test_hundred(input, expected):
    ''' tests string match for a hundred '''
    execute_matching_test(input, expected, data_ns.hundred)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Thousand ", True),
    ("thOUSAnd ", True),
    # negative assertions
    ("thousand.", False),
    ("THoussand ", False),
    ("THoussand", False),
    ("THOUssand THoussand ", False),
])
def test_thousand(input, expected):
    ''' tests string match for a thousand '''
    execute_matching_test(input, expected, data_ns.thousand)


@pytest.mark.parametrize("input,expected", [
    # positive assertions (words)
    ("One Thousand And Fifty Nine ", True),
    ("Two hundred and fifty ", True),
    ("Three hundred four ", True),
    ("Thirty seven ", True),
    ("FIFTY One ", True),
    ("Three hundred Ten ", True),
    # positive assertions (numbers)
    ("1", True),
    ("15", True),
    ("44", True),
    ("256", True),
    ("256", True),
    ("1256", True),
    ("32457", True),
    # negative assertions (words)
    ("ONE THousszz22and FIFTY and four onde", False),
    ("ONE one oNe and onE Three", False),
    # negative assertions (numbers)
    ("536233 ", False),
    ("111111 ", False),
    ("1111ss11", False),
    ("123 456", False),
])
def test_street_number(input, expected):
    ''' tests string match for a street number '''
    execute_matching_test(input, expected, data_ns.street_number)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Northeast Kentucky Industrial ", True),
    ("One ", True),
    ("First ", True),
    ("Ave 123 ", True),
    ("Northeast 5 ", True),
    ("a", True),
    ("ab", True),
    # negative assertions
    ("Northeast Kentucky Industrial Maple ", False),
    ("", False),
])
def test_street_name(input, expected):
    ''' tests positive string match for a street name '''
    execute_matching_test(input, expected, data_ns.street_name)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("N.", True),
    ("N", True),
    ("S", True),
    ("West ", True),
    ("eASt ", True),
    ("NW", True),
    ("SE", True),
    ("NW.", True),
    ("N.O.", True),
    # negative assertions
    ("NS ", False),
    ("EW ", False),
])
def test_post_direction(input, expected):
    ''' tests string match for a post_direction '''
    execute_matching_test(input, expected, data_ns.post_direction)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Street ", True),
    ("St. ", True),
    ("St.", True),
    ("Blvd.", True),
    ("Blvd. ", True),
    ("LN ", True),
    ("RD", True),
    ("Cir", True),
    ("Highway ", True),
    ("Hwy ", True),
    ("Ct", True),
    ("Sq.", True),
    ("LP. ", True),
    ("LP. (Route A1 )", True),
    ("Street route 5 ", True),
    ("Ctr", True),
    ("blvd", True),
    ("Estate", True),
    ("Manor", True),
    # negative assertions
    # TODO

])
def test_street_type(input, expected):
    ''' tests string match for a street id '''
    execute_matching_test(input, expected, data_ns.street_type)

@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("OH-34", True),
    ("CoUnty RoAd 19", True),
    ("US HwY 999", True),
    ("Highway 12", True),
    ("us rouTE 2", True),
])
def test_special_streets(input, expected):
    ''' tests string match for special road types'''
    execute_matching_test(input, expected, data_ns.special_streets)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("floor 3 ", True),
    ("floor 11 ", True),
    ("floor 15 ", True),
    ("1st floor ", True),
    ("2nd floor ", True),
    ("15th floor ", True),
    ("16th. floor ", True),
    # negative assertions
    ("16th.floor ", False),
    ("1stfloor ", False),

])
def test_floor(input, expected):
    ''' tests string match for a floor '''
    execute_matching_test(input, expected, data_ns.floor)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("bldg m ", True),
    ("Building F ", True),
    ("bldg 2 ", True),
    ("building 3 ", True),
    ("building 100 ", True),
    ("building 1000 ", True),
    ("Building ", True),
    ("building one ", True),
    ("Building three ", True),
    # negative assertions
    ("bldg", False),
    ("bldgm", False),
    ("bldg100 ", False),
    ("building 10000 ", False),

])
def test_building(input, expected):
    ''' tests string match for a building '''
    execute_matching_test(input, expected, data_ns.building)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("suite 900 ", True),
    ("Suite #2 ", True),
    ("suite #218 ", True),
    ("suite J7 ", True),
    ("suite 102A ", True),
    ("suite a&b ", True),
    ("Suite J#200 ", True),
    ("suite 710-327 ", True),
    ("Suite A ", True),
    ("ste A ", True),
    ("Ste 101 ", True),
    ("ste 502b ", True),
    ("ste 14-15 ", True),
    ("ste E ", True),
    ("ste 9E ", True),
    ("Suite 1800 ", True),
    ("Apt 1B ", True),
    ("Rm. 52 ", True),
    ("#2b ", True),
    # negative assertions
    ("suite900 ", False),
    ("Suite#2", False),
    ("suite218 ", False),
])
def test_occupancy(input, expected):
    ''' tests string match for a place id '''
    execute_matching_test(input, expected, data_ns.occupancy)

@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("Suite 40 Big Hall", True),
    ("Rm A300 Pine haLl", True),
    # negative assertions
    ("Rm A300 Pine center", False),
])
def test_dorm(input, expected):
    ''' tests string match for a dorm'''
    execute_matching_test(input, expected, data_ns.dorm)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("po box 108", True),
    ("Po Box 53485", True),
    ("P.O. box 119", True),
    ("PO box 1070", True),
    # negative assertions
    ("po box108 ", False),
    ("PoBox53485 ", False),
    ("P.O. box119", False),
    ("POb ox1070 ", False),
])
def test_po_box_positive(input, expected):
    ''' tests exact string match for a po box '''
    execute_matching_test(input, expected, data_ns.po_box)


@pytest.mark.parametrize("input,expected", [
    # positive assertions
    ("9652 Loiret Boulevard", True),
    ("101 MacIntosh Boulevard", True),
    ("1 West Hegeler Lane", True),
    ("1270 Leeds Avenue", True),
    ("85-1190 Ranchview Rd. NW", True),
    ("62 Portland Road (Route 1)", True),
    ("200 N. Pine Avenue Suite 514 ", True),
    ("200 S. Alloy Drive", True),
    ("Two Hundred S. Alloy Drive", True),
    ("Two Hundred South Alloy Drive", True),
    ("Two Hundred South Alloy Dr.", True),
    ("11001 Fondren Rd,", True),
    ("9606 North Mopac Expressway Suite 500 ", True),
    ("9692 East Arapahoe Road,", True),
    ("9 Grand Avenue, Suite 2 ", True),
    ("9 Grand Avenue Building 2, Suite 2,", True),
    ("9 Grand Avenue Building 2, Suite 2A,", True),
    ("233 Richmond Highway Suite 1800 ", True),
    ("354 Eisenhower Parkway P.O. Box 472,", True),
    ("6645 N Ensign St", True),
    ("1200 Old Fairhaven Pkwy Apt 106,", True),
    ("1659 Scott Blvd Ste 26,", True),
    ("377 Fisher Rd Ste C", True),
    ("1833 Stearman Ave", True),
    ("1737 S Lumpkin St Ste B,", True),
    ("101 N Court Sq Ste 16,", True),
    ("1790 Yardley Langhorne Rd, Suite #205,", True),
    ("280 West Main Street", True),
    ("701 Tennessee Walk", True),
    ("7457 Harwin Dr", True),
    ("700 Davis Avenue", True),
    ("1 W 47th St", True),
    ("832 Seward St", True),
    ("2740 Timber Ridge Lane", True),
    ("810 E Western Ave", True),
    ("6223 Richmond Ave Ste 105,", True),
    ("400 Middle Street", True),
    ("81 N Main St", True),
    ("3705 West Memorial Road", True),
    ("4911 Matterhorn Dr", True),
    ("5830 Yahl Street, #2b,", True),
    ("9400 Doliver Dr Apt 13,", True),
    ("10701 Stirling Road", True),
    ("1865 Corporate Dr Ste 225,", True),
    ("80 Beaman Rd", True),
    ("9691 Spratley Ave", True),
    ("10835 New Haven Rd NW ", True),
    ("320 W Broussard Rd", True),
    ("9001 Any Old Way", True),
    ("8967 Market St.", True),
    ("3724 Oxford Blvd.", True),
    ("901 Rainier Ave S ", True),
])
def test_full_street_positive(input, expected):
    ''' tests exact string match for a full street '''
    execute_matching_test(input, expected, data_ns.full_street)