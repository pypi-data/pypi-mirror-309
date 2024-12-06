import numpy as np
import robotic as ry

print(ry.compiled())

SG = ry.DataGen.ShapenetGrasps()

opt = ry.DataGen.ShapenetGrasps_Options()
opt.startShape=3
opt.numShapes=1
opt.verbose=0
SG.setOptions(opt)

opt = ry.DataGen.PhysX_Options()
opt.motorKp=20000.
opt.motorKd=500.
opt.angularDamping=.1
opt.defaultFriction=3.
SG.setPhysxOptions(opt)

X, Z, S = SG.getSamples(20)
SG.displaySamples(X, Z, S)
#   for(uint i=0;i<X.d0;i++){
#     arr scores = RG.evaluateSample(X[i], Z[i]);
#     cout <<"scores " <<i <<"\n  data: " <<S[i] <<"\n  eval: " <<scores.reshape(-1) <<' ' <<(min(scores)>0.) <<endl;
#   }
