#nouveau programme pour l'acceleration materielle
#gaetan 8/09/13

import Image
import numpy
import pyopencl as cl


class Climage:

	def __init__(self,image):

		self.context = cl.Context()
		self.queue = cl.CommandQueue(self.context)
		self.nom = image
		self.image = Image.open(image)
		self.pix = self.image.load()
		self.x,self.y = self.image.size

		f = open('haar.cl', 'r')
		fstr = "".join(f.readlines())
		self.program = cl.Program(self.context, fstr).build()
		f.close()

	def execute(self,epsilon):

		tabstl = self.gettl()
		tlr = numpy.array(tabstl[0] , dtype = numpy.uint8)
		tlg = numpy.array(tabstl[1] , dtype = numpy.uint8)
		tlb = numpy.array(tabstl[2] , dtype = numpy.uint8)

		tabstr = self.gettr()
		trr = numpy.array(tabstr[0] , dtype = numpy.uint8)
		trg = numpy.array(tabstr[1] , dtype = numpy.uint8)
		trb = numpy.array(tabstr[2] , dtype = numpy.uint8)

		tabsll = self.getll()
		llr = numpy.array(tabsll[0] , dtype = numpy.uint8)
		llg = numpy.array(tabsll[1] , dtype = numpy.uint8)
		llb = numpy.array(tabsll[2] , dtype = numpy.uint8)

		tabslr = self.getlr()
		lrr = numpy.array(tabslr[0] , dtype = numpy.uint8)
		lrg = numpy.array(tabslr[1] , dtype = numpy.uint8)
		lrb = numpy.array(tabslr[2] , dtype = numpy.uint8)


		for i in [[tlr,trr,llr,lrr],[tlg,trg,llg,lrg],[tlb,trb,llb,lrb]]:
			mf = cl.mem_flags
			tl_buf = cl.Buffer(self.context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=i[0])
			tr_buf = cl.Buffer(self.context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=i[1])
			ll_buf = cl.Buffer(self.context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=i[2])
			lr_buf = cl.Buffer(self.context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=i[3])
			epsilon = numpy.int32(epsilon)
			self.program.haar(self.queue, i[0].shape, None, tl_buf, tr_buf, ll_buf, lr_buf, epsilon)
			cl.enqueue_copy(self.queue, i[0], tl_buf)
			cl.enqueue_copy(self.queue, i[1], tr_buf)
			cl.enqueue_copy(self.queue, i[2], ll_buf)
			cl.enqueue_copy(self.queue, i[3], lr_buf)
			
		for i in self.x/2:
			for j in self.y/2:
				self.pix[2*x,2*y] = (tlr[i+j],tlg[i+j],tlb[i+j])
				self.pix[2*x+1,2*y] = (trr[i+j],trg[i+j],trb[i+j])
				self.pix[2*x,2*y+1] = (llr[i+j],llg[i+j],llb[i+j])
				self.pix[2*x+1,2*y+1] = (lrr[i+j],lrg[i+j],lrb[i+j])

	def save(self):
		
		self.image.save('output.jpg', 'JPEG', quality = 100)

	
	def gettl(self):

		tabr,tabg,tabb = [],[],[]
		for i in range(self.x/2):
			for j in range(self.y/2):
				tabr.append(self.pix[2*i,2*j][0])
				tabg.append(self.pix[2*i,2*j][1])
				tabb.append(self.pix[2*i,2*j][2])
		return tabr,tabg,tabb

	def gettr(self):

		tabr,tabg,tabb = [],[],[]
		for i in range(self.x/2):
			for j in range(self.y/2):
				tabr.append(self.pix[2*i +1,2*j][0])
				tabg.append(self.pix[2*i+1,2*j][1])
				tabb.append(self.pix[2*i+1,2*j][2])
		return tabr,tabg,tabb

	def getll(self):

		tabr,tabg,tabb = [],[],[]
		for i in range(self.x/2):
			for j in range(self.y/2):
				tabr.append(self.pix[2*i,2*j+1][0])
				tabg.append(self.pix[2*i,2*j+1][1])
				tabb.append(self.pix[2*i,2*j+1][2])
		return tabr,tabg,tabb


	def getlr(self):

		tabr,tabg,tabb = [],[],[]
		for i in range(self.x/2):
			for j in range(self.y/2):
				tabr.append(self.pix[2*i+1,2*j+1][0])
				tabg.append(self.pix[2*i+1,2*j+1][1])
				tabb.append(self.pix[2*i+1,2*j+1][2])
		return tabr,tabg,tabb


def main():
	img = Climage('images/piano_bleu.jpg')
	img.execute(15)
	img.save()


if __name__ == "__main__":
	main()
