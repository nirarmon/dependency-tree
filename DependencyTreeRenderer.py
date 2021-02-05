import abc


class IDependencyTreeRenderer(abc.ABC):
    @abc.abstractmethod
    def clear(self):
        pass
    @abc.abstractmethod
    def startNewLevel(self):
        pass
    @abc.abstractmethod
    def endLevel(self):
        pass
    @abc.abstractmethod
    def addNewEntry(self,entry):
        pass
    @abc.abstractmethod
    def render(self):
        pass

class HtmlTreeRenderer(IDependencyTreeRenderer):

    def __init__(self):
        self.__html = []
        self.__html.append('<ul>')
        self.__levelCounter = 1

    def clear(self):
        self.__html=[]
        self.__html.append('<ul>')
        self.__levelCounter = 1
    
    def startNewLevel(self):
        self.__html.append('<ul>')
        self.__levelCounter+=1

    def endLevel(self):
        if (self.__levelCounter>2):
            self.__html.append('</ul>')
            self.__levelCounter-=1

    def addNewEntry(self,entry):
        self.__html.append('<li>'+entry+'</li>')

    def render(self):
        for i in range(self.__levelCounter):
            self.__html.append('</ul>')
            self.__levelCounter-=1
        if self.__levelCounter!=0:
            raise RendererException('Level count is not 0, some level were not closed properly')
        return ''.join(self.__html) 

class RendererException(Exception):
    def __init__(self,message):
        self.message = message
        super().__init__(self.message)


# o= HtmlTreeRenderer()
# o.addNewEntry("first item")
# o.startNewLevel()
# o.addNewEntry("sub item")
# o.addNewEntry("sub item")
# o.startNewLevel()
# o.addNewEntry("sub sub item")
# o.endLevel()
# o.endLevel()
# print(o.render())

# try:
#     o.clear
#     o.startNewLevel()
#     o.endLevel()
#     o.endLevel()
#     o.render()
# except RendererException as error:
#     print(error)
