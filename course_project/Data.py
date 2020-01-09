class Data:

    def __init__(self, time, data, t1=0, t2=0, filename="", size=None):
        self.time = time
        self.amplitude = data
        self.t1 = t1
        self.t2 = t2
        self.shot_number = 0
        self.filename = filename
        if size is None:
            self.size = len(time)
        else:
            self.size = size



    def copy(self):
        time = self.time.copy()
        amplitude = self.amplitude.copy()
        t1 = self.t1
        t2 = self.t2
        filename = self.filename
        size = self.size
        res = Data(time, amplitude, t1, t2, filename, size)
        return res

