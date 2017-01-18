
import maya.cmds as cmds
import maya.mel as mel
import os,socket,time
import xml.etree.ElementTree as ET
import subprocess

#### ----------variable---------- #######
LocalBase       = "L:/"
ServerBase      = "I:/"
XMLPath         = "L:\DS_B\CHAR\Liam\Modeling\\"
CompareTool     = "D:\\Kialiam\\Work\\Personal\\Script\\ScriptBase\\PicCompareExternalExec.py"

#### ------- copyFile ------------ #######
def copyfile(source,dest):
	dst = open(dest,'wb')
	src = open(source,'rb')
	dst.write(src.read() )
	dst.close()
	src.close()

#### ------- prettyPrintXML ------------ #######	
def prettyPrintXML(elem, level = 0):
	i = '\n' + level * '    '
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + '   '
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for elem in elem:
			prettyPrintXML(elem, level + 1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and ( not elem.tail or not elem.tail.strip() ):
			elem.tail = i
	
#### ------- AvoidExistsFolder ------------ #######		
def AvoidExistsFolder( File , localFile , CompareTool ):
	
	#### ------variable----- #######
	i      = True
	num    = 0
	ext    = File.rsplit(".",1)[-1]
	Name   = File.rsplit(".",1)[0]
	CompareTool = CompareTool
	
	#### ------variable----- #######
	################################
	if len(Name.rsplit("_",1)[-1]) == 2:
		Name = Name.rsplit("_",1)[0]
		
	TempF = Name
	while i == True:
		if os.path.exists( Name+".%s" %ext ):
			if Name.rsplit("/",1)[0] != localFile.rsplit("/",1)[0]:
				import subprocess
				if "True" in subprocess.check_output([ "python" , CompareTool , Name+".%s" %ext , localFile ]):
					i = False
					Name = Name
				else:
					i = True
					num += 1
					Name = TempF+"_%0.2d" %num
			else:
				i = False
				Name = Name 
		else:
			i = False
			Name = Name
 
	if Name.rsplit("/",1)[-1] +"."+ext != localFile.rsplit("/",1)[-1]:
		print "%s \nSaved as %s.%s\n" %(localFile.rsplit("/",1)[-1],Name,ext)
	else:
		print "%s \nSaved as %s.%s\n" %( Name.rsplit("/",1)[-1]+"."+ext,Name,ext)
	return Name+".%s" %ext

#### ----------variable---------- #######
ScencePath      = cmds.file( query=True,sceneName=True )
NewScencePath   = ScencePath.replace( LocalBase , ServerBase )
TexturePathBase = NewScencePath.rsplit("/",2)[0] + "/Texture/"
ReferenceFile   = []
LatestVer       = 0

if os.path.isdir( "L:/DS_B/" ):

	if LocalBase == ScencePath[:3] and ScencePath.rsplit("/",3)[1] in ScencePath.rsplit("/",3)[-1] and "DS_B" == ScencePath.split("/",2)[1]:

		##  --- GetFileNameVersionInfo ---- ## 
		mayafileName = ScencePath.rsplit("/")[-1].rsplit(".")[0]
		NameNoVerNum = mayafileName.rsplit("_")[0] if mayafileName.rsplit("_")[-1].replace("v","",1).isdigit() else mayafileName  
		mayafileVer  = mayafileName.rsplit("_")[-1] if mayafileName.rsplit("_")[-1].replace("v","",1).isdigit() else mayafileName 
		VerNumber    = int( mayafileVer[1:] ) if mayafileVer[1:].isdigit() else "noVerNum"
		currentNum   = int(mayafileVer[1:]) if mayafileVer[1:].isdigit() else 1
		listDir      = filter( lambda x : ".ma" in x[-3:] , os.listdir( NewScencePath.rsplit("/",1)[0]+"/" ) )

		##  --- GetFileVersionInfo ---- ## 
		ExistFileVer = []
		for x in listDir:
			if len( x[:-3].rsplit("_")[-1] ) <= 4 and "v" in x[:-3].rsplit("_")[-1] and x[:-3].rsplit("_")[-1][1:].isdigit():
				ExistFileVer.append( int( x[:-3].rsplit("_")[-1][1:] ) )

		if ScencePath[:2] != ServerBase[:-1]:
			if ( len( mayafileVer ) == 4 ) and ( mayafileVer[0] == "v"  ) and ( str(VerNumber).isdigit() ):
				currentNum = VerNumber
			if len(ExistFileVer) > 0:
				LatestNum = reduce(lambda x,y: x if x > y else y , ExistFileVer )
				if LatestNum >= currentNum:
					currentNum = LatestNum + 1

			NewMayaFielName = NameNoVerNum + "_v%0.3d.ma" %currentNum
			
		##  --- GetTexturePathAndConnections ---- ## 
		TextureConnection = {}
		for x in cmds.ls( type = "file" ):
			localPath  = cmds.getAttr("%s.fileTextureName" %x )
			serverPath = TexturePathBase + localPath.rsplit("/",1)[-1]
			serverPath = AvoidExistsFolder( serverPath , localPath , CompareTool )
			TextureConnection["%s.fileTextureName" %x] = [localPath , serverPath]

		## ----------- GetFileReferenceInfo ------------------ ###   
		ReferenceFile.extend(cmds.ls(rf=True))
		ReferencePath = map(lambda x: cmds.referenceQuery( x, filename=True ) , ReferenceFile )


		##  --- writing log ---- ##   
		FileType        = NewScencePath.rsplit("/",2)[1]
		Name            = NewScencePath.rsplit("/",3)[1]
		NewMayaFielName = NewMayaFielName
		AllTexture      = [x[1] for x in TextureConnection.values()]
		AllReference    = ReferencePath
		VersionNum      = "v%0.2d" %currentNum
		UpdatedUser     = socket.gethostname()
		TimeAndDate     = time.strftime('%H:%M %a %y%m%d')

		## -------------- building XML ---------------- ##
		XMLFile = "Log_%s.xml" %TimeAndDate.rsplit(" ",1)[-1]

		LatestLogs = [x for x in os.listdir( XMLPath.rsplit("\\",1)[0] ) if "Log_" in x ]
		LatestLog  = reduce(lambda x,y : x if x.rsplit("_")[-1].split(".")[0] > y.rsplit("_")[-1].split(".")[0] else y , LatestLogs ) if LatestLogs else None
		if LatestLog:
			tree = ET.parse( XMLPath + "\\" + LatestLog )
			Root = tree.getroot()
		else:
			Root = ET.Element( XMLFile[:-4] )

		Root.tag = XMLFile[:-4]  

		F_Typ    = [x for x in Root.findall("FileType") if "Modeling" == x.attrib.get("name")]
		if not len(F_Typ):
			F_Typ = ET.SubElement( Root,"FileType" )
			F_Typ.set( "name",FileType )
			
		else:
		   
			F_Typ = F_Typ[0]
			
		## --- AvoidExistedObjectName ---- ##
		if len(F_Typ.findall(Name)):
			LatestVer = int(F_Typ.find(Name).attrib.get("ver")[1:])
			F_Typ.remove(F_Typ.find(Name))

		## --- WriteObjectName ---- ##
		F_Nm     = ET.SubElement( F_Typ,Name ) ;F_Nm.set( "ver",VersionNum )

		## --- WriteTextureAndReference ---- ##
		Txtr     = ET.SubElement( F_Nm,"LinkedTexture" ) if len( AllTexture ) > 0 else None
		[Txtr.set( "name%s"%str(y+1),x ) for x,y in zip( AllTexture,range( len(AllTexture) ) )]if len( AllTexture )>0 else None
		Rfrnc    = ET.SubElement( F_Nm,"LinkedReference" )if len( AllReference ) > 0 else None
		[Rfrnc.set( "name%s"%str(y+1),x ) for x,y in zip( AllReference,range( len(AllReference) ) )]if len( AllReference )>0 else None

		## --- WriteUserAndTime ---- ##
		ET.SubElement( F_Nm,"Updateder" ).set( "name",UpdatedUser )
		ET.SubElement( F_Nm,"Time" ).set( "name", TimeAndDate )

		prettyPrintXML( Root )
		Tree = ET.ElementTree( Root ) 

		if LatestVer < currentNum:
			## --- Writing ---- ##
			Tree.write( XMLPath+"\\"+XMLFile , encoding = 'utf-8' )

			## ------------ action -------- ##
			cmds.file( rename = ScencePath.rsplit("/",1)[0] + "/" + NewMayaFielName  )
			cmds.file( save = True, type = 'mayaAscii' )

			map(lambda x: copyfile( TextureConnection[x][0] , TextureConnection[x][1] ) if TextureConnection[x][0] != TextureConnection[x][1] else None , TextureConnection.keys() )
			map(lambda x: cmds.setAttr( x , TextureConnection[x][1] , type = "string" ) , TextureConnection.keys() )

			cmds.file( rename = NewScencePath.rsplit("/",1)[0] + "/" + NewMayaFielName  )
			cmds.file( save = True, type = 'mayaAscii' )
			
			cmds.file( ScencePath.rsplit("/",1)[0] + "/" + NewMayaFielName , o = True ) ## ---- open back the localfile
			
			cmds.warning( "File is saved to Server Successfully !!" )

			## ------------------------------------ ##

		else:

			cmds.warning( "Maya file's version is too low !!! Please check maya file's folder might be damaged...." )

	else:

		cmds.warning( "Please check current maya file location...//: Should be in L: drive and correct folder //" )

else:

	cmds.warning( "Please make sure I drive has being connected..." )