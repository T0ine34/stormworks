from stormworks_server.elements.utils import getColorVariants, getIcon, isCustomIcon, Position, Channel, Input
from stormworks_server.colors import Color
import pytest
from xml.etree.ElementTree import Element, fromstring

def test_getColorVariants():
    assert getColorVariants(Color(255, 255, 255, 255)) == {
        "oppositeBW": Color(0, 0, 0, 255),
        "dark": Color(223, 223, 223, 255),
        "darkOppositeBW": Color(0, 0, 0, 255)
    }
    assert getColorVariants(Color(0, 0, 0, 255)) == {
        "oppositeBW": Color(255, 255, 255, 255),
        "dark": Color(0, 0, 0, 255),
        "darkOppositeBW": Color(255, 255, 255, 255)
    }
    assert getColorVariants(Color(128, 128, 128, 255)) == {
        "oppositeBW": Color(0, 0, 0, 255),
        "dark": Color(96, 96, 96, 255),
        "darkOppositeBW": Color(0, 0, 0, 255)
    }
    
def test_getIcon():
    pod = fromstring("""<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <path d="M 75 45 C 75 10, 85 -10, 85 50" stroke-width="4" fill="none"/>
    <path d="M 75 55 C 75 90, 85 110, 85 50" stroke-width="4" fill="none"/>
    <path d="M 70 65 L 60 65 C 40 65, 20 60, 10 50 C 20 40, 40 35, 60 35 L 70 35" stroke-width="4" fill="none"/>
    <path d="M 70 45 C 75 45, 90 45, 90 50 C 90 55, 75 55, 70 55" stroke-width="4" />
    <circle cx="70" cy="65" r="2" stroke="none"/>
    <circle cx="70" cy="35" r="2" stroke="none"/>
    <circle cx="60" cy="65" r="2" stroke="none"/>
    <circle cx="60" cy="35" r="2" stroke="none"/>
    <line x1="70" y1="65" x2="70" y2="35" stroke-width="4"/>
</svg>
""")
    
    icon = getIcon("pod")
    assert icon.tag == pod.tag
    assert icon.attrib == pod.attrib
    assert icon.text == pod.text
    assert icon.tail == pod.tail

    with pytest.raises(FileNotFoundError):
        getIcon("nonexistenticon")