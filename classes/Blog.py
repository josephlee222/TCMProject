from datetime import datetime
from time import time

from marko import convert


class Blog:
    def __init__(self, createdBy, title, content, brief, coverImage=[]):
        self.id = int(time() * 1000)
        self.createdBy = createdBy
        self.updatedBy = None
        self.datetime = datetime.now()
        self.title = str(title)
        self.content = str(content)
        self.brief = str(brief)
        self.coverImage = coverImage

    def getId(self):
        return self.id

    def getCreatedBy(self):
        return self.createdBy

    def getUpdatedBy(self):
        return self.updatedBy

    def getTitle(self):
        return self.title

    def getBrief(self):
        return self.brief

    def getContent(self):
        return self.content

    def getConvertedContent(self):
        return convert(self.content)

    def getCoverImage(self):
        return self.coverImage

    def getDatetime(self):
        return self.datetime

    def setCreatedBy(self, createdBy):
        self.createdBy = createdBy

    def setUpdatedBy(self, updatedBy):
        self.updatedBy = updatedBy

    def setTitle(self, title):
        self.title = title

    def setBrief(self, brief):
        self.brief = brief

    def setContent(self, content):
        self.content = content

    def setCoverImage(self, coverImage):
        self.coverImage = coverImage
