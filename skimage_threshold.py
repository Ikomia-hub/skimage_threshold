from ikomia import dataprocess


# --------------------
# - Interface class to integrate the process with Ikomia application
# - Inherits dataprocess.CPluginProcessInterface from Ikomia API
# --------------------
class IkomiaPlugin(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def getProcessFactory(self):
        # Instantiate process object
        from skimage_threshold.skimage_threshold_process import ThresholdFactory
        return ThresholdFactory()

    def getWidgetFactory(self):
        # Instantiate associated widget object
        from skimage_threshold.skimage_threshold_widget import ThresholdWidgetFactory
        return ThresholdWidgetFactory()
