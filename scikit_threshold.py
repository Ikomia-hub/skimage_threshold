from ikomia import dataprocess


# --------------------
# - Interface class to integrate the process with Ikomia application
# - Inherits dataprocess.CPluginProcessInterface from Ikomia API
# --------------------
class scikit_threshold(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def getProcessFactory(self):
        # Instantiate process object
        from scikit_threshold.scikit_threshold_process import scikit_thresholdProcessFactory
        return scikit_thresholdProcessFactory()

    def getWidgetFactory(self):
        # Instantiate associated widget object
        from scikit_threshold.scikit_threshold_widget import scikit_thresholdWidgetFactory
        return scikit_thresholdWidgetFactory()
