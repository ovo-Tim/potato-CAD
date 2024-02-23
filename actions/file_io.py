from OCCT.Extend.DataExchange import write_step_file, write_iges_file, write_brep_file
import logging

from OCCT.Extend.DataExchange import read_step_file, read_iges_file, read_stl_file
from OCCT.Extend.TopologyUtils import TopologyExplorer 
from OCCT.BRepTools import BRepTools
from OCCT.TopoDS import TopoDS_Shape
from OCCT.BRep import BRep_Builder
from OCCT.TopoDS import  TopoDS_Shape
# from OCCT.Standard import Standard_OS

from lib import shape_data
from zipfile import ZipFile
import ujson as json
import tempfile, os
from typing import Union

def export(path:str, shapes:list):
    suffix = path.split('.')[-1].lower()

    if suffix == 'brep':
        write_brep_file(shapes, path)
    elif suffix == 'step':
        write_step_file(shapes, path)
    elif suffix == 'iges':
        write_iges_file(shapes, path)
    else:
        logging.error(f"Not supported {suffix}.Stop exporting.")

def import_shap(path:str) -> Union[TopoDS_Shape,list[TopoDS_Shape]]:
    logging.info("Load file:" + path)
    suffix = path.split('.')[-1].lower()

    if suffix == 'brep':
        logging.info("Found BREP,loading")
        mod_file = TopoDS_Shape()
        builder = BRep_Builder()
        BRepTools.Read_(mod_file, path, builder)

    elif suffix == 'step':
        logging.info("Found STEP, loading")
        mod_file = read_step_file(path, as_compound=False)
    elif suffix == 'iges':
        logging.info("Found IGES, loading")
        mod_file = read_iges_file(path, return_as_shapes=True)
    elif suffix == 'stl':
        logging.info("Found STL, loading")
        mod_file = read_stl_file(path)
    else:
        logging.error(f"Not supported {suffix}. Stop loading.")
        return
    
    logging.info("Load finish")

    return mod_file

def _generate_brep(shape: dict, name:str, path:str = '', cache_dir = "tmp"):
    file_list = []
    meta = {}
    sha: TopoDS_Shape = shape['data'] # The TopoDS_Shape object
    children = shape['children'] # The children dict
    logging.debug(f"Writing {cache_dir}/{path}-{name}.brep: {sha}")
    write_brep_file(sha, f'{cache_dir}/{path}-{name}.brep')

    children_meta = {}
    for child_name, child_shape in children:
        child_meta, fl = _generate_brep(child_shape, child_name, f'{path}-{child_name}', cache_dir)
        # i = d
        file_list += fl
        children_meta[child_name] = child_meta

    attributes = {}

    # TODO: attributes
    meta['data'] = {
            'brep_file': f'{path}-{name}.brep',
            'attributes': attributes
        }
    meta['children'] = children_meta

    file_list.append(f'.{cache_dir}/{path}-{name}.brep')
    return meta, file_list

def compress_folder(zfile:ZipFile, folder:str, baseDir=""):
    logging.debug("Compress folder:" + folder)
    logging.debug("Base dir:" + baseDir)
    fileList=os.listdir(folder)
    for file in fileList:
        if os.path.isfile(os.path.join(folder,file)): # 如果是文件
            zfile.write(os.path.join(folder,file),os.path.join(baseDir,file))
        else:
            zfile.write(os.path.join(folder,file),baseDir+"/"+file) # 创建文件夹
            logging.debug(f"Compressing folder {file}")
            # baseFolderName=os.path.basename(folder)
            compress_folder(zfile,os.path.join(folder,file),baseDir=os.path.join(baseDir,file))

def save(path:str, shapes:shape_data.main_datas):
    logging.info("Save file:" + path)
    data = shapes.export_to_json()
    cache = tempfile.mktemp()
    os.mkdir(cache)
    logging.debug(f"Cache dir: {cache}")

    meta = {}
    for name, sha in data.items():
        _meta, brep_list = _generate_brep(sha, name, cache_dir=cache) # meta.json and brep files
        meta[name] = _meta
    logging.debug(f"Meta data: {meta}")
    with open(f'{cache}/meta.json', 'w') as f:
        f.write(json.dumps(meta, ensure_ascii=False))
    with ZipFile(path, 'w') as f:
        compress_folder(f, cache)

def _load_brep(data_meta: dict, cache_dir:str) -> dict:
    shape = {}

    mod_file = TopoDS_Shape()
    builder = BRep_Builder()
    logging.debug(f"Loading:{cache_dir}/{data_meta['data']['brep_file']}")
    BRepTools.Read_(mod_file, f"{cache_dir}/{data_meta['data']['brep_file']}", builder)

    # TODO: attributes

    shape['data'] = mod_file

    children = {}
    for child_name, child_meta in data_meta['children'].items():
        children[child_name] = _load_brep(child_meta, cache_dir)

    shape['children'] = children
    return shape

def load_file(path:str) -> dict[str, dict]:
    cache = tempfile.mktemp()
    os.mkdir(cache)
    logging.debug(f"Unzip cache dir: {cache}")
    with ZipFile(path, 'r') as f:
        for name in f.namelist():
            f.extract(name, cache)

    with open(f'{cache}/meta.json', 'r') as f:
        meta:dict[str, dict] = json.loads(f.read())
    logging.debug(f"Meta data: {meta}")
    
    shape_datas = {}

    for name, shape in meta.items():
        shape_datas[name] = _load_brep(shape, cache)

    return shape_datas