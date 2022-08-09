import datetime

class Process:
    def __init__(self, processId, processName,processUrl,createTime = datetime.datetime.now()) -> None:
        super().__init__()
        self.processId = processId
        self.processName = processName
        self.processUrl = processUrl
        self.createTime = createTime
