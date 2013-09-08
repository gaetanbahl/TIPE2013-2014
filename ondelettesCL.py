#nouveau programme pour l'acceleration materielle
#gaetan 8/09/13

import Image
import numpy
import pyopencl as cl
import sys

class Climage:

	def __init__(self,image):

		self.context = cl.create_some_context()
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
		tlr = numpy.array(tabstl[0] , dtype = numpy.int32)
		tlg = numpy.array(tabstl[1] , dtype = numpy.int32)
		tlb = numpy.array(tabstl[2] , dtype = numpy.int32)
		print tlg
		tabstr = self.gettr()
		trr = numpy.array(tabstr[0] , dtype = numpy.int32)
		trg = numpy.array(tabstr[1] , dtype = numpy.int32)
		trb = numpy.array(tabstr[2] , dtype = numpy.int32)

		tabsll = self.getll()
		llr = numpy.array(tabsll[0] , dtype = numpy.int32)
		llg = numpy.array(tabsll[1] , dtype = numpy.int32)
		llb = numpy.array(tabsll[2] , dtype = numpy.int32)

		tabslr = self.getlr()
		lrr = numpy.array(tabslr[0] , dtype = numpy.int32)
		lrg = numpy.array(tabslr[1] , dtype = numpy.int32)
		lrb = numpy.array(tabslr[2] , dtype = numpy.int32)


		for i in [[tlr,trr,llr,lrr],[tlg,trg,llg,lrg],[tlb,trb,llb,lrb]]:
			mf = cl.mem_flags
			tl_buf = cl.Buffer(self.context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=i[0])
			tr_buf = cl.Buffer(self.context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=i[1])
			ll_buf = cl.Buffer(self.context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=i[2])
			lr_buf = cl.Buffer(self.context, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=i[3])
			epsilon = numpy.int32(epsilon)
			print "bite !"
			self.program.haar(self.queue, i[0].shape, None, tl_buf, tr_buf, ll_buf, lr_buf, epsilon)
			print "bite ?"
			
			cl.enqueue_read_buffer(self.queue, tl_buf, i[0]).wait()
			print 'bite'
			cl.enqueue_read_buffer(self.queue, tr_buf, i[1]).wait()
			cl.enqueue_read_buffer(self.queue, ll_buf, i[2]).wait()
			cl.enqueue_read_buffer(self.queue, lr_buf, i[3]).wait()
			print i[1][100:150]
			
			
			
		for i in range(self.x/2):
			for j in range(self.y/2):
				self.pix[2*i,2*j] = (tlr[i+j],tlg[i+j],tlb[i+j])
				self.pix[2*i+1,2*j] = (trr[i+j],trg[i+j],trb[i+j])
				self.pix[2*i,2*j+1] = (llr[i+j],llg[i+j],llb[i+j])
				self.pix[2*i+1,2*j+1] = (lrr[i+j],lrg[i+j],lrb[i+j])

	def save(self,a):
		
		self.image.save(a, 'JPEG', quality = 100)

	
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


def main(args):
	img = Climage(args[1])
	img.execute(15)
	img.save(args[2])


if __name__ == "__main__":
	main(sys.argv)
