import griffe
from caqtus.device.camera import CameraConfiguration
import inspect

s = inspect.getdoc(CameraConfiguration)
doc = griffe.Docstring(s)


def auto_parse(doc: griffe.Docstring) -> None:
    griffe.parse_google(doc)
    griffe.parse_numpy(doc)
    griffe.parse_sphinx(doc)


for section in griffe.parse_google(doc):
    print(section)
