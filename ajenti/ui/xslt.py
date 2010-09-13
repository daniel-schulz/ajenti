from lxml import etree
from lxml.etree import *

xslt = None

def attr(_, v, d):
    #print 'att',v,d
    return d if v == [] else v[0]

def css(_, v, d):
    #print 'css',v,d
    v = d if v == [] else v[0]
    if v == 'auto': 
        return v
    #print v if '%' in v else '%spx'%v
    return v if '%' in v else '%spx'%v

def iif(_, q, a, b):
    return a if len(q)>0 and q[0].lower() == 'true' else b
    

class Selector(etree.XSLTExtension):
    def execute(self, context, self_node, input_node, output_parent):
        print input_node.getchildren()
        child = input_node[int(self_node.get('index'))]
        results = self.apply_templates(context, child)
        output_parent.append(results[0])
        
       
def prepare(includes):
    global xslt
    xml = XSLT % ''.join([open(x).read() for x in includes])
    ex = {
        ('ext', 'attr') : attr,
        ('ext', 'iif') : iif,
        ('ext', 'node') : Selector(),
        ('ext', 'css') : css
    }
    xslt = etree.XSLT(etree.fromstring(xml), extensions=ex)
        
def render(templ):
    global xslt
    return DT + etree.tostring(xslt(xslt(templ))) #!!!
    
    
DT = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
"""
    
XSLT="""
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:x="ext"
    extension-element-prefixes="x">
    
  <xsl:output method="html" indent="yes" encoding="UTF-8"/>
  
  <xsl:template match="@*|node()">
     <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
     </xsl:copy>
  </xsl:template>

  <xsl:template match="html">
      <html xmlns="http://www.w3.org/1999/xhtml">
          <xsl:apply-templates />
      </html>
  </xsl:template>

  <xsl:template match="xml">
      <xsl:apply-templates />
  </xsl:template>
  
  <xsl:template match="headstylesheets">
     <xsl:for-each select="headstylesheet">
         <link href="{@href}" rel="stylesheet" media="all" />
     </xsl:for-each>
  </xsl:template>

  <xsl:template match="headscripts">
     <xsl:for-each select="headscript">
         <script src="{@href}">
            <xsl:text> </xsl:text>
         </script>
     </xsl:for-each>
  </xsl:template>
  
  %s
  
</xsl:stylesheet>  
"""



