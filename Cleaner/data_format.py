import xml.sax

class WikiData(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.title = ""
        self.ns = ""
        self.id = ""
        #self.revision.id = ""
        #self.revision.parent.id = ""

    def startElement(self,tag,attributes):
        self.CurrentData = tag
        if tag == "page":
            title = attributes["page"]
            print ("Title:",title)

    def endElement(self,tag):
        if self.CurrentData == "ns":
            print("NS:",self.ns)
        elif self.CurrentData == "id":
            print("ID:",self.id)
        #elif self.CurrentData == "revision":
            #print("Rev ID:",self.revision.id)

    def characters(self,tag):
        if self.CurrentData == "title":
            self.title = content
        elif self.CurrentData == "ns":
            self.ns = content
        #elif self.CurrentData == "revision":
            #self.revision.id = content

if __name__ == "__main__":

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # override the default ContextHandler
    Handler = WikiData()
    parser.setContentHandler( Handler )
    parser.parse("file1.xml")
