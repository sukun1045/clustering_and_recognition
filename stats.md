# temporal_segmentation

## CMU MOCAP DATABASE
### Test Process
1. Three actions
  1. Simple, non-repeated 
     * w1,r1,j1 **checked** 
  2. Simple, repeated
     * w1,r1,j1,w2,r2 **checked** (step=8000,loss=0.0094,test_loss>0.05,error>1.05)
     * w1,r1,j1,w2,w3 **checked** (step=8000,loss=0.0057,test_loss>0.06,error>0.9)
     * w1,r1,j1,w2,r2,j3
     
     
2. Five actions
  
