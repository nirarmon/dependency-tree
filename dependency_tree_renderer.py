import abc


class IdependencyTreeRenderer(abc.ABC):
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
    def render(self):
        pass
   
    @abc.abstractmethod
    def add_new_entry(self,entry_name,entry_level):
        pass


class HtmlTreeRenderer(IdependencyTreeRenderer):

    def __init__(self):
        self.__html = []
        self.__html.append('<ul>')
        self.__level_counter = 0

    def clear(self):
        self.__html=[]
        self.__html.append('<ul>')
        self.__level_counter = 0
    
    def start_new_level(self):
        self.__html.append('<ul>')
        self.__level_counter+=1

    def add_new_entry(self,entry_name,entry_level):
        if entry_level == self.__level_counter:
            self.__html.append('<li>'+entry_name+'</li>')
        if entry_level > self.__level_counter:
            self.__html.append((entry_level-self.__level_counter)*'<ul>')
            self.__html.append('<li>'+entry_name+'</li>')
        if entry_level < self.__level_counter:
            self.__html.append((self.__level_counter-entry_level)*'</ul>')
            self.__html.append('<li>'+entry_name+'</li>')
        self.__level_counter=entry_level


    def end_level(self):
        if (self.__level_counter>2):
            self.__html.append('</ul>')
            self.__level_counter-=1

    # def add_new_entry(self,entry):
    #     self.__html.append('<li>'+entry+'</li>')

    def render(self):
        for i in range(self.__level_counter):
            self.__html.append('</ul>')
            self.__level_counter -= 1
        tree_body = ''.join(self.__html)

        # wrap the tree with a small HTML page that uses jsTree for styling
        full_page = (
            "<!DOCTYPE html>"
            "<html>"
            "<head>"
            "<meta charset='UTF-8'>"
            "<title>Dependency Tree</title>"
            "<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.12/themes/default/style.min.css'/>"
            "<style>body{font-family:Arial,sans-serif;margin:20px;}</style>"
            "</head>"
            "<body>"
            "<form action='/packages' method='get' style='margin-bottom:20px;'>"
            "<input type='text' name='package' placeholder='Package name' required>"
            "<input type='text' name='version' value='latest'>"
            "<button type='submit'>Search</button>"
            "</form>"
            "<div id='tree'>" + tree_body + "</div>"
            "<script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js'></script>"
            "<script src='https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.12/jstree.min.js'></script>"
            "<script>$(function(){$('#tree').jstree();});</script>"
            "</body>"
            "</html>"
        )
        return full_page

class RendererException(Exception):
    def __init__(self,message):
        self.message = message
        super().__init__(self.message)
