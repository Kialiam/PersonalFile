

import os
import xml.etree.ElementTree as ET


###---------------------------variable-------------------------------------------------######

TreePath     = "D:/Kialiam/Work/Personal/Script/ScriptBase/FileStructureTest.XML"
Root 		 = ET.parse( TreePath ).getroot( )

###---------------------------define-------------------------------------------------######

def SubFileBuild( nametag , dirpath , level = 0 ):
	#print "nametag = %s ,%s" %(level,nametag)
	for i in Root.findall(nametag) if type(nametag) == str else [nametag]:
		#print "level = %s ,%s" %(level,i)
		try:
			filetype = []
			for x in i.findall("SubFileType"):
				filetype.append(x.attrib.get("Type"))
				#filetype = i.findall("SubFileType")[0]
		except:
			filetype = 0
		print "level = %s ,%s , %s" %(level,i,filetype)

		for y in i.getchildren():     # element of x,include subfiletype

			## - for Label with "FileName", check it is exists, make a dir with value of filename 
			if y.tag == "FileName":
				print "FileName = %s " %(y.attrib.get("name"))

				###----------------variable---------------------######
				ObjectName = y.attrib.get("name")
				newdirpath = dirpath + "/" + ObjectName
				###----------------variable---------------------######
				if ObjectName not in os.listdir(dirpath+"/"):
					os.mkdir(newdirpath)
				## - if file exists, go next level with sub group label by loop tool "SubFileBuild"
				if len(filetype) is not 0:
					for f_type in filetype:
						#print "level = %s ,%s" %(level,f_type)
						if f_type == "SPECIFICTYPE":
							print "SPECIFICTYPE = %s " %(f_type)
							## - base on item name to find another label
							SubFileBuild( ObjectName , newdirpath , level = level +1 )
						else:
							## - base on file type to create child
							SubFileBuild( f_type , newdirpath , level = level +1 )

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
							for f_type in filetype:
								#print "level = %s ,%s" %(level,f_type)
								if f_type == "SPECIFICTYPE":
									## - base on item name to find another label
									SubFileBuild( ObjectName , newdirpath , level = level +1 )
								else:
									## - base on file type to create child
									SubFileBuild( f_type , newdirpath , level = level +1 )

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

# if PROJNAME not in os.listdir(KROOTPATH):
# 	os.mkdir(KProjnamePath)

# SubFileBuild("SceneFolder" , KProjnamePath )

###-----------------------------------------------------------------------------------------###




