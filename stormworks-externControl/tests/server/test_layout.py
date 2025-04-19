import pytest
from xml.etree.ElementTree import Element
from unittest.mock import MagicMock
from stormworks_server.layout import Layout
from stormworks_server.elements import Component
from stormworks_server.elements.utils import Position

@pytest.fixture
def mock_component():
    component = MagicMock(spec=Component)
    component.position = MagicMock(spec=Position)
    component.position.x = 0
    component.position.y = 0
    component.position.width = 10
    component.position.height = 10
    component.html.return_value = (Element('div'), '.component { }')
    return component

def test_layout_initialization(mock_component):
    layout = Layout([mock_component])
    assert layout._width == 9
    assert layout._height == 9

def test_layout_html(mock_component, tmp_path):
    layout = Layout([mock_component])
    template_path = tmp_path / "template.html"
    template_content = "<html><head><style>{{style}}</style></head><body>{{buttons}}</body></html>"
    
    with open(template_path, "w") as f:
        f.write(template_content)
    
    html_output = layout.html(str(template_path))
    
    assert "<style>.container {" in html_output
    assert "grid-template-columns: repeat(9, 1fr);" in html_output
    assert "grid-template-rows: repeat(9, 1fr);" in html_output
    assert "<div" in html_output

def test_layout_html_template_not_found(mock_component):
    layout = Layout([mock_component])
    with pytest.raises(FileNotFoundError):
        layout.html("non_existent_template.html")

