import pandas as pd
import numpy as np
import math
import glob
import numpy.matlib
""""
Author: Nav. Eng. Edgar Villamarin Garcia
Mail: e_villamarin@grupo-villamarin.com
Web: www.grupo-villamarin.com

""""
def wage(ja,PD,AEAO,z):
  """
  Reference: Barnitsas, M.M., Ray, D. and Kinley, P. (1981).
  KT, KQ and Efficiency Curves for the Wageningen B-Series Propellers
  http://deepblue.lib.umich.edu/handle/2027.42/3557
  
  Ja: Advance Coefficient
  PD: Pitch/Diameter coefficient
  AEAO: Expand Propeller Area Coefficient
  z: Numbers of Blade propellers
  """
  import scipy.io
  import math
  mat = scipy.io.loadmat('/content/Propeller/WageningData.mat')
  KT = sum(mat['WagCThrust_stuv']*((ja)**mat['WagThrust_s'])*PD**mat['WagThrust_t']*AEAO**mat['WagThrust_u']*z**mat['WagThrust_v'])
  KQ= sum(mat['WagCTorque_stuv']*((ja)**mat['WagTorque_s'])*PD**mat['WagTorque_t']*AEAO**mat['WagTorque_u']*z**mat['WagTorque_v'])
  KT=float(KT)
  KQ=float(KQ)
  return KT,KQ

def curve_kt_kq_wage(PD,AEAO,z):
  """
  Determine the KT: Thrust coefficient, KQ: Torque coefficient, no= open water efficiency for a 
  different values of advance coefficient J, for wagennigen propellers.
  """
  if z>2 and z<7 and PD> 0.5 and PD<1.4 and AEAO>0.35 and AEAO<1.40:
    j=np.arange(0,2,0.001)
    kt=[]
    kq=[]
    ne=[]
    jn=0
    for x in range(0,len(j),1):
      kt1,kq1=wage(j[x],PD,AEAO,z)
      if kt1>0 and kq1>0:
        kt.append(kt1)
        kq.append(kq1)
        ne.append((j[x]/(2*3.1416))*(kt1/kq1))
        jn=jn+1
    j=j[0:jn]
    villamarin=pd.DataFrame()
    villamarin['J']=j
    villamarin['KT']=kt
    villamarin['KQ']=kq
    villamarin['no']=ne
  else:
    return print('Check aplication limits')
  return villamarin

def kaplan(FileID,PD,J):
  """
  Determine the KT: Thrust coefficient, KQ: Torque coefficient, no= open water efficiency for a 
  different values of advance coefficient J, for wagennigen propellers.
  Reference Coefficient:
  https://repository.tudelft.nl/islandora/object/uuid:b8cd2238-1cd7-4a64-a74e-73f4dcdf35d4/datastream/OBJ/download
  FileID: Name of the data file coefficient, Ka375,Ka455,Ka470,Ka575
  """
  File='/content/propeller'+str(FileID)
  ka=pd.read_csv(File)
  heads=list(ka.columns)
  #factor=np.ones((7,7))
  R=np.ones((7,1))
  Ja=np.ones((7,1))
  for x in range(0,7,1):
    R[x,0]=PD**x
    Ja[x,0]=J**x
  for x in range(0,len(heads),1):
    globals()[f'A{x}']=np.array(ka[heads[x]])
    globals()[f'A{x}']=np.matlib.reshape(globals()[f'A{x}'],(7,7))
  KT=float(np.matmul(np.transpose(np.matmul(A0,Ja)),R))
  KQ=float(np.matmul(np.transpose(np.matmul(A1,Ja)),R))
  KTN=float(np.matmul(np.transpose(np.matmul(A2,Ja)),R))
  return KT,KTN,KQ

def curve_kt_kq_kaplan(FileID,PD):
  """
  Determine the KT: Thrust coefficient, KQ: Torque coefficient, no= open water efficiency for a 
  different values of advance coefficient J, for kapla in a duct 19A propellers.
  """
  if  PD> 0.5 and PD<1.4:
    j=np.arange(0,2,0.001)
    kt=[]
    kq=[]
    ne=[]
    jn=0
    for x in range(0,len(j),1):
      kt1,kq1=kaplan(FileID,PD,j[x])
      if kt1>0 and kq1>0:
        kt.append(kt1)
        kq.append(kq1)
        ne.append((j[x]/(2*3.1416))*(kt1/kq1))
        jn=jn+1
    j=j[0:jn]
    villamarin=pd.DataFrame()
    villamarin['J']=j
    villamarin['KT']=kt
    villamarin['KQ']=kq
    villamarin['no']=ne
  else:
    return print('Check aplication limits')
  return villamarin

