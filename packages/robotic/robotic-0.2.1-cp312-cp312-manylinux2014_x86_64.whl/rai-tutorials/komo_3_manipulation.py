
import robotic as ry
import numpy as np
import random
import time

# this import the local manipulation.py .. to be integrated in robotic..
import manipulation as manip


# A basic configuration with a box and cylinder:

# In[ ]:


C = ry.Config()
C.addFile(ry.raiPath('scenarios/pandaSingle.g'))

C.addFrame('box') \
    .setPosition([-.25,.1,1.]) \
    .setShape(ry.ST.ssBox, size=[.06,.06,.06,.005]) \
    .setColor([1,.5,0]) \
    .setContact(1)

C.addFrame('capsule') \
    .setShape(ry.ST.capsule, [.2,.02]) \
    .setPosition([.25,.1,1.]) \
    .setColor([1,.5,0]) \
    .setContact(1)

# for convenience, a few definitions:
qHome = C.getJointState()
gripper = 'l_gripper'
palm = 'l_palm'
box = 'box'
table = 'table'
boxSize = C.getFrame(box).getSize()

C.view()




C.setJointState(qHome)

for i in range(10):
    grasp_ori = random.choice(['x', 'y', 'z'])
    place_ori = 'z' #random.choice(['x', 'y', 'z'])
    info = f'pnp {i}, grasp orientation {grasp_ori}, place orientation {place_ori}'
    print('===', info)
    
    # setup manipulation problem
    man = manip.ManipulationModelling()
    man.setup_pick_and_place_waypoints(C, gripper, box)
    man.grasp_box(1., gripper, box, palm, grasp_ori)
    man.place_box(2., box, table, palm, place_ori)
    man.target_relative_xy_position(2., box, table, [(i%5)*.1-.2, .2])
    
    # solve
    q = man.solve()

    # if feasible, display (including 'fake' simulation with kinematic attach)
    if man.ret.feasible:
        C.setJointState(q[0])
        C.view(True, f'{info}\nwaypoint 0\nret: {man.ret}')
        C.attach(gripper, box)
        C.setJointState(q[1])
        C.view(True, f'{info}\nwaypoint 1\nret: {man.ret}')
        C.attach(table, box)
        C.setJointState(qHome)
        C.view(True, 'back home')
    else:
        print(' -- infeasible')

del man
C.getFrame('box').setPosition([-.25,.1,1.])
C.view()


# ## Path generation
# 
# Once solutions to the manipulation keyframes/waypoints are available, the next step is to generate motion between them. We can use sample-based path finding (bi-directional RRT) and/or smooth motion optimization for this.

# ### Smooth point-to-point motion
# The following demonstrates smooth point-to-point motion between box grasps, there the motion is additionally constrains the endeffector to retract and approach:

# In[ ]:


C.setJointState(qHome)
limits = C.getJointLimits()
verbose = 0

for i in range(20):
    qStart = C.getJointState()
    
    # choose a random grasp orientation
    orientation = random.choice(['x', 'y', 'z'])
    print('===', i, 'orientation', orientation)
    
    # setup the grasp problem
    man = manip.ManipulationModelling()
    man.setup_inverse_kinematics(C, accumulated_collisions=True)
    man.grasp_box(1., gripper, box, palm, orientation)
    
    # solve
    pose = man.solve()
    print('    IK:', man.ret)
    
    # if feasible, display; otherwise try another grasp
    if man.ret.feasible:
        if verbose>0:
            C.setJointState(pose[0])
            C.view(True, f'grasp {i} with orientation {orientation}\nret: {man.ret}')
    else:
        print('  -- infeasible')
        C.setJointState(qStart)
        continue

    # setup the motion problem
    man = manip.ManipulationModelling()
    man.setup_point_to_point_motion(C, pose[0])
    man.retract([.0, .2], gripper)
    # man.approach([.8, 1.], gripper)
    
    # solve
    path = man.solve()
    print('  path:', man.ret)

    # if feasible, display trivially (no real execution in BotOp here)
    if man.ret.feasible:
        for t in range(path.shape[0]):
            C.setJointState(path[t])
            C.view(False, f'grasp {i} with orientation {orientation}, path step {t}\n{man.ret}')
            time.sleep(.05)
        C.view(verbose>0, f'path done')
    else:
        print('  -- infeasible')
        
del man


# ## Integrated Example
# 
# Let's start with an integrated example, where the robot endlessly loops through picking and placing a box on a table.

# In[ ]:


import robotic as ry
import manipulation as manip
import numpy as np
#from importlib import reload
import time
import random


# We define a basic configuration with box on the table:

# In[ ]:


C = ry.Config()
C.addFile(ry.raiPath('../rai-robotModels/scenarios/pandaSingle.g'))

C.addFrame('box', 'table') \
    .setJoint(ry.JT.rigid) \
    .setShape(ry.ST.ssBox, [.15,.06,.06,.005]) \
    .setRelativePosition([-.0,.3-.055,.095]) \
    .setContact(1) \
    .setMass(.1)

C.addFrame('obstacle', 'table') \
    .setShape(ry.ST.ssBox, [.06,.15,.06,.005]) \
    .setColor([.1]) \
    .setRelativePosition([-.15,.3-.055,.095]) \
    .setContact(1)

C.delFrame('panda_collCameraWrist')

# for convenience, a few definitions:
qHome = C.getJointState()
gripper = 'l_gripper'
palm = 'l_palm'
box = 'box'
table = 'table'
boxSize = C.getFrame(box).getSize()

C.view()


# ### tob grasps and pick-and-place over an object

# In[ ]:


#reload(manip)

C.setJointState(qHome)
C.view_raise()

