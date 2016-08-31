import numpy as np
import matplotlib.pyplot as plt
import time
start = time.clock()
print('The program is running...\n...\n...')

#函数定义
def OCV(x):
	global y
	y=pl[1]*x**8+pl[2]*x**7+pl[3]*x**6+pl[4]*x**5+pl[5]*x**4+pl[6]*x**3+pl[7]*x**2+pl[8]*x**1+pl[9]
	return y

def DCR(x):
	global y2
	y2 = gl[1]*x**8+gl[2]*x**7+gl[3]*x**6+gl[4]*x**5+gl[5]*x**4+gl[6]*x**3+gl[7]*x**2+gl[8]*x**1+gl[9]
	return y2	
	
#函数参数定义——需要用户自己提供	
pl=(0,-73.6,243.8,-281.9,104.2,38.25,-39.12,8.9,0.3688,3.294)
gl=(0,0,0,14.81,-49.17,65.64,-45.05,16.79,-3.236,0.3011)



fig, ax = plt.subplots()
#初始值-需要用户自己提供
variation=0.5 #电池内阻一致性
CAP=2.8#标称容量

#可修改的参数
dt=1 #计算间隔时间（单位：s）
pno=2 #并数
sno=4 #串数
I=3

#开始计算
n=0
SOC=np.ones((sno,pno))
V=np.zeros((sno,pno))
C=np.zeros((sno,pno))
IS=np.zeros((sno,pno))

#DCR正态分布随机系数
coff=np.random.normal(1,variation**2,(sno,pno))

#生成多维数组-方程参数
xs=np.zeros((pno,pno))
cs=np.zeros(pno)

j=0
while j<sno:
	i=0
	while i<pno-1:
		xs[i][i]=DCR(SOC[j][i])*coff[j][i]
		xs[i][i+1]=-DCR(SOC[j][i+1])*coff[j][i+1]
		xs[pno-1][i]=1
		xs[pno-1][-1]=1
		cs[i]=OCV(SOC[j][i])-OCV(SOC[j][i+1])
		cs[-1]=I
		i=i+1
	IS[j]=np.linalg.solve(xs,cs)
	j=j+1

V=OCV(SOC)-IS*DCR(SOC)*coff
C=C+IS*dt/3600
SOC=SOC-IS*dt/(3600*CAP)
MSOC=SOC.min()
MV=V.min()

while MV>=2.5 and MV<=4.2 and MSOC>=0 and MSOC<=1:
	j=0
	while j<sno:
		i=0
		while i<pno-1:
			xs[i][i]=DCR(SOC[j][i])*coff[j][i]
			xs[i][i+1]=-DCR(SOC[j][i+1])*coff[j][i+1]
			xs[pno-1][i]=1
			xs[pno-1][-1]=1
			cs[i]=OCV(SOC[j][i])-OCV(SOC[j][i+1])
			cs[-1]=I
			i=i+1
		IS[j]=np.linalg.solve(xs,cs)
		j=j+1

	V=OCV(SOC)-IS*DCR(SOC)*coff
	C=C+IS*dt/3600
	SOC=SOC-IS*dt/(3600*CAP)
	for i in range(sno):
		for j in range(pno):
			ax.plot(n,IS[i][j],'k.-',markersize=1)
	MSOC=SOC.min()
	MV=V.min()
	n=n+dt
ax.set_xlabel('Time/s', fontsize=15)
ax.set_ylabel('Current/A', fontsize=15)
ax.set_title('%d' %pno+'P'+'%d' %sno+'S',fontsize=18)
#title='%d' %pno+'P'+'%d' %sno+'S'
	
print('Thanks for your patience.\nThe result is as below...\n')	
print('IS=',IS,'\nOCV=',OCV(SOC),'\nV=',V,'\nC=',C,'\n')
print('variation of Capacity=',np.var(C)**0.5,'\n')
print('The plot is the final...')
ax.grid(True)
fig.tight_layout()
plt.show()
end = time.clock()
print('total time=',end-start,'\n')
