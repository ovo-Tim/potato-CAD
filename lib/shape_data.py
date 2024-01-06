from typing import Any
from OCC.Core.AIS import AIS_Shape
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeShape
from ..lib.occ_page import potaoViewer
import logging
import ujson as json

SUPPORT_TYPE = AIS_Shape|TopoDS_Shape|BRepBuilderAPI_MakeShape

class shape_item
class main_datas

class main_datas():
    def __init__(self, canva) -> None:
        self.shapes: dict[str, shape_item] = {}
        self.canva: potaoViewer = canva

    def add_shape(self, shape: SUPPORT_TYPE|shape_item, name: str, display=True):
        if isinstance(shape, shape_item):
            self.shapes[name] = shape
        else:
            self.shapes[name] = shape_item(shape, self)
        if display:
            self.canva.display.DisplayShape(self.shapes[name].ais_shape, True)

    def update_display(self, name: str):
        '''
            Please run this function when you change shape_data.
            This function will update display by running display.Context.Redisplay.
        '''
        self.canva.display.Context.Redisplay(self.shapes[name].ais_shape, True)

    def export_to_json(self) -> dict:
        res = {}
        for key, value in self.shapes.items():
            res[key] = value.export_to_json()
        return res

class shape_item():
    def __init__(self, shape: SUPPORT_TYPE, parent: main_datas = None) -> None:
        self.shape_data: SUPPORT_TYPE = shape
        self.child_shape: dict[str, shape_item] = {}
        self.parent: main_datas = parent
        
    def TopoDS_Shape(self) -> TopoDS_Shape:
        if isinstance(self.shape_data, AIS_Shape):
            return self.shape_data.Shape()
        elif isinstance(self.shape_data, TopoDS_Shape):
            return self.shape_data
        elif isinstance(self.shape_data, BRepBuilderAPI_MakeShape):
            return self.shape_data.Shape()
        
    def update_shape(self):
        '''
            You don't need to run this function, it will be called automatically. (When you set shape_data)
            Run this function when you replace shape_data.
            This function will update ais_shape. And if you set parent, it will also update view(parent.canva.display.Context.Redisplay).
        '''
        if isinstance(self.shape_data, AIS_Shape):
            self.ais_shape: AIS_Shape = self.shape_data
        else:
            self.ais_shape = AIS_Shape(self.TopoDS_Shape())

        if self.parent is not None:
            self.parent.canva.display.Context.Redisplay(self.ais_shape, True)

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if __name == 'shape_data':
            self.update_ais_shape()

    def export_to_json(self) -> dict:
        '''
            Export shape data (including child shape) to json
            The json should be like:
                {
                    'data': {
                        (OCC shape data...)
                    },
                    'childen': {
                        'Child Box': {
                            'data': {
                                (OCC shape data...)
                            },
                            'childen': {
                                (child's child shape data...)
                            }
                        },
                        (Other childen shape data...)
                    }
                }
        '''
        res = {}
        res['data'] = json.loads(self.TopoDS_Shape().DumpJsonToString())
        res['childen'] = {}
        for key, value in self.child_shape.items():
            res['childen'][key] = value.export_to_json()
        return res
        

        