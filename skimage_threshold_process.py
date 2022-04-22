from ikomia import core, dataprocess
import copy
from skimage.filters import *
import cv2
import numpy as np


# --------------------
# - Class to handle the process parameters
# - Inherits core.CProtocolTaskParam from Ikomia API
# --------------------
class ThresholdParam(core.CWorkflowTaskParam):

    def __init__(self):
        core.CWorkflowTaskParam.__init__(self)
        # parameters
        self.local_method = "Otsu"
        self.local_block_size = 35
        self.local_mth = "gaussian"
        self.local_offset = 0
        self.local_mode = "reflect"
        self.local_param = None
        self.local_cval = 0
        self.niblackSauvola_window_size = 15
        self.niblackSauvola_k = 0.2
        self.sauvola_r = None
        self.triangle_nbins = 256
        self.multiotsu_classes = 3
        self.multiotsu_nbins = 256
        self.hysteresis_low = 0.1
        self.hysteresis_hight = 0.35
        self.minimum_nbins = 256
        self.minimum_maxiter = 10000
        self.otsu_nbins = 256
        self.yen_nbins = 256
        self.isodata_nbins = 256
        self.li_tolerance = None
        self.li_initialguess = None

    def setParamMap(self, paramMap):
        # set parameters values from Ikomia application
        self.local_method = int(paramMap["local_method"])
        self.local_block_size = int(paramMap["local_block_size"])
        self.local_offset = int(paramMap["local_offset"])
        self.local_mth = int(paramMap["local_mth"])
        self.local_mode = int(paramMap["local_mode"])
        self.local_cval = int(paramMap["local_cval"])
        self.local_param = int(paramMap["local_param"])
        self.niblackSauvola_window_size = int(paramMap["niblackSauvola_window_size"])
        self.niblackSauvola_k = int(paramMap["niblackSauvola_k"])
        self.sauvola_r = int(paramMap["sauvola_r"])
        self.triangle_nbins = int(paramMap["triangle_nbins"])
        self.multiotsu_classes = int(paramMap["multiotsu_classes"])
        self.multiotsu_nbins = int(paramMap["multiotsu_nbins"])
        self.hysteresis_low = int(paramMap["hysteresis_low"])
        self.hysteresis_hight = int(paramMap["hysteresis_hight"])
        self.minimum_nbins = int(paramMap["minimum_nbins"])
        self.minimum_maxiter = int(paramMap["minimum_maxiter"])
        self.otsu_nbins = int(paramMap["otsu_nbins"])
        self.yen_nbins = int(paramMap["yen_nbins"])
        self.isodata_nbins = int(paramMap["isodata_nbins"])
        self.li_tolerance = int(paramMap["li_tolerance"])
        self.li_initialguess = int(paramMap["li_initialguess"])


    def getParamMap(self):
        # Send parameters values to Ikomia application
        paramMap = core.ParamMap()
        paramMap["local_method"] = str(self.local_method)
        paramMap["local_block_size"] = str(self.local_block_size)
        paramMap["local_offset"] = str(self.local_offset)
        paramMap["local_mth"] = str(self.local_mth)
        paramMap["local_mode"] = str(self.local_mode)
        paramMap["local_cval"] = str(self.local_cval)
        paramMap["local_param"] = str(self.local_param)
        paramMap["niblackSauvola_window_size"] = str(self.niblackSauvola_window_size)
        paramMap["niblackSauvola_k"] = str(self.niblackSauvola_k)
        paramMap["sauvola_r"] = str(self.sauvola_r)
        paramMap["triangle_nbins"] = str(self.triangle_nbins)
        paramMap["multiotsu_classes"] = str(self.multiotsu_classes)
        paramMap["multiotsu_nbins"] = str(self.multiotsu_nbins)
        paramMap["hysteresis_low"] = str(self.hysteresis_low)
        paramMap["hysteresis_hight"] = str(self.hysteresis_hight)
        paramMap["minimum_nbins"] = str(self.minimum_nbins)
        paramMap["minimum_maxiter"] = str(self.minimum_maxiter)
        paramMap["otsu_nbins"] = str(self.otsu_nbins)
        paramMap["yen_nbins"] = str(self.yen_nbins)
        paramMap["isodata_nbins"] = str(self.isodata_nbins)
        paramMap["li_tolerance"] = str(self.li_tolerance)
        paramMap["li_initialguess"] = str(self.li_initialguess)
        return paramMap


