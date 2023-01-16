class Blog:
    count_id=0 #date and time identifier
    def __init__(self, title, content):
            Blog.count_id+=1
            self.__adminno = Blog.count_id
            self.__title = str(title)
            self.__content = str(content)

        # except ValueError:
        #     print("Value error while creating article")

    def setTitle(self, title):
        self.__title = self
    def setContent(self, content):
        self.__content = content

    def get_title_id(self):
        return self.__title

    def get_content_id(self):
        return self.__content

    def getId(self):
        return self.__adminno
