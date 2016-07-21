import base64
from io import BytesIO
import os
from PIL import Image



class ImageProcessor:
	def __init__(self,request):
		img64 = request.POST.get('imgUrl')
		img64 = img64[img64.find(',')+1:]
		self.img = Image.open(BytesIO(base64.b64decode(img64)))
		self.initDim = (int(request.POST.get('imgInitW')), int(request.POST.get('imgInitH')))
		self.scaleDim = (int(float(request.POST.get('imgW'))), int(float(request.POST.get('imgH'))))
		self.cropDim = (int(float(request.POST.get('cropW'))), int(float(request.POST.get('cropH'))))
		self.corner = (int(float(request.POST.get('imgX1'))), int(float(request.POST.get('imgY1'))))
		self.rotation = request.POST.get("rotation")
		if '-' in request.POST.get("rotation"):
			self.angle = int(request.POST.get("rotation")[1:])
		else:
			self.angle = 360 - int(request.POST.get("rotation"))#rotation in pil is counterclockwise
		

	def CropImage(self):
		self.img = self.img.resize(self.scaleDim, Image.LANCZOS)
		self.img = self.img.rotate(self.angle)
		self.img = self.img.crop((self.corner[0], self.corner[1] , self.cropDim[0] + self.corner[0], self.cropDim[1] + self.corner[1]))
		
		
	def SaveImage(self, filename):
		full_path = os.path.join("/var/www/html/ShotForTheHeart/media/", filename)
		try:
			self.img.save(full_path)
			return True
		except:
			return False
		
	def LoadImage(self, path):
		filename = "/var/www/html/ShotForTheHeart/" + path
		return base64.b64encode(open(filename,"rb").read())
		