# --------------------
# - Class which implements the process
# - Inherits core.CProtocolTask or derived from Ikomia API
# --------------------
class Threshold(dataprocess.C2dImageTask):

    def __init__(self, name, param):
        dataprocess.C2dImageTask.__init__(self, name)

        if param is None:
            self.setParam(ThresholdParam())
        else:
            self.setParam(copy.deepcopy(param))

    def getProgressSteps(self):
        # Function returning the number of progress steps for this process
        # This is handled by the main progress bar of Ikomia application
        return 3

    def run(self):
        # Core function of your process
        self.beginTaskRun()

        # Get input :
        input = self.getInput(0)

        # Get output :
        output = self.getOutput(0)

        # Get parameters :
        param = self.getParam()

        # Get image from input/output (numpy array):
        srcImage = input.getImage()

        # Convert to grey Image if RGB
        if len(srcImage.shape) == 3:
            srcImage = cv2.cvtColor(srcImage, cv2.COLOR_RGB2GRAY)

        self.emitStepProgress()
            
        # threshold methods
        if param.local_method == "Otsu":
            thresh = threshold_otsu(srcImage, nbins=param.otsu_nbins)
        elif param.local_method == "Yen":
            thresh = threshold_yen(srcImage, nbins=param.yen_nbins)
        elif param.local_method == "Iso data":
            thresh = threshold_isodata(srcImage, nbins=param.isodata_nbins, return_all=False)
        elif param.local_method == "Li":
            thresh = threshold_li(srcImage, tolerance=param.li_tolerance, initial_guess=param.li_initialguess, iter_callback=None)
        elif param.local_method == "Mean":
            thresh = threshold_mean(srcImage)
        elif param.local_method == "Minimum":
            thresh = threshold_minimum(srcImage, nbins=param.minimum_nbins, max_iter=param.minimum_maxiter)
        elif param.local_method == "Local":
            thresh = threshold_local(srcImage, param.local_block_size, method=param.local_mth, offset=param.local_offset, mode=param.local_mode, param=param.local_param, cval=param.local_cval)
        elif param.local_method == "Niblack":
            thresh = threshold_niblack(srcImage, window_size=param.niblackSauvola_window_size, k=param.niblackSauvola_k)
        elif param.local_method == "Sauvola":
            thresh = threshold_sauvola(srcImage, window_size=param.niblackSauvola_window_size, k=param.niblackSauvola_k, r=param.sauvola_r)
        elif param.local_method == "Triangle":
            thresh = threshold_triangle(srcImage, param.triangle_nbins)
        elif param.local_method == "Multi otsu":
            thresh = threshold_multiotsu(srcImage, param.multiotsu_classes, param.multiotsu_nbins)
            proc_img = np.digitize(srcImage, bins=thresh)
        elif param.local_method == "Hysteresis":
            edges = sobel(srcImage)
            hight = (edges > param.hysteresis_hight).astype(int)
            low = (edges > param.hysteresis_low).astype(int)
            hyst = apply_hysteresis_threshold(edges, param.hysteresis_low, param.hysteresis_hight)
            proc_img = hight + hyst

        self.emitStepProgress()
        
        # Set image of input/output (numpy array):
        if param.local_method != "Multi otsu" and param.local_method != "Hysteresis":
            proc_img = (srcImage > thresh).astype(np.uint8) * 255
        
        output.setImage(proc_img)

         # Step progress bar:
        self.emitStepProgress()
        # Call endTaskRun to finalize process
        self.endTaskRun()


# --------------------
# - Factory class to build process object
# - Inherits dataprocess.CProcessFactory from Ikomia API
# --------------------
class ThresholdFactory(dataprocess.CTaskFactory):

    def __init__(self):
        dataprocess.CTaskFactory.__init__(self)
        # process information
        self.info.name = "skimage_threshold"
        self.info.shortDescription = "Compilation of well-known thresholding methods from scikit-image library."
        self.info.description = "Compilation of well-known thresholding methods from scikit-image library: " \
                                "Otsu, Multi-Otsu, Yen, IsoData, Li, Mean, Minimum, Local, Niblack, Sauvola " \
                                "Triangle, Hysteresis."
        self.info.authors = "Ikomia team"
        self.info.path = "Plugins/Python/Segmentation/Threshold"
        self.info.article = ""
        self.info.journal = ""
        self.info.year = 2020
        self.info.license = "MIT License"
        self.info.version = "1.0.0"
        self.info.repo = "https://github.com/Ikomia-dev/IkomiaPluginsPython"
        self.info.documentationLink = "https://scikit-image.org/docs/dev/api/skimage.filters.html"
        self.info.iconPath = "icons/scikit.png"
        self.info.keywords = "sci-kit,segmentation,threshold,otsu,yen,iso data,li,mean,minimum,local,niblack,sauvola,triangle,multi otsu,hysteresis"

    def create(self, param=None):
        # Create process object
        return Threshold(self.info.name, param)
