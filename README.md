# potatoCAD
We are going to build simple CAD that is easy to learn and easy to use.

## Meaning
Although FreeCAD has provided a lot of powerful functions, we found that FreeCAD is not easy to learn and has a lot of bugs. So we hope to build a new CAD that doesn't need t be powerful but easy to use.

## Main libraries
 - [pyOCCT2](https://github.com/ovo-Tim/pyOCCT2)
 - [PySide6](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/index.html)
 - [pyqtribbon](https://github.com/ovo-Tim/pyqtribbon)

 ## Our problems
 We found that open cascade visualization doesn't support wayland([Link](https://dev.opencascade.org/content/it-possible-native-support-wayland)). So we decided to use another visualization library. We found that FreeCAD uses [Coin3D](https://www.coin3d.org/) and Coin3D can be displayed on wayland. But there is no document about making OCCT and Coin3D work together.