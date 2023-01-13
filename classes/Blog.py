class Blog:
    def __init__(self, title, content):
        try:
            self.title = str(title)
            self.content = str(content)

        except ValueError:
            print("Value error while creating article")

    def setTitle(self, title):
        self.title = self
    def setContent(self, content):
        self.content = content
