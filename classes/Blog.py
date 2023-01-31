from time import time
from datetime import datetime
from marko import convert


class Blog:
    def __init__(self, createdBy, title, content, coverImage=[]):
        self.id = self.id = int(time() * 1000)
        self.createdBy = createdBy
        self.updatedBy = None
        self.datetime = datetime.now()
        self.title = str(title)
        self.content = str(content)
        self.coverImage = coverImage


    def getId(self):
        return self.id

    def getCreatedBy(self):
        return self.createdBy

    def getUpdatedBy(self):
        return self.updatedBy

    def getTitle(self):
        return self.title

    def getContent(self):
        return self.content

    def getConvertedContent(self):
        return convert(self.content)

    def getCoverImage(self):
        return self.coverImage

    def setCreatedBy(self, createdBy):
        return self.createdBy

    def getUpdatedBy(self, updatedBy):
        return self.updatedBy

    def setTitle(self, title):
        self.title = title

    def setContent(self, content):
        self.content = content

    def setCoverImage(self, coverImage):
        self.coverImage = coverImage