C.getFrame(box).setRelativePosition([-.0,.3-.055,.095])
C.getFrame(box).setRelativeQuaternion([1.,0,0,0])

for i in range(7):
        qStart = C.getJointState()

        graspDirection = 'yz' #random.choice(['xz', 'yz'])
        placeDirection = 'z'
        place_position = [(i%3)*.3-.3, .2]
        place_orientation = [-(i%2),((i+1)%2),0.]
        info = f'placement {i}: grasp {graspDirection} place {placeDirection} place_pos {place_position} place_ori {place_orientation}'
        print('===', info)

        M = manip.ManipulationModelling()
        M.setup_pick_and_place_waypoints(C, gripper, box, homing_scale=1e-1, joint_limits=False)
        M.grasp_top_box(1., gripper, box, graspDirection)
        M.place_box(2., box, table, palm, placeDirection)
        M.target_relative_xy_position(2., box, table, place_position)
        M.target_x_orientation(2., box, place_orientation)
        M.solve()
        if not M.feasible:
                continue

        M2 = M.sub_motion(0)
        M2.retract([.0, .2], gripper)
        M2.approach([.8, 1.], gripper)
        M2.solve()
        if not M2.ret.feasible:
            continue

        M3 = M.sub_motion(1)
#         M3.retract([.0, .2], box, distance=.05)
#         M3.approach([.8, 1.], box, distance=.05)
        M3.no_collisions([], [table, box])
        M3.no_collisions([], [box, 'obstacle'])
        M3.bias(.5, qHome, 1e0)
        M3.solve()
        if not M3.ret.feasible:
            continue
            
        M2.play(C)
        C.attach(gripper, box)
        M3.play(C)
        C.attach(table, box)

del M


# ### endless box pick and place with random pick and place orientations

# In[ ]:


#reload(manip)

C.delFrame('obstacle')

C.setJointState(qHome)
C.view_raise()

for l in range(20):
        qStart = C.getJointState()

        graspDirection = random.choice(['y', 'z']) #'x' not possible: box too large
        placeDirection = random.choice(['x', 'y', 'z', 'xNeg', 'yNeg', 'zNeg'])
        info = f'placement {l}: grasp {graspDirection} place {placeDirection}'
        print('===', info)

        M = manip.ManipulationModelling(info)
        M.setup_pick_and_place_waypoints(C, gripper, box, homing_scale=1e-1)
        M.grasp_box(1., gripper, box, palm, graspDirection)
        M.place_box(2., box, table, palm, placeDirection)
        M.no_collisions([], [palm, table])
        M.target_relative_xy_position(2., box, table, [.2, .3])
        ways = M.solve()

        if not M.feasible:
            continue

        M2 = M.sub_motion(0)
        # M = manip.ManipulationModelling(C, info, helpers=[gripper])
        # M.setup_point_to_point_motion(qStart, ways[0])
        M2.no_collisions([.3,.7], [palm, box], margin=.05)
        M2.retract([.0, .2], gripper)
        M2.approach([.8, 1.], gripper)
        M2.solve()
        if not M2.feasible:
            continue

        M3 = M.sub_motion(1)
        #manip.ManipulationModelling(C, info)
        # M.setup_point_to_point_motion(ways[0], ways[1])
        M3.no_collisions([], [table, box])
        M3.solve()
        if not M3.ret.feasible:
            continue

        M2.play(C)
        C.attach(gripper, box)
        M3.play(C)
        C.attach(table, box)

del M


# ### random pushes

# In[ ]:


#from importlib import reload 
#reload(manip)

C.getFrame('l_panda_finger_joint1').setJointState(np.array([.0]))

obj = box
C.getFrame(obj).setRelativePosition([-.0,.3-.055,.095])
C.getFrame(obj).setRelativeQuaternion([1.,0,0,0])

for i in range(30):
     qStart = C.getJointState()

     info = f'push {i}'
     print('===', info)

     M = manip.ManipulationModelling(info)
     M.setup_pick_and_place_waypoints(C, gripper, obj, 1e-1, accumulated_collisions=False)
     pushStart = M.straight_push([1.,2.], obj, gripper, table)
     #random target position
     M.komo.addObjective([2.], ry.FS.position, [obj], ry.OT.eq, 1e1*np.array([[1,0,0],[0,1,0]]), .4*np.random.rand(3) - .2+np.array([.0,.3,.0]))
     M.solve()
     if not M.ret.feasible:
          continue

     M1 = M.sub_motion(0, accumulated_collisions=False)
     M1.retractPush([.0, .15], gripper, .03)
     M1.approachPush([.85, 1.], gripper, .03)
     M1.no_collisions([.15,.85], [obj, 'l_finger1'], .02)
     M1.no_collisions([.15,.85], [obj, 'l_finger2'], .02)
     M1.no_collisions([.15,.85], [obj, 'l_palm'], .02)
     M1.no_collisions([], [table, 'l_finger1'], .0)
     M1.no_collisions([], [table, 'l_finger2'], .0)
     M1.solve()
     if not M1.ret.feasible:
          continue

     M2 = M.sub_motion(1, accumulated_collisions=False)
     M2.komo.addObjective([], ry.FS.positionRel, [gripper, pushStart], ry.OT.eq, 1e1*np.array([[1,0,0],[0,0,1]]))
     M2.solve()
     if not M2.ret.feasible:
          continue

     M1.play(C, 1.)
     C.attach(gripper, obj)
     M2.play(C, 1.)
     C.attach(table, obj)

del M


# ## TODOS:
# * Proper execution: BotOp instead of display with C
# * RRTs
# * additional planar motion constraint for in-plane manipulation
# * more typical manipulation constraints: camera_look_at, push_straight, 

# In[ ]:


del C


# In[ ]:




