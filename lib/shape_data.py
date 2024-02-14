from typing import Any
from OCCT.AIS import AIS_Shape
from OCCT.TopoDS import TopoDS_Shape
from OCCT.BRepBuilderAPI import BRepBuilderAPI_MakeShape
from OCCT.Display.qtDisplay import qtViewer3d
import logging
import ujson as json
from typing import Union

SUPPORT_TYPE = Union[AIS_Shape, TopoDS_Shape, BRepBuilderAPI_MakeShape]

class shape_item(): # Just for type hint
    pass

class main_datas():
    def __init__(self, canva:qtViewer3d) -> None:
        self.shapes: dict[str, shape_item] = {}
        self.canva = canva

    def add_shape(self, shape: Union[SUPPORT_TYPE, shape_item], name: str):
        if isinstance(shape, shape_item):
            self.shapes[name] = shape
        else:
            self.shapes[name] = shape_item(shape, self)

        self.canva._display.DisplayShape(self.shapes[name].ais_shape, update=True)

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

    def export_to_list(self) -> list[TopoDS_Shape]:
        return [i.shape_data for i in self.shapes.values()]

class shape_item():
    def __init__(self, shape: SUPPORT_TYPE, parent: main_datas = None) -> None:

        self.child_shape: dict[str, shape_item] = {}
        self.parent: main_datas = parent
        self.shape_data: TopoDS_Shape = None

        if isinstance(shape, AIS_Shape):
            super().__setattr__('shape_data', shape.Shape()) # self.shape_data:TopoDS_Shape = shape.Shape()
            self.ais_shape: AIS_Shape = shape
        else:
            if isinstance(shape, TopoDS_Shape):
                super().__setattr__('shape_data', shape) # self.shape_data:TopoDS_Shape = shape
            if isinstance(shape, BRepBuilderAPI_MakeShape):
                super().__setattr__('shape_data', shape.Shape()) # self.shape_data:TopoDS_Shape = shape.Shape()
            self.ais_shape: AIS_Shape = AIS_Shape(self.shape_data)
                
    def update_shape(self):
        '''
            You don't need to run this function, it will be called automatically. (When you set shape_data)
            Run this function when you replace shape_data.
            This function will update ais_shape. And if you set parent, it will also update view(parent.canva.display.Context.Redisplay).
        '''
        self.ais_shape.SetShape(self.shape_data)

        if self.parent is not None:
            self.parent.canva._display.Context.Redisplay(self.ais_shape, True)

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if __name == 'shape_data' and __value is not None:
            self.update_shape()

    def export_to_json(self) -> dict:
        '''
            Export shape data (including child shape) to json
            The json should be like:
                {
                    'data': {
                        (OCC shape data...)
                    },
                    'children': {
                        'Child Box': {
                            'data': {
                                (OCC shape data...)
                            },
                            'children': {
                                (child's child shape data...)
                            }
                        },
                        (Other children shape data...)
                    }
                }
        '''
        res = {}
        res['data'] = self.shape_data
        res['children'] = {}
        for key, value in self.child_shape.items():
            res['children'][key] = value.export_to_json()
        return res
        

def load_from_json(canva, json_data: dict[str, str]) -> main_datas:
    res = main_datas(canva)
    for name, json_shape in json_data.items():
        res.add_shape(TopoDS_Shape(), name)