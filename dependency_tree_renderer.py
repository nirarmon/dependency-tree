import abc


class Idependency_tree_renderer(abc.ABC):
    @abc.abstractmethod
    def clear(self):
        pass
    @abc.abstractmethod
    def start_new_level(self):
        pass
    @abc.abstractmethod
    def end_level(self):
        pass
    @abc.abstractmethod
    def add_new_entry(self,entry):
        pass
    @abc.abstractmethod
    def render(self):
        pass

class HtmlTreeRenderer(Idependency_tree_renderer):

    def __init__(self):
        self.__html = []
        self.__html.append('<ul>')
        self.__level_counter = 1

    def clear(self):
        self.__html=[]
        self.__html.append('<ul>')
        self.__level_counter = 1
    
    def start_new_level(self):
        self.__html.append('<ul>')
        self.__level_counter+=1

    def end_level(self):
        if (self.__level_counter>2):
            self.__html.append('</ul>')
            self.__level_counter-=1

    def add_new_entry(self,entry):
        self.__html.append('<li>'+entry+'</li>')

    def render(self):
        for i in range(self.__level_counter):
            self.__html.append('</ul>')
            self.__level_counter-=1
        if self.__level_counter!=0:
            raise RendererException('Level count is not 0, some level were not closed properly')
        return ''.join(self.__html) 

class RendererException(Exception):
    def __init__(self,message):
        self.message = message
        super().__init__(self.message)
