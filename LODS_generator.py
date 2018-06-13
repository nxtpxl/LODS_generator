# pyside gui
import os
import site
site.addsitedir('C:\Program Files\Autodesk\Maya2018\Python\Lib\site-packages\Qt.py-master')
#print(Qt.__binding__)
import Qt
from Qt import QtWidgets

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from shiboken2 import wrapInstance
import maya.cmds as cmds
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

class LOD_Generator(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        path = "C:/Users/nitin.singh/Dropbox/MAYA_2018_python_code/polyReduce_002.ui"
        self.ui = QUiLoader().load(path)
        #self.ui = uic.loadUi(os.path.dirname(__file__) + '/poly_reduce_Ui.ui')
        #self.ui = uic.loadUi(path)
        self.addGeoIconPath = 'L:/NXTPXLENT/pipe___RND/library/icons/ui_icons/add.png'

        self.ui.tabWidget.setStyleSheet("""
        QTabBar::tab:selected {
            background:  darkGreen;
        }
        QTabWidget::tab-bar {
            left: 10px; /* move to the right by 5px */
        }
        QTabBar::tab {
            border: 2px solid #C4C4C3;

            border-top-left-radius: 1px;
            border-top-right-radius: 5px;
            min-width: 30ex;
        }
        QTabBar::tab:selected {
            border-color: #3BB143;
            border-top-color: lightGreen; /* same as pane color */
            margin-top: 0px; /* make non-selected tabs look smaller */
        }
        QTabWidget::tab-bar {
            alignment: center;
        }
        QTabBar::tab:hover {
            background: #0F52BA;
        }
        """)

        self.ui.add_selectedMesh_button.setIcon(QIcon(self.addGeoIconPath))
        self.ui.geometry_selected_name_lineEdit.setStyleSheet("* { background-color: rgba(0, 0, 0, 0); }");
        self.ui.LOD1_num.setDisabled(True)
        self.ui.LOD1_num.setStyleSheet("""QSpinBox { background-color: rgb(70, 70, 70)}""")
        self.ui.LOD2_num.setDisabled(True)
        self.ui.LOD2_num.setStyleSheet("""QSpinBox { background-color: rgb(70, 70, 70)}""")
        self.ui.LOD3_num.setDisabled(True)
        self.ui.LOD3_num.setStyleSheet("""QSpinBox { background-color: rgb(70, 70, 70)}""")
        self.ui.LOD1_horizontalSlider.setDisabled(True)
        self.ui.LOD1_horizontalSlider.setStyleSheet("""QLineEdit { background-color: rgb(70, 70, 70)}""")
        self.ui.LOD2_horizontalSlider.setDisabled(True)
        self.ui.LOD2_horizontalSlider.setStyleSheet("""QLineEdit { background-color: rgb(70, 70, 70)}""")
        self.ui.LOD3_horizontalSlider.setDisabled(True)
        self.ui.LOD3_horizontalSlider.setStyleSheet("""QLineEdit { background-color: rgb(70, 70, 70)}""")

        self.ui.wrap_comboBox.addItems(['180', '720', '2880' ])
        self.ui.BBOX_comboBox.addItems(['Bounding Box'])
        self.updateButton('off')



        self.ui.LOD1_spinBox.setDisabled(True)
        self.ui.LOD2_spinBox.setDisabled(True)
        self.ui.LOD3_spinBox.setDisabled(True)
        self.ui.wrap_comboBox.setDisabled(True)
        self.ui.BBOX_comboBox.setDisabled(True)
        self.ui.generate_button.setDisabled(True)
        self.ui.LOD1_spinBox.setStyleSheet("""QSpinBox { background-color: rgb(70, 70, 70)}""")
        self.ui.LOD2_spinBox.setStyleSheet("""QSpinBox { background-color: rgb(70, 70, 70)}""")
        self.ui.LOD3_spinBox.setStyleSheet("""QSpinBox { background-color: rgb(70, 70, 70)}""")

        self.ui.LOD1_spinBox.valueChanged.connect(self.ui.LOD1_horizontalSlider.setValue)
        self.ui.LOD1_horizontalSlider.valueChanged.connect(self.ui.LOD1_spinBox.setValue)
        self.ui.LOD1_spinBox.setValue(75)

        self.ui.LOD2_spinBox.valueChanged.connect(self.ui.LOD2_horizontalSlider.setValue)
        self.ui.LOD2_horizontalSlider.valueChanged.connect(self.ui.LOD2_spinBox.setValue)
        self.ui.LOD2_spinBox.setValue(35)

        self.ui.LOD3_spinBox.valueChanged.connect(self.ui.LOD3_horizontalSlider.setValue)
        self.ui.LOD3_horizontalSlider.valueChanged.connect(self.ui.LOD3_spinBox.setValue)
        self.ui.LOD3_spinBox.setValue(8)

        self.ui.LOD1_chkBox.stateChanged.connect(self.state_changed_LOD1)
        self.ui.LOD2_chkBox.stateChanged.connect(self.state_changed_LOD2)
        self.ui.LOD3_chkBox.stateChanged.connect(self.state_changed_LOD3)
        self.ui.WRAP_chkBox.stateChanged.connect(self.state_changed_wrap_LOD)
        self.ui.BBOX_chkBox.stateChanged.connect(self.state_changed_BBOX_LOD)
        self.ui.add_selectedMesh_button.clicked.connect(self.addGeoForReduction)
        self.ui.wrap_comboBox.setStyleSheet('selection-background-color: rgb(0,168,0)')
        self.ui.wrap_comboBox.setStyleSheet('background-color: rgb(70,70,70)')
        self.ui.generate_button.setStyleSheet("""QPushButton { background-color: rgb(70, 70, 70)}""")
        self.ui.generate_button.clicked.connect(self.generateLODS)
        self.ui.float_on_top_checkBox.toggled.connect(self.AlwaysOn_top)
        self.ui.float_on_top_checkBox.setStyleSheet("color: grey")

    def updateButton(self, status):
        font=QFont()
        font.setItalic(True)
        font.setPointSize(16)
        font.setBold(True)

        if status == 'on':
            pass
        else:
            font.setStrikeOut(True)
        self.ui.generate_button.setFont(font)

    def AlwaysOn_top(self):
        if self.ui.float_on_top_checkBox.isChecked():
            self.ui.setWindowFlags(self.ui.windowFlags() | Qt.WindowStaysOnTopHint)
            self.ui.float_on_top_checkBox.setStyleSheet("color: lightGreen")
            self.ui.show()
        else:
            self.ui.setWindowFlags(self.ui.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.ui.float_on_top_checkBox.setStyleSheet("color: grey")
            self.ui.show()

    def addGeoForReduction(self):
        mesh = cmds.ls(sl=True, transforms=True, type="mesh")
        print mesh
        self.ui.geometry_selected_name_lineEdit.clear()
        if mesh:
            fullPath = str(cmds.ls(mesh, long = True)[0])
            meshUUID = str(cmds.ls(fullPath, uuid = True)[0])
            self.ui.geometry_selected_name_lineEdit.setStyleSheet("""QLineEdit { background-color: green; color: yellow }""")
            print (mesh[0], fullPath, meshUUID)
            self.ui.selectedGeo_groupBox.setTitle('Selected Mesh:  ' +meshUUID)
            self.ui.geometry_selected_name_lineEdit.insert(mesh[0])
            self.updateButton('on')
            self.ui.generate_button.setDisabled(False)
            self.ui.generate_button.setStyleSheet("""QPushButton { background-color: rgb(0, 100, 0)}""")
            LOD01_Percent = self.ui.LOD1_horizontalSlider.value()
            LOD02_Percent = self.ui.LOD2_horizontalSlider.value()
            LOD03_Percent = self.ui.LOD3_horizontalSlider.value()
            currentMeshPolyGonCount = cmds.polyEvaluate(fullPath,f=True)
            print currentMeshPolyGonCount
            LOD01_PolyPercent = (LOD01_Percent * currentMeshPolyGonCount) / 100
            LOD02_PolyPercent = (LOD02_Percent * currentMeshPolyGonCount) / 100
            LOD03_PolyPercent = (LOD03_Percent * currentMeshPolyGonCount) / 100

            self.ui.LOD1_num.setValue(LOD01_PolyPercent)
            self.ui.LOD2_num.setValue(LOD02_PolyPercent)
            self.ui.LOD3_num.setValue(LOD03_PolyPercent)

        else:
            self.ui.geometry_selected_name_lineEdit.setStyleSheet("""QLineEdit { background-color: red; color: white }""")
            self.ui.selectedGeo_groupBox.setTitle('Selected Mesh')
            self.ui.geometry_selected_name_lineEdit.insert('not a valid selection')
            self.updateButton('off')
            self.ui.generate_button.setDisabled(True)
            self.ui.generate_button.setStyleSheet("""QPushButton { background-color: rgb(70, 70, 70)}""")

    def state_changed_LOD1(self, int):
        self.UIStateUpdate(self.ui.LOD1_chkBox, self.ui.LOD1_num, self.ui.LOD1_horizontalSlider, self.ui.LOD1_spinBox)

    def state_changed_LOD2(self, int):
        self.UIStateUpdate(self.ui.LOD2_chkBox, self.ui.LOD2_num, self.ui.LOD2_horizontalSlider, self.ui.LOD2_spinBox)

    def state_changed_LOD3(self, int):
        self.UIStateUpdate(self.ui.LOD3_chkBox, self.ui.LOD3_num, self.ui.LOD3_horizontalSlider, self.ui.LOD3_spinBox)

    def UIStateUpdate(self, chkBox, intField, slider, spinBox):
        if chkBox.isChecked():
            intField.setDisabled(False)
            slider.setDisabled(False)
            spinBox.setDisabled(False)
            intField.setStyleSheet("""QSpinBox { background-color: rgb(35, 35, 35)}""")
            slider.setStyleSheet("""QLineEdit { background-color: rgb(35, 35, 35)}""")
            spinBox.setStyleSheet("""QSpinBox { background-color: rgb(60, 60, 60)}""")
        else:
            intField.setValue(0)
            intField.setDisabled(True)
            slider.setDisabled(True)
            spinBox.setDisabled(True)
            spinBox.setValue(10)
            intField.setStyleSheet("""QSpinBox { background-color: rgb(70, 70, 70)}""")
            slider.setStyleSheet("""QLineEdit { background-color: rgb(70, 70, 70)}""")
            spinBox.setStyleSheet("""QSpinBox { background-color: rgb(70, 70, 70)}""")



    def state_changed_wrap_LOD(self, int):
        if self.ui.WRAP_chkBox.isChecked():
            self.ui.wrap_comboBox.setDisabled(False)
            self.ui.wrap_comboBox.setStyleSheet('background-color: rgb(35,35,35)')
        else:
            self.ui.wrap_comboBox.setDisabled(True)
            self.ui.wrap_comboBox.setStyleSheet('background-color: rgb(70,70,70)')

    def state_changed_BBOX_LOD(self, int):
        if self.ui.BBOX_chkBox.isChecked():
            self.ui.BBOX_comboBox.setDisabled(False)
            self.ui.BBOX_comboBox.setStyleSheet('background-color: rgb(35,35,35)')
        else:
            self.ui.BBOX_comboBox.setDisabled(True)
            self.ui.BBOX_comboBox.setStyleSheet('background-color: rgb(70,70,70)')

    def whatTab(self):
        currentIndex = self.ui.tabWidget.currentIndex()
        currentWidget = self.ui.tabWidget.currentWidget()
        return currentIndex

    def tabSelected(self, arg=None):
        print '\n\t tabSelected() current Tab index =', arg

    def genFunction(self, createdLOD, reductionNumber):
        mesh = cmds.select(createdLOD)
        #mel.eval('polyCleanupArgList 3 { "0","2","1","0","1","1","1","0","0","1e-005","1","1e-005","1","1e-005","0","1","1" };')
        cmds.polyReduce(ver=1, termination=2, tct=reductionNumber)
        cmds.delete(ch=True)


    def MakeCube(self, *args):
        geo = cmds.geomToBBox(keepOriginal=True, name="bakedBOX", combineMesh = True)
        return geo


    def copyPivot(self):
        #1. Select source object(s)
        #2. Add to selection target object

        sourceObj = cmds.ls(sl = True)[len(cmds.ls(sl = True))-1]
        targetObj = cmds.ls(sl = True)[0:(len(cmds.ls(sl = True))-1)]
        parentList = []
        for obj in targetObj:
            print obj
            if cmds.listRelatives( obj, parent = True):
                parentList.append(cmds.listRelatives( obj, parent = True)[0])
            else:
                parentList.append('')
        if len(cmds.ls(sl = True))<2:
            cmds.error('select 2 or more objects.')
        pivotTranslate = cmds.xform (sourceObj, q = True, ws = True, rotatePivot = True)
        cmds.parent(targetObj, sourceObj)
        cmds.makeIdentity(targetObj, a = True, t = True, r = True, s = True)
        cmds.xform (targetObj, ws = True, pivots = pivotTranslate)
        for ind in range(len(targetObj)):
            if parentList[ind] != '' :
                cmds.parent(targetObj[ind], parentList[ind])
            else:
                cmds.parent(targetObj[ind], world = True)

    def generateLODS(self):

        x = self.ui.selectedGeo_groupBox.title()
        x = (x.replace('Selected Mesh:  ',''))
        fullPath = str(cmds.ls(x, long = True)[0])
        if fullPath:
            print fullPath
            obSl = fullPath
            if len(obSl) == 0:
                cmds.confirmDialog(title='Error:', message='No objects selected for polygon reduction')
            else:
                print ('\n')
                cmds.select(obSl)
                lods = []
                LOD01_Val = []
                LOD02_Val = []
                LOD03_Val = []

                currentIndex = self.whatTab()
                print currentIndex
                if currentIndex == 0:
                    LOD1_Number = int(self.ui.LOD1_num.text())
                    LOD2_Number = int(self.ui.LOD2_num.text())
                    LOD3_Number = int(self.ui.LOD3_num.text())
                    LOD3_Number = int(self.ui.LOD3_num.text())
                    LOD01_Val.append(LOD1_Number)
                    LOD02_Val.append(LOD2_Number)
                    LOD03_Val.append(LOD3_Number)
                else:
                    LOD01_Percent = self.ui.LOD1_horizontalSlider.value()
                    LOD02_Percent = self.ui.LOD2_horizontalSlider.value()
                    LOD03_Percent = self.ui.LOD3_horizontalSlider.value()
                    currentMeshPolyGonCount = cmds.polyEvaluate(f=True)
                    print currentMeshPolyGonCount
                    LOD01_PolyPercent = (LOD01_Percent * currentMeshPolyGonCount) / 100
                    LOD02_PolyPercent = (LOD02_Percent * currentMeshPolyGonCount) / 100
                    LOD03_PolyPercent = (LOD03_Percent * currentMeshPolyGonCount) / 100
                    LOD01_Val.append(LOD01_PolyPercent)
                    LOD02_Val.append(LOD02_PolyPercent)
                    LOD03_Val.append(LOD03_PolyPercent)

                LOD0_LOD = cmds.duplicate(obSl, name=(obSl + '__LOD0'))
                lods.append(LOD0_LOD)

                print LOD01_Val,LOD02_Val,LOD03_Val
                if self.ui.LOD1_chkBox.isChecked():
                    LOD1_Num = LOD01_Val[0]
                    LOD1_LOD = cmds.duplicate(obSl, name=(obSl + '__LOD1'))
                    self.genFunction(LOD1_LOD, LOD1_Num)
                    lods.append(LOD1_LOD)
                    print ('"__LOD1"__LOD__generated__Successfully :~- ' + str(LOD1_LOD))
                if self.ui.LOD2_chkBox.isChecked():
                    LOD2_Num = LOD02_Val[0]
                    LOD2_LOD = cmds.duplicate(obSl, name=(obSl + '__LOD2'))
                    self.genFunction(LOD2_LOD, LOD2_Num)
                    lods.append(LOD2_LOD)
                    print ('"__LOD2"__LOD__generated__Successfully :~- ' + str(LOD2_LOD))
                if self.ui.LOD3_chkBox.isChecked():
                    LOD3_Num = LOD03_Val[0]
                    LOD3_LOD = cmds.duplicate(obSl, name=(obSl + '__LOD3'))
                    self.genFunction(LOD3_LOD, LOD3_Num)
                    lods.append(LOD3_LOD)
                    print ('"__LOD3"__LOD__generated__Successfully :~- ' + str(LOD3_LOD))

                if self.ui.WRAP_chkBox.isChecked():
                    WRAP_Num = str(self.ui.wrap_comboBox.currentText())
                    print WRAP_Num
                    LOD5_LOD = cmds.CreatePolygonSoccerBall(n = obSl + '__LOD4')
                    newMesh = cmds.rename(LOD5_LOD, (obSl + '__LOD4'))
                    if WRAP_Num == '180':
                        cmds.polySmooth(newMesh, divisions=1 )
                    if WRAP_Num == '720':
                        cmds.polySmooth(newMesh, divisions=2 )
                    if WRAP_Num == '2880':
                        cmds.polySmooth(newMesh, divisions=3 )
                    cmds.delete(newMesh, ch = True)
                    bbox = cmds.exactWorldBoundingBox(obSl)
                    x1, y1, z1, x2, y2, z2 = cmds.exactWorldBoundingBox(obSl)
                    xc = (x2 + x1) / 2.0
                    yc = (y2 + y1) / 2.0
                    zc = (z2 + z1) / 2.0
                    xw = x2 - x1
                    yw = y2 - y1
                    zw = z2 - z1
                    cmds.move(xc, yc, zc, newMesh)
                    cmds.scale(xw, yw, zw, newMesh)
                    shrinkWrapNode = pm.deformer(newMesh, type='shrinkWrap')[0]
                    pm.PyNode(obSl).worldMesh[0] >> shrinkWrapNode.targetGeom
                    shrinkWrapNode.closestIfNoIntersection.set(True)
                    cmds.delete(newMesh, ch = True)
                    cmds.select(clear = True)
                    cmds.select(newMesh)
                    cmds.select(obSl, add = True)
                    self.copyPivot()


                    lods.append(newMesh)
                if self.ui.BBOX_chkBox.isChecked():
                    print ('make a bounding box')
                    cmds.select(obSl)
                    box = self.MakeCube()
                    newmeshBox = cmds.rename(box, (obSl + '__LOD5'))
                    lods.append(newmeshBox)
                    cmds.select(obSl)
                    cmds.select(newmeshBox, add = True)
                    self.copyPivot()

                cmds.select(clear=True)
                if lods == []:
                    pass
                else:
                    grp = (obSl + '__LOD_grp')
                    if cmds.objExists(grp):
                        pass
                    else:
                        lod_grp = cmds.group(n=grp, em=True)
                    print grp
                    for lod in lods:
                        print lod
                        cmds.parent(lod, grp)
                print ('\n')
                cmds.inViewMessage(amg="LOD generated successfully", pos="botCenter", fade=True)
                print('Done')

        else:
            cmds.confirmDialog(title='Error:', message='No objects selected for polygon reduction')



def run():
    global UI
    UI = LOD_Generator()
    UI.ui.show()


run()
