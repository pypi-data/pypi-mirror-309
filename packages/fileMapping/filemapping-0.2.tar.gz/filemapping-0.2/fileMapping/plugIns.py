import os

from fileMapping import pluginLoading

def pathConversion(cpath: os.path, path: os.path) -> os.path:
    """
    当要转化的文件目录在调用文件的临旁时,则可以用这个快速转化

    例：
    |--->
        |-> plugIns
        |-> x.py

    其中x.py要调用plugIns文件夹时即可快速调用

    pathConversion(__file__, "plugIns")
    :param cpath: __file__
    :param path: 必须为文件夹
    :return:
    """
    return os.path.join(os.path.dirname(cpath)if os.path.isfile(cpath)else cpath, os.path.abspath(path))


class File:
    callObject = {}
    invoke = {}
    def __init__(self, absolutePath: os.path, screening=None):
        """
        映射文件夹下的Python文件或者包
        :param absolutePath: 当前的根目录绝对路径
        :param screening: 要映射的文件夹
        """
        if screening is None:
            screening = ["py"]

        if not ((not os.path.isabs(absolutePath)) or (not os.path.islink(absolutePath))):
            raise FileNotFoundError(f"不是一个有效的绝对路径。: '{absolutePath}'")

        self.listOfFiles = {
            i.split('.')[0]: os.path.join(absolutePath, i) for i in os.listdir(absolutePath)
            if (i.split('.')[-1] in screening) and os.path.isfile(os.path.join(absolutePath, i))
        }

        for key, data in self.listOfFiles.items():
            self.callObject[key] = pluginLoading.f(data)
            # self.callObject[key].run()


    def run(self, *args, **kwargs):
        """
        运行映射文件
        :return:
        """
        for key, data in self.listOfFiles.items():
            self.callObject[key].run(*args, **kwargs)
            self.invoke[key] = self.callObject[key].pack


