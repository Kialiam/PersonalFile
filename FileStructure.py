

import os
import xml.etree.ElementTree as ET


###---------------------------variable-------------------------------------------------######

TreePath     = "D:/Kialiam/Work/Personal/Script/ScriptBase/FileStructureTest.XML"
Root 		 = ET.parse( TreePath ).getroot( )

###---------------------------define-------------------------------------------------######

def SubFileBuild( nametag , dirpath , level = 0 ):

	for i in Root.findall(nametag) if type(nametag) == str else [nametag]:

		try:
			filetype = i.findall("SubFileType")[0].attrib.get("Type")
		except:
			filetype = 0

		for y in i.getchildren():     # element of x,include subfiletype

			## - for Label with "FileName", check it is exists, make a dir with value of filename 
			if y.tag == "FileName":
				###----------------variable---------------------######
				ObjectName = y.attrib.get("name")
				newdirpath = dirpath + "/" + ObjectName
				###----------------variable---------------------######
				if ObjectName not in os.listdir(dirpath+"/"):
					os.mkdir(newdirpath)
				## - if file exists, go next level with sub group label by loop tool "SubFileBuild"
				if filetype == "SpecificType":
					## - base on item name to find another label
					SubFileBuild( ObjectName , newdirpath , level = level +1 )
				elif filetype is not 0:
					## - base on file type to create child
					SubFileBuild( filetype , newdirpath , level = level +1 )

			## - for Label with "FileNumber", get the amount and create them
			if y.tag == "FileNumber":                 
				NUM = y.attrib.get("num")
				for x in range(int(NUM)):
					###----------------variable---------------------######
					ObjectName = "%s_sh%0.3d" %(i.attrib.get("name"),x+1)
					newdirpath = dirpath + "/" + ObjectName
					###----------------variable---------------------######
					if ObjectName not in os.listdir(dirpath+"/"):
						os.mkdir(newdirpath)
					if filetype is not 0:
						## - base on file type to create child
						SubFileBuild( filetype , newdirpath , level = level +1 )

			if len( y.getchildren() ) > 0:
				## - direcet create folder with child instead of another label
				SubFileBuild( y , newdirpath , level = level +1  )

							

###---------------------------variable-------------------------------------------------######

IROOTPATH    = "I:/"
PROJNAME     = "DS_B"
KROOTPATH    = "K:/"

IProjnamePath = IROOTPATH+PROJNAME#+"/"

KProjnamePath = KROOTPATH+PROJNAME

### Ensure ProjectName ###
###----------------------- I drive -------------------------------------###

if PROJNAME not in os.listdir(IROOTPATH):
	os.mkdir(IProjnamePath)


SubFileBuild("Category" , IProjnamePath )

###----------------------------- K drive ----------------------------------------------------###

if PROJNAME not in os.listdir(KROOTPATH):
	os.mkdir(KProjnamePath)

SubFileBuild("SceneFolder" , KProjnamePath )

###-----------------------------------------------------------------------------------------###




