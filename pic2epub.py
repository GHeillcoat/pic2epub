# encoding:utf-8
# !/usr/bin/python3


import zipfile
import os.path

'''
ePub文件的目录&结构
mimetype
META_INF/
    container.xml
OBBPS/
    content.opf
    title.html
    stylesheet.css
    toc.ncx
images/
    cover.png
'''

container_template = '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
    <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
      <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
      </rootfiles>
  </container>
    '''
content_template = '''
   <?xml version="1.0" encoding="utf-8" standalone="no"?>
   <package xmlns="http://www.idpf.org/2007/opf" 
            xmlns:dc="http://purl.org/dc/elements/1.1/" 
            unique-identifier="bookid" version="2.0">
     <metadata>
       <dc:title>书山有路勤为径,学海无涯苦作舟</dc:title>
       <dc:creator>Auntilz</dc:creator>
       <dc:identifier id="bookid">urn:uuid:12345</dc:identifier>
       <meta name="cover" content="cover-image" />
     </metadata>
     <manifest>
         %(manifest)s
       <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
       <item id="content" href="content.html" media-type="application/xhtml+xml"/>
       <item id="css" href="Styles/stylesheet.css" media-type="text/css"/>
     </manifest>
     <spine toc="ncx">
         %(spine)s
       <itemref idref="cover" linear="no"/>
       <itemref idref="content"/>
     </spine>
     <guide>
       <reference href="cover.html" type="cover" title="Cover"/>
     </guide>
   </package>
   '''
nav_template='''<navPoint id="navPoint-%(id)d" playOrder="%(id)d">
      <navLabel>
        <text>%(dir)s</text>
      </navLabel>
      <content src="Text/%(html_filname)s"/>
    </navPoint>'''

toc_template = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
   "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">

<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:12345"/>
    <meta name="dtb:depth" content="2"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>%(title)s</text>
  </docTitle>
  <navMap>
    %(navList)s
  </navMap>
</ncx>
'''
dir_temple = '''
<div class="sgc-toc-level-1">
  <a href=%(html_filname)s>%(dir)s</a>
</div>
'''


toc_html_template = '''
    <?xml version="1.0"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
   "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Contents</title>
<link href="../sgc-toc.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<h1 align="center">%(title)s</h1>
<h3 align="center">由脚本自动生成&nbsp;by:Auntilz</h3>
<h6 align="center">参考：https://blog.csdn.net/qq_40036519/article/details/121737221</h6>
</body></html>
'''

class epub:
    def __init__(self, title):
        self.title = title
        # acreate zip file
        path = os.path.dirname(os.path.realpath(__file__))+"\\output\\"
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        self.epubFile = zipfile.ZipFile('%s.epub' % title, 'w')
        self.manifest = ''
        self.spine = ''
        self.toc_navList = ''
        self.id = 0
        self.dirList = ''
        self.manifest += '<item id="TOC.xhtml" href="Text/TOC.xhtml" media-type="application/xhtml+xml"/>'
        self.spine += '<itemref idref="TOC.xhtml"/>'
        self.create_mimetype()
        self.create_container()
        self.create_stylesheet()
    def setAutho(self, autho):
        self.autho = autho
    def setType(self, type):
        self.type = type
    def addFile(self, html_content, dir):
        # 构造文件，创建html
        html_filname = "%s.html" % dir
        html_fd = os.open(html_filname, os.O_RDWR|os.O_CREAT )
        os.write(html_fd, bytes(html_content, encoding = "utf-8"))
        os.close(html_fd)
        self.manifest += '<item id="%s" href="Text/%s" media-type="application/xhtml+xml"/>' % (html_filname, html_filname)
        self.spine += '<itemref idref="%s"/>' % (html_filname)
        self.id = self.id + 1
        self.toc_navList += nav_template % {"id": self.id, "dir": dir, "html_filname" : html_filname}

        #print("html_filname:", html_filname)
        #print("toc_navList:", self.toc_navList)


        self.dirList += dir_temple % {"html_filname" : html_filname, "dir": dir}
        self.epubFile.write(html_filname, 'OEBPS/Text/' + html_filname, compress_type=zipfile.ZIP_DEFLATED)
        #删除临时文件
        os.remove(html_filname)
    def close(self):
        # save zip file
        self.create_toc()
        self.create_content_file()
        #self.create_pic(filePath)
        self.epubFile.close()
    def create_mimetype(self):
        self.epubFile.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
    def create_pic(self,filePath):
        txt=""
        dir=os.listdir(filePath)
        dir.sort()
        for i in dir:
            with open(filePath+"/"+i,'rb') as f:
                    pic=f.read()
                    txt=txt+'''<img alt="图像" src="../../%s" />'''%i+"\n"
                    self.epubFile.writestr(i, pic, compress_type=zipfile.ZIP_STORED)
                    f.close()
        self.addFile(txt, self.title)
    def create_container(self):
        self.epubFile.writestr('META-INF/container.xml', container_template, compress_type=zipfile.ZIP_STORED)
    def create_toc(self):
        self.epubFile.writestr('OEBPS/toc.ncx', toc_template % {"title": self.title, "navList": self.toc_navList}, compress_type=zipfile.ZIP_STORED)
        self.epubFile.writestr('OEBPS/Text/TOC.xhtml', toc_html_template % {"title": self.title}, compress_type=zipfile.ZIP_STORED)
    def create_content_file(self):
        self.epubFile.writestr('OEBPS/content.opf', content_template % {
            'manifest': self.manifest,
            'spine': self.spine, },
                      compress_type=zipfile.ZIP_STORED)

    def create_stylesheet(self):
        css_info = '''
            body {
              font-family: sans-serif;     
            }
            h1,h2,h3,h4 {
              font-family: serif;     
              color: red;
            }
        '''
        self.epubFile.writestr('OEBPS/Styles/stylesheet.css', css_info, compress_type=zipfile.ZIP_STORED)
def create_epub():
  fileName=input("给文件起个名吧：\n")
  epubObj = epub(fileName)
  filePath=input("欲合并图片的文件夹路径：\n")
  epubObj.create_pic(filePath)
  epubObj.close()
def lot_create_epub():
  filePath=input("欲合并图片的文件夹路径：\n")
  fileList=os.listdir(filePath)
  fileList.sort()
  for i in fileList:
    epubObj = epub(i)
    epubObj.create_pic(filePath+"/"+i)
    epubObj.close()

    
'''if __name__ == '__main__':
  print("1.单个文件生成epub\n2.批量生成epub")
  choice=input("请输入选择：\n")
  if choice=="1":
    create_epub()
  elif choice=="2":
    lot_create_epub()'''