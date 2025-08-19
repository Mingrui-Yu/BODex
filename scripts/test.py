import numpy as np

file = "src/curobo/content/assets/output/sim_shadow/tabletop/debug/graspdata/core_bottle_1a7ba1f4c892e2da30711cdbdbc73924/tabletop_ur10e/scale008_pose000_0_grasp.npy"

data = np.load(file, allow_pickle=True).item()

a = 1