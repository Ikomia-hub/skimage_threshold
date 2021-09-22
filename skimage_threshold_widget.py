from ikomia import core, dataprocess
from ikomia.utils import qtconversion
from skimage_threshold.skimage_threshold_process import ThresholdParam
# PyQt GUI framework
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# --------------------
# - Class which implements widget associated with the process
# - Inherits core.CProtocolTaskWidget from Ikomia API
# --------------------
class ThresholdWidget(core.CWorkflowTaskWidget):

    def __init__(self, param, parent):
        core.CWorkflowTaskWidget.__init__(self, parent)

        if param is None:
            self.parameters = ThresholdParam()
        else:
            self.parameters = param

        self.MAX_SPINBOX = 10000000
        self.gridLayout = QGridLayout()
        
        # all parameters widgets
        self.stack_none = QWidget()
        self.stack_otsu = QWidget()
        self.stack_yen = QWidget()
        self.stack_local = QWidget()
        self.stack_minimum = QWidget()
        self.stack_triangle = QWidget()
        self.stack_niblack = QWidget()
        self.stack_sauvola = QWidget()
        self.stack_multiotsu = QWidget()
        self.stack_hysteris = QWidget()
        self.stack_isodata = QWidget()
        self.stack_li = QWidget()

        # set all parameters widgets
        self.stack_methodWidget()
        self.stack_triangleWidget()
        self.stack_minimumWidget()
        self.stack_localWidget()
        self.stack_niblackWidget()
        self.stack_sauvolaWidget()
        self.stack_multiotsuWidget()
        self.stack_hysterisWidget()
        self.stack_otsuWidget()
        self.stack_yenWidget()
        self.stack_isodataWidget()
        self.stack_liWidget()

        # main widget
        self.stack = QStackedWidget()
        self.stack.addWidget(self.stack_otsu)
        self.stack.addWidget(self.stack_local)
        self.stack.addWidget(self.stack_niblack)
        self.stack.addWidget(self.stack_triangle)
        self.stack.addWidget(self.stack_multiotsu)
        self.stack.addWidget(self.stack_hysteris)
        self.stack.addWidget(self.stack_minimum)
        self.stack.addWidget(self.stack_none)
        self.stack.addWidget(self.stack_yen)
        self.stack.addWidget(self.stack_isodata)
        self.stack.addWidget(self.stack_li)
        self.stack.addWidget(self.stack_sauvola)
        self.gridLayout.addWidget(self.stack, 2, 0)

        layout_ptr = qtconversion.PyQtToQt(self.gridLayout)
        self.setLayout(layout_ptr)

        # update left parameter panel
        if self.parameters.local_method != None:
           index = self.stack_comboMethod.findText(self.parameters.local_method, Qt.MatchFixedString)
           self.stack_comboMethod.setCurrentIndex(index)

    # widgets methods
    def stack_methodWidget(self):
        label_method = QLabel("Méthode de seuillage :")
        self.stack_comboMethod = QComboBox()
        self.stack_comboMethod.addItem("Otsu")
        self.stack_comboMethod.addItem("Yen")
        self.stack_comboMethod.addItem("Iso data")
        self.stack_comboMethod.addItem("Li")
        self.stack_comboMethod.addItem("Mean")
        self.stack_comboMethod.addItem("Minimum")
        self.stack_comboMethod.addItem("Local")
        self.stack_comboMethod.addItem("Niblack")
        self.stack_comboMethod.addItem("Sauvola")
        self.stack_comboMethod.addItem("Triangle")
        self.stack_comboMethod.addItem("Multi otsu")
        self.stack_comboMethod.addItem("Hysteresis")
        self.stack_comboMethod.currentIndexChanged.connect(self.onSelectionChange)
        self.gridLayout.addWidget(label_method,0,0)
        self.gridLayout.addWidget(self.stack_comboMethod,1,0)

    def stack_localWidget(self):
        gridLayout = QGridLayout()

        label_block_size = QLabel("block size :")
        self.spin_block_size = QSpinBox()
        self.spin_block_size.setValue(35)
        self.spin_block_size.setSingleStep(2)
        self.spin_block_size.setMaximum(self.MAX_SPINBOX)
        # update left parameter panel
        if self.parameters.local_block_size != 35:
            self.spin_block_size.setValue(self.parameters.local_block_size)

        label_mth = QLabel("method :")
        self.stack_comboMethod_mth = QComboBox()
        self.stack_comboMethod_mth.addItem("gaussian")
        self.stack_comboMethod_mth.addItem("mean")
        self.stack_comboMethod_mth.addItem("median")
        # update left parameter panel
        if self.parameters.local_mth == "mean":
            self.stack_comboMethod_mth.clear()
            self.stack_comboMethod_mth.addItem("mean")
            self.stack_comboMethod_mth.addItem("gaussian")
            self.stack_comboMethod_mth.addItem("median")
        if self.parameters.local_mth == "median":
            self.stack_comboMethod_mth.clear()
            self.stack_comboMethod_mth.addItem("median")
            self.stack_comboMethod_mth.addItem("gaussian")
            self.stack_comboMethod_mth.addItem("mean")
        self.stack_comboMethod_mth.currentIndexChanged.connect(self.onSelectionMethod)

        label_offset = QLabel("offset :")
        self.spin_offset = QSpinBox()
        self.spin_offset.setValue(0)
        self.spin_offset.setMaximum(self.MAX_SPINBOX)
        # update left parameter panel
        if self.parameters.local_offset != 0:
            self.spin_offset.setValue(self.parameters.local_offset)

        label_mode = QLabel("mode :")
        self.stack_comboMethod_mode = QComboBox()
        self.stack_comboMethod_mode.addItem("reflect")
        self.stack_comboMethod_mode.addItem("constant")
        self.stack_comboMethod_mode.addItem("nearest")
        self.stack_comboMethod_mode.addItem("mirror")
        self.stack_comboMethod_mode.addItem("wrap")
        # update left parameter panel
        if self.parameters.local_mode == "constant":
            self.stack_comboMethod_mode.clear()
            self.stack_comboMethod_mode.addItem("constant")
            self.stack_comboMethod_mode.addItem("reflect")
            self.stack_comboMethod_mode.addItem("nearest")
            self.stack_comboMethod_mode.addItem("mirror")
            self.stack_comboMethod_mode.addItem("wrap")
        elif self.parameters.local_mode == "nearest":
            self.stack_comboMethod_mode.clear()
            self.stack_comboMethod_mode.addItem("nearest")
            self.stack_comboMethod_mode.addItem("reflect")
            self.stack_comboMethod_mode.addItem("constant")
            self.stack_comboMethod_mode.addItem("mirror")
            self.stack_comboMethod_mode.addItem("wrap")
        elif self.parameters.local_mode == "mirror":
            self.stack_comboMethod_mode.clear()
            self.stack_comboMethod_mode.addItem("mirror")
            self.stack_comboMethod_mode.addItem("reflect")
            self.stack_comboMethod_mode.addItem("constant")
            self.stack_comboMethod_mode.addItem("nearest")
            self.stack_comboMethod_mode.addItem("wrap")
        elif self.parameters.local_mode == "wrap":
            self.stack_comboMethod_mode.clear()
            self.stack_comboMethod_mode.addItem("wrap")
            self.stack_comboMethod_mode.addItem("reflect")
            self.stack_comboMethod_mode.addItem("constant")
            self.stack_comboMethod_mode.addItem("nearest")
            self.stack_comboMethod_mode.addItem("mirror")
        self.stack_comboMethod_mode.currentIndexChanged.connect(self.onSelectionMode)

        self.label_cval = QLabel("c_val :")
        self.spin_cval = QDoubleSpinBox()
        self.spin_cval.setValue(0)
        self.spin_cval.setMaximum(self.MAX_SPINBOX)
        self.spin_cval.setSingleStep(0.1)
        # update left parameter panel
        if self.parameters.local_mode == "constant":
            self.spin_cval.setValue(self.parameters.local_cval)
        else :
            self.label_cval.hide()
            self.spin_cval.hide()

        self.label_local_param = QLabel("sigma :")
        self.spin_local_param = QDoubleSpinBox()
        self.spin_local_param.setValue(2.0)
        self.spin_local_param.setMaximum(self.MAX_SPINBOX)
        # update left parameter panel
        if self.parameters.local_mth == "gaussian" and self.parameters.local_param != None:
            self.spin_local_param.setValue(self.parameters.local_param)
        if self.parameters.local_mth != "gaussian": 
            self.label_local_param.hide()
            self.spin_local_param.hide()

        gridLayout.setRowStretch(0,0)
        gridLayout.addWidget(label_block_size, 0, 0)
        gridLayout.setRowStretch(0,1)
        gridLayout.addWidget(self.spin_block_size, 0, 1)
        gridLayout.setRowStretch(1,2)
        gridLayout.addWidget(label_mth, 1, 0)
        gridLayout.setRowStretch(1,3)
        gridLayout.addWidget(self.stack_comboMethod_mth, 1, 1)
        gridLayout.setRowStretch(2,4)
        gridLayout.addWidget(self.label_local_param, 2, 0)
        gridLayout.setRowStretch(2,5)
        gridLayout.addWidget(self.spin_local_param, 2, 1)
        gridLayout.setRowStretch(3,6)
        gridLayout.addWidget(label_offset, 3, 0)
        gridLayout.setRowStretch(3,7)
        gridLayout.addWidget(self.spin_offset, 3, 1)
        gridLayout.setRowStretch(4,8)
        gridLayout.addWidget(label_mode, 4, 0)
        gridLayout.setRowStretch(4,9)
        gridLayout.addWidget(self.stack_comboMethod_mode, 4, 1)
        gridLayout.setRowStretch(5,10)
        gridLayout.addWidget(self.label_cval, 5, 0)
        gridLayout.setRowStretch(5,11)
        gridLayout.addWidget(self.spin_cval, 5, 1)
        gridLayout.setRowStretch(6,12)
        self.stack_local.setLayout(gridLayout)

    def stack_niblackWidget(self):
        gridLayout = QGridLayout()
        label_window_size = QLabel("window_size :")
        self.spin_window_sizenb = QSpinBox()
        self.spin_window_sizenb.setValue(15)
        self.spin_window_sizenb.setSingleStep(2)
        self.spin_window_sizenb.setMinimum(1)
        self.spin_window_sizenb.setMaximum(self.MAX_SPINBOX)
        if self.parameters.niblackSauvola_window_size != 15:
            self.spin_window_sizenb.setValue(self.parameters.niblackSauvola_window_size)

        label_k = QLabel("k :")
        self.spin_knb = QDoubleSpinBox()
        self.spin_knb.setSingleStep(0.05)
        self.spin_knb.setValue(0.2)
        self.spin_knb.setMaximum(self.MAX_SPINBOX)
        if self.parameters.niblackSauvola_k != 0.2:
            self.spin_knb.setValue(self.parameters.niblackSauvola_k)

        gridLayout.setRowStretch(0,0)
        gridLayout.addWidget(label_window_size, 0, 0)
        gridLayout.setRowStretch(0,1)
        gridLayout.addWidget(self.spin_window_sizenb, 0, 1)
        gridLayout.setRowStretch(1,2)
        gridLayout.addWidget(label_k, 1, 0)
        gridLayout.setRowStretch(2,3)
        gridLayout.addWidget(self.spin_knb, 1, 1)
        gridLayout.setRowStretch(3,4)
        self.stack_niblack.setLayout(gridLayout)

    def stack_sauvolaWidget(self):
        gridLayout = QGridLayout()
        label_window_size = QLabel("window_size :")
        self.spin_window_size = QSpinBox()
        self.spin_window_size.setValue(15)
        self.spin_window_size.setMaximum(self.MAX_SPINBOX)
        self.spin_window_size.setSingleStep(2)
        self.spin_window_size.setMinimum(1)
        if self.parameters.niblackSauvola_window_size != 15:
            self.spin_window_size.setValue(self.parameters.niblackSauvola_window_size)

        label_k = QLabel("k :")
        self.spin_k = QDoubleSpinBox()
        self.spin_k.setMaximum(self.MAX_SPINBOX)
        self.spin_k.setSingleStep(0.05)
        self.spin_k.setValue(0.2)
        if self.parameters.niblackSauvola_k != 0.2:
            self.spin_k.setValue(self.parameters.niblackSauvola_k)

        self.sauvola_check = QCheckBox("Default r");
        self.sauvola_check.setChecked(True);

        self.spin_r = QDoubleSpinBox()
        self.spin_r.setSingleStep(10)
        self.spin_r.setMaximum(self.MAX_SPINBOX)
        self.spin_r.setValue(0)
        
        if self.parameters.sauvola_r != None:
            self.sauvola_check.setChecked(False)
            self.spin_r.setValue(self.parameters.sauvola_r)
        else : 
            self.spin_r.hide()

        self.sauvola_check.stateChanged.connect(self.OnSauvolaDefaultChange)

        gridLayout.setRowStretch(0,0)
        gridLayout.addWidget(label_window_size, 0, 0)
        gridLayout.setRowStretch(0,1)
        gridLayout.addWidget(self.spin_window_size, 0, 1)
        gridLayout.setRowStretch(1,2)
        gridLayout.addWidget(label_k, 1, 0)
        gridLayout.setRowStretch(1,3)
        gridLayout.addWidget(self.spin_k, 1, 1)
        gridLayout.setRowStretch(2,4)
        gridLayout.addWidget(self.sauvola_check, 2, 0)
        gridLayout.setRowStretch(2,5)
        gridLayout.addWidget(self.spin_r, 2, 1)
        gridLayout.setRowStretch(3,6)
        self.stack_sauvola.setLayout(gridLayout)

    def stack_triangleWidget(self):
        gridLayout = QGridLayout()
        label_nbins = QLabel("nbins :")
        self.spin_nbins = QSpinBox()
        self.spin_nbins.setMaximum(self.MAX_SPINBOX)
        self.spin_nbins.setValue(256)
        if self.parameters.triangle_nbins != 256:
            self.spin_nbins.setValue(self.parameters.triangle_nbins)

        gridLayout.setRowStretch(0,0)
        gridLayout.addWidget(label_nbins, 0, 0)
        gridLayout.setRowStretch(0,1)
        gridLayout.addWidget(self.spin_nbins, 0, 1)
        gridLayout.setRowStretch(1,2)
        self.stack_triangle.setLayout(gridLayout)

    def stack_otsuWidget(self):
        gridLayout = QGridLayout()
        label_nbins = QLabel("nbins :")
        self.spin_nbinsOtsu = QSpinBox()
        self.spin_nbinsOtsu.setMaximum(self.MAX_SPINBOX)
        self.spin_nbinsOtsu.setValue(256)
        if self.parameters.otsu_nbins != 256:
            self.spin_nbinsOtsu.setValue(self.parameters.otsu_nbins)

        gridLayout.setRowStretch(0,0)
        gridLayout.addWidget(label_nbins, 0, 0)
        gridLayout.setRowStretch(0,1)
        gridLayout.addWidget(self.spin_nbinsOtsu, 0, 1)
        gridLayout.setRowStretch(1,2)

        self.stack_otsu.setLayout(gridLayout)

    def stack_isodataWidget(self):
        gridLayout = QGridLayout()
        label_nbins = QLabel("nbins :")
        self.spin_nbinsIso = QSpinBox()
        self.spin_nbinsIso.setMaximum(self.MAX_SPINBOX)
        self.spin_nbinsIso.setValue(256)
        if self.parameters.isodata_nbins != 256:
            self.spin_nbinsIso.setValue(self.parameters.isodata_nbins)

        gridLayout.setRowStretch(0,0)
        gridLayout.addWidget(label_nbins, 0, 0)
        gridLayout.setRowStretch(0,1)
        gridLayout.addWidget(self.spin_nbinsIso, 0, 1)
        gridLayout.setRowStretch(1,2)
        self.stack_isodata.setLayout(gridLayout)

    def stack_yenWidget(self):
        gridLayout = QGridLayout()
        label_nbins = QLabel("nbins :")
        self.spin_nbinsYen = QSpinBox()
        self.spin_nbinsYen.setMaximum(self.MAX_SPINBOX)
        self.spin_nbinsYen.setValue(256)
        if self.parameters.yen_nbins != 256:
            self.spin_nbinsYen.setValue(self.parameters.yen_nbins)

        gridLayout.setRowStretch(0,0)
        gridLayout.addWidget(label_nbins, 0, 0)
        gridLayout.setRowStretch(0,1)
        gridLayout.addWidget(self.spin_nbinsYen, 0, 1)
        gridLayout.setRowStretch(1,2)
        self.stack_yen.setLayout(gridLayout)

    def stack_liWidget(self):
        gridLayout = QGridLayout()
        label_default = QLabel("Default value :")
        self.li_check = QCheckBox();
        self.li_check.setChecked(True);
        self.label_tolerence = QLabel("tolerance :")
        self.spin_tolerance = QDoubleSpinBox()
        self.spin_tolerance.setValue(0.1)
        self.spin_tolerance.setMinimum(0.1)
        self.spin_tolerance.setSingleStep(0.01)
        self.spin_tolerance.setMaximum(65535)
        self.label_initialguess = QLabel("initial_guess :")
        self.spin_initialguess = QDoubleSpinBox()
        self.spin_initialguess.setValue(0.1)
        self.spin_initialguess.setMinimum(0.1)
        self.spin_initialguess.setSingleStep(0.01)
        self.spin_initialguess.setMaximum(65535)
        self.li_check.stateChanged.connect(self.OnLiDefaultChange)

        if self.parameters.li_tolerance != None or self.parameters.li_initialguess != None:
            self.li_check.setChecked(False)
            self.spin_tolerance.setValue(self.parameters.li_tolerance)
            self.spin_initialguess.setValue(self.parameters.li_initialguess)
        else : 
            self.label_tolerence.hide()
            self.spin_tolerance.hide()
            self.label_initialguess.hide()
            self.spin_initialguess.hide()

        gridLayout.setRowStretch(0,0)
        gridLayout.addWidget(label_default, 0, 0)
        gridLayout.setRowStretch(0,1)
        gridLayout.addWidget(self.li_check, 0, 1)
        gridLayout.setRowStretch(1,2)
        gridLayout.addWidget(self.label_tolerence, 1, 0)
        gridLayout.setRowStretch(1,3)
        gridLayout.addWidget(self.spin_tolerance, 1, 1)
        gridLayout.setRowStretch(2,4)
        gridLayout.addWidget(self.label_initialguess, 2, 0)
        gridLayout.setRowStretch(2,5)
        gridLayout.addWidget(self.spin_initialguess, 2, 1)
        gridLayout.setRowStretch(3,6)
        
        self.stack_li.setLayout(gridLayout)

    def stack_multiotsuWidget(self):
        gridLayout = QGridLayout()
        label_classes = QLabel("classes :")
        self.spin_classes = QSpinBox()
        self.spin_classes.setMinimum(2)
        self.spin_classes.setValue(3)
        self.spin_classes.setMaximum(self.MAX_SPINBOX)
        if self.parameters.multiotsu_classes != 3:
            self.spin_classes.setValue(self.parameters.multiotsu_classes)

        label_mo_nbins = QLabel("nbins :")
        self.spin_mo_nbins = QSpinBox()
        self.spin_mo_nbins.setMaximum(self.MAX_SPINBOX)
        self.spin_mo_nbins.setValue(256)
        if self.parameters.multiotsu_nbins != 3:
            self.spin_mo_nbins.setValue(self.parameters.multiotsu_nbins)

        gridLayout.setRowStretch(0,0)
        gridLayout.addWidget(label_classes, 0, 0)
        gridLayout.setRowStretch(0,1)
        gridLayout.addWidget(self.spin_classes, 0, 1)
        gridLayout.setRowStretch(1,2)
        gridLayout.addWidget(label_mo_nbins, 1, 0)
        gridLayout.setRowStretch(1,3)
        gridLayout.addWidget(self.spin_mo_nbins, 1, 1)
        gridLayout.setRowStretch(2,4)
        self.stack_multiotsu.setLayout(gridLayout)

    def stack_hysterisWidget(self):
        gridLayout = QGridLayout()
        label_low = QLabel("low :")
        self.spin_low = QDoubleSpinBox()
        self.spin_low.setSingleStep(0.05)
        self.spin_low.setMaximum(self.MAX_SPINBOX)
        self.spin_low.setValue(0.1)
        if self.parameters.hysteresis_low != 0.1:
            self.spin_low.setValue(self.parameters.hysteresis_low)

        label_hight = QLabel("hight :")
        self.spin_hight = QDoubleSpinBox()
        self.spin_hight.setSingleStep(0.05)
        self.spin_hight.setMaximum(self.MAX_SPINBOX)
        self.spin_hight.setValue(0.35)
        if self.parameters.hysteresis_hight != 0.35:
            self.spin_hight.setValue(self.parameters.hysteresis_hight)

        gridLayout.setRowStretch(0,0)
        gridLayout.addWidget(label_low, 0, 0)
        gridLayout.setRowStretch(0,1)
        gridLayout.addWidget(self.spin_low, 0, 1)
        gridLayout.setRowStretch(1,2)
        gridLayout.addWidget(label_hight, 1, 0)
        gridLayout.setRowStretch(1,3)
        gridLayout.addWidget(self.spin_hight, 1, 1)
        gridLayout.setRowStretch(2,4)
        self.stack_hysteris.setLayout(gridLayout)

    def stack_minimumWidget(self):
        gridLayout = QGridLayout()
        label_nbins = QLabel("nbins :")
        self.spin_nbinsmin = QSpinBox()
        self.spin_nbinsmin.setMaximum(self.MAX_SPINBOX)
        self.spin_nbinsmin.setValue(256)
        if self.parameters.minimum_nbins != 256:
            self.spin_nbinsmin.setValue(self.parameters.minimum_nbins)

        label_maxiter = QLabel("max_iter:")
        self.spin_maxiter = QSpinBox()
        self.spin_maxiter.setMinimum(0)
        self.spin_maxiter.setMaximum(self.MAX_SPINBOX)
        self.spin_maxiter.setValue(10000)
        self.spin_maxiter.setSingleStep(10)
        if self.parameters.minimum_maxiter != 10000:
            self.spin_maxiter.setValue(self.parameters.minimum_maxiter)

        gridLayout.setRowStretch(0,0)
        gridLayout.addWidget(label_nbins, 0, 0)
        gridLayout.setRowStretch(0,1)
        gridLayout.addWidget(self.spin_nbinsmin, 0, 1)
        gridLayout.setRowStretch(1,2)
        gridLayout.addWidget(label_maxiter, 1, 0)
        gridLayout.setRowStretch(1,3)
        gridLayout.addWidget(self.spin_maxiter, 1, 1)
        gridLayout.setRowStretch(2,4)
        self.stack_minimum.setLayout(gridLayout)

    # pySlot -> chosen method
    def onSelectionChange(self):
        if self.stack_comboMethod.currentText() == "Local":
            self.stack.setCurrentIndex(1)
        elif self.stack_comboMethod.currentText() == "Niblack":
            self.stack.setCurrentIndex(2)
        elif self.stack_comboMethod.currentText() == "Triangle":
            self.stack.setCurrentIndex(3)
        elif self.stack_comboMethod.currentText() == "Multi otsu":
            self.stack.setCurrentIndex(4)
        elif self.stack_comboMethod.currentText() == "Hysteresis":
            self.stack.setCurrentIndex(5)
        elif self.stack_comboMethod.currentText() == "Minimum":
            self.stack.setCurrentIndex(6)
        elif self.stack_comboMethod.currentText() == "Otsu":
            self.stack.setCurrentIndex(0)
        elif self.stack_comboMethod.currentText() == "Yen":
            self.stack.setCurrentIndex(8)
        elif self.stack_comboMethod.currentText() == "Iso data":
            self.stack.setCurrentIndex(9)
        elif self.stack_comboMethod.currentText() == "Li":
            self.stack.setCurrentIndex(10)
        elif self.stack_comboMethod.currentText() == "Sauvola":
            self.stack.setCurrentIndex(11)
        else: 
            self.stack.setCurrentIndex(7)

    #pySlot -> local method
    def onSelectionMethod(self):
        if self.stack_comboMethod_mth.currentText() == "gaussian":
            self.label_local_param.show()
            self.spin_local_param.show()
        else :
            self.label_local_param.hide()
            self.spin_local_param.hide()

    #pySlot -> local method
    def onSelectionMode(self):
        if self.stack_comboMethod_mode.currentText() == "constant":
            self.label_cval.show()
            self.spin_cval.show()
        else :
            self.label_cval.hide()
            self.spin_cval.hide()

    #pySlot -> li method
    def OnLiDefaultChange(self):
        if self.li_check.isChecked():
            self.label_tolerence.hide()
            self.spin_tolerance.hide()
            self.label_initialguess.hide()
            self.spin_initialguess.hide()
        else :
            self.label_tolerence.show()
            self.spin_tolerance.show()
            self.label_initialguess.show()
            self.spin_initialguess.show()

    #pySlot -> sauvola method
    def OnSauvolaDefaultChange(self):
        if self.sauvola_check.isChecked():
            self.spin_r.hide()
        else :
            self.spin_r.show()

    def onApply(self):
        # Apply button clicked slot
        self.parameters.local_method = self.stack_comboMethod.currentText()
        if self.stack_comboMethod.currentText() == "Local":
            self.parameters.local_block_size = self.spin_block_size.value()
            self.parameters.local_offset = self.spin_offset.value()
            self.parameters.local_mth = self.stack_comboMethod_mth.currentText()
            self.parameters.local_mode = self.stack_comboMethod_mode.currentText()
            if self.stack_comboMethod_mode.currentText() == "constant":
                self.parameters.local_cval = self.spin_cval.value()
            else:   
                self.parameters.local_cval = 0
            if self.stack_comboMethod_mth.currentText() == "gaussian":
                self.parameters.local_param = self.spin_local_param.value()
            else:
                self.parameters.local_param = None
        elif self.stack_comboMethod.currentText() == "Niblack":
            self.parameters.niblackSauvola_window_size = self.spin_window_sizenb.value()
            self.parameters.niblackSauvola_k = self.spin_knb.value()
        elif self.stack_comboMethod.currentText() == "Triangle":
            self.parameters.triangle_nbins = self.spin_nbins.value()
        elif self.stack_comboMethod.currentText() == "Multi otsu":
            self.parameters.multiotsu_classes = self.spin_classes.value()
            self.parameters.multiotsu_nbins = self.spin_mo_nbins.value()
        elif self.stack_comboMethod.currentText() == "Hysteresis":
            self.parameters.hysteresis_low = self.spin_low.value()
            self.parameters.hysteresis_hight = self.spin_hight.value()
        elif self.stack_comboMethod.currentText() == "Minimum":
            self.parameters.minimum_maxiter = self.spin_maxiter.value()
            self.parameters.minimum_nbins = self.spin_nbinsmin.value()
        elif self.stack_comboMethod.currentText() == "Otsu":
            self.parameters.otsu_nbins = self.spin_nbinsOtsu.value()
        elif self.stack_comboMethod.currentText() == "Yen":
            self.parameters.yen_nbins = self.spin_nbinsYen.value()
        elif self.stack_comboMethod.currentText() == "Iso data":
            self.parameters.isodata_nbins = self.spin_nbinsIso.value()
        elif self.stack_comboMethod.currentText() == "Sauvola":
             if self.sauvola_check.isChecked():
                self.parameters.niblackSauvola_window_size = self.spin_window_size.value()
                self.parameters.niblackSauvola_k = self.spin_k.value()
                self.parameters.sauvola_r = None
             else:
                self.parameters.niblackSauvola_window_size = self.spin_window_size.value()
                self.parameters.niblackSauvola_k = self.spin_k.value()
                self.parameters.sauvola_r = self.spin_r.value()
        elif self.stack_comboMethod.currentText() == "Li":
            if self.li_check.isChecked():
                self.parameters.li_tolerance = None
                self.parameters.li_initialguess = None
            else:
                self.parameters.li_tolerance = self.spin_tolerance.value()
                self.parameters.li_initialguess = self.spin_initialguess.value()

        # Send signal to launch the process
        self.emitApply(self.parameters)


# --------------------
# - Factory class to build process widget object
# - Inherits dataprocess.CWidgetFactory from Ikomia API
# --------------------
class ThresholdWidgetFactory(dataprocess.CWidgetFactory):

    def __init__(self):
        dataprocess.CWidgetFactory.__init__(self)
        # Set the name of the process -> it must be the same as the one declared in the process factory class
        self.name = "skimage_threshold"

    def create(self, param):
        # Create widget object
        return ThresholdWidget(param, None)
