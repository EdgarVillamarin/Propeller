def wage(ja,PD,AEAO,z):
  """
  Reference: Barnitsas, M.M., Ray, D. and Kinley, P. (1981).
  KT, KQ and Efficiency Curves for the Wageningen B-Series Propellers
  http://deepblue.lib.umich.edu/handle/2027.42/3557
  """
  import scipy.io
  import math
  mat = scipy.io.loadmat('/content/Propeller/WageningData.mat')
  KT = sum(mat['WagCThrust_stuv']*((ja)**mat['WagThrust_s'])*PD**mat['WagThrust_t']*AEAO**mat['WagThrust_u']*z**mat['WagThrust_v'])
  KQ= sum(mat['WagCTorque_stuv']*((ja)**mat['WagTorque_s'])*PD**mat['WagTorque_t']*AEAO**mat['WagTorque_u']*z**mat['WagTorque_v'])
  KT=float(KT)
  KQ=float(KQ)
  return KT,KQ
