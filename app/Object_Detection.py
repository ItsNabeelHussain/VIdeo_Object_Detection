import glob
import logging
import os
import re

import torch

from app import Images_from_Video


class DetectObject:
    """
    Detect Object in Images.
    """

    def __init__(self):
        self.__frames_time = {}
        self.__model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)
        self.response = {}
        """
                Create and configure logger
                """
        logging.basicConfig(filename="newfile.log",
                            format='%(asctime)s %(message)s',
                            filemode='w')
        """
        Creating an object
        """
        self.logger = logging.getLogger()
        """
        Setting the threshold of logger to DEBUG
        """
        self.logger.setLevel(logging.DEBUG)
        self.__result_list = []  # List of DataFrame

    def dir_handling(self):
        """
        delete all images in these directories
        else create new directory
        """
        path = os.path.dirname(os.path.abspath(__file__)) + '/' + "processed/"
        if os.path.isdir(path):
            for f in os.listdir(path):
                os.remove(os.path.join(path, f))
        else:
            os.makedirs(path)

        dir = os.path.dirname(os.path.abspath(__file__)) + '/' + "original_frames/"
        if os.path.isdir(dir):
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))
        else:
            os.mkdir(dir)

    def video_to_images(self, f_name):
        self.dir_handling()
        """
        :param video filename:
        :return processed images:
        """
        img = Images_from_Video.ImagesFromVideo(self.logger,
                                                f_name)
        cam = img.readfile()
        self.__frames_time = img.get_frames_times(cam)

        if "Error Message" in self.__frames_time:
            return self.__frames_time
        img.processing(cam)
        img.detect_duplicate_images()
        images = glob.glob(os.path.dirname(os.path.abspath(__file__)) + '/' +
                           "processed/*.jpg")
        return images



    def get_Processed_frames_name(self):
        try:
            path = os.path.dirname(os.path.abspath(__file__)) + '/' + "processed/"
            images = glob.glob(path + "*.jpg")
            return images
        except Exception as e:
            self.logger.error(e)

    def detect_objects(self, image):
        """
        Take Image and return detected objects information.
        Parameters:
            image:
        Returns:
        """
        total = 0
        classes_count = {}
        for slice in range(0, len(image), 100):

            if slice + 100 < len(image):
                result = self.__model(image[slice:slice + 100])
                self.__result_list.extend(result.pandas().xyxy)
            else:
                result = self.__model(image[slice:])
                self.__result_list.extend(result.pandas().xyxy)

        for frame_id, frame in enumerate(self.__result_list):
            detected_classes = set(frame['name'])
            list_objects = list(frame['name'])
            for obj in detected_classes:
                time = []
                frames_name = []
                regex = re.compile(r'(\d+|\s+)')
                name = int(regex.split(image[frame_id])[-2])
                initial_time = round(name / self.__frames_time["frames_per_second"], 2)
                end_time = round((name + 1) / self.__frames_time["frames_per_second"], 2)
                if obj in classes_count:
                    classes_count[obj] += list_objects.count(obj)
                    time = self.response[obj]["time"]
                    frames_name = self.response[obj]["frames"]
                else:
                    self.response[obj] = {}
                    classes_count[obj] = list_objects.count(obj)

                time.append([initial_time, end_time])
                frames_name.append(image[frame_id])
                self.response[obj]["time"] = time
                self.response[obj]["frames"] = frames_name
                total += list_objects.count(obj)

        classes_count['All'] = total

        return {'video_duration': self.__frames_time["video_time"],
                'objects_count': classes_count, 'objects_loc': self.response}
