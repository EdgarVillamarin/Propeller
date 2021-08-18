import pandas as pd
import numpy as np
import math

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

def curve_kt_kq(PD,AEAO,z):
  """
  Determine the KT: Thrust coefficient, KQ: Torque coefficient, no= open water efficiency for a 
  different values of advance coefficient J.
  Author: Nav. Eng. Edgar Villamarin
  mail: e_villamarin@grupo-villamarin.com
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
