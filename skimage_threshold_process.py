from ikomia import core, dataprocess
import copy
from skimage.filters import *
import cv2
import numpy as np


def float_or_none(s):
    if s == 'None':
        return None
    return float(s)

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

    def set_values(self, paramMap):
        # set parameters values from Ikomia application
        self.local_method = paramMap["local_method"]
        self.local_block_size = int(paramMap["local_block_size"])
        self.local_offset = int(paramMap["local_offset"])
        self.local_mth = paramMap["local_mth"]
        self.local_mode = paramMap["local_mode"]
        self.local_cval = int(paramMap["local_cval"])
        self.local_param = float_or_none(paramMap["local_param"])
        self.niblackSauvola_window_size = int(paramMap["niblackSauvola_window_size"])
        self.niblackSauvola_k = float(paramMap["niblackSauvola_k"])
        self.sauvola_r = float_or_none(paramMap["sauvola_r"])
        self.triangle_nbins = int(paramMap["triangle_nbins"])
        self.multiotsu_classes = int(paramMap["multiotsu_classes"])
        self.multiotsu_nbins = int(paramMap["multiotsu_nbins"])
        self.hysteresis_low = float(paramMap["hysteresis_low"])
        self.hysteresis_hight = float(paramMap["hysteresis_hight"])
        self.minimum_nbins = int(paramMap["minimum_nbins"])
        self.minimum_maxiter = int(paramMap["minimum_maxiter"])
        self.otsu_nbins = int(paramMap["otsu_nbins"])
        self.yen_nbins = int(paramMap["yen_nbins"])
        self.isodata_nbins = int(paramMap["isodata_nbins"])
        self.li_tolerance = float_or_none(paramMap["li_tolerance"])
        self.li_initialguess = float_or_none(paramMap["li_initialguess"])


    def get_values(self):
        # Send parameters values to Ikomia application
        paramMap = {}
        paramMap["local_method"] = self.local_method
        paramMap["local_block_size"] = str(self.local_block_size)
        paramMap["local_offset"] = str(self.local_offset)
        paramMap["local_mth"] = self.local_mth
        paramMap["local_mode"] = self.local_mode
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
            self.set_param_object(ThresholdParam())
        else:
            self.set_param_object(copy.deepcopy(param))

    def get_progress_steps(self):
        # Function returning the number of progress steps for this process
        # This is handled by the main progress bar of Ikomia application
        return 3

    def run(self):
        # Core function of your process
        self.begin_task_run()

        # Get input :
        input = self.get_input(0)

        # Get output :
        output = self.get_output(0)

        # Get parameters :
        param = self.get_param_object()

        # Get image from input/output (numpy array):
        srcImage = input.get_image()

        # Convert to grey Image if RGB
        if len(srcImage.shape) == 3:
            srcImage = cv2.cvtColor(srcImage, cv2.COLOR_RGB2GRAY)

        self.emit_step_progress()
            
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

        self.emit_step_progress()
        
        # Set image of input/output (numpy array):
        if param.local_method != "Multi otsu" and param.local_method != "Hysteresis":
            proc_img = (srcImage > thresh).astype(np.uint8) * 255
        
        output.set_image(proc_img)

         # Step progress bar:
        self.emit_step_progress()
        # Call end_task_run to finalize process
        self.end_task_run()


# --------------------
# - Factory class to build process object
# - Inherits dataprocess.CProcessFactory from Ikomia API
# --------------------
class ThresholdFactory(dataprocess.CTaskFactory):

    def __init__(self):
        dataprocess.CTaskFactory.__init__(self)
        # process information
        self.info.name = "skimage_threshold"
        self.info.short_description = "Compilation of well-known thresholding methods from scikit-image library."
        self.info.description = "Compilation of well-known thresholding methods from scikit-image library: " \
                                "Otsu, Multi-Otsu, Yen, IsoData, Li, Mean, Minimum, Local, Niblack, Sauvola " \
                                "Triangle, Hysteresis."
        self.info.authors = "Ikomia team"
        self.info.path = "Plugins/Python/Segmentation/Threshold"
        self.info.article = ""
        self.info.journal = ""
        self.info.year = 2020
        self.info.license = "MIT License"
        self.info.version = "1.0.1"
        self.info.repo = "https://github.com/Ikomia-dev/IkomiaPluginsPython"
        self.info.documentation_link = "https://scikit-image.org/docs/dev/api/skimage.filters.html"
        self.info.icon_path = "icons/scikit.png"
        self.info.keywords = "sci-kit,segmentation,threshold,otsu,yen,iso data,li,mean,minimum,local,niblack,sauvola,triangle,multi otsu,hysteresis"

    def create(self, param=None):
        # Create process object
        return Threshold(self.info.name, param)
