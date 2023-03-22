from ikomia.core import task, ParamMap
import cv2
from ikomia.utils.tests import run_for_test
import logging
logger = logging.getLogger(__name__)


def test(t, data_dict):
    logger.info("===== Test::infer skimage morpho snakes =====")
    img = cv2.imread(data_dict["images"]["detection"]["coco"])[::-1]
    input_img = t.get_input(0)
    input_img.set_image(img)

    for method in ["Otsu", "Yen", "Iso data", "Li", "Mean", "Minimum", "Local", "Niblack", "Sauvola", "Triangle",
                   "Multi otsu", "Hysteresis"]:
        params = task.get_parameters(t)
        params["local_method"] = method
        task.set_parameters(t, params)
        yield run_for_test(t)
