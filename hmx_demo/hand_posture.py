import sys,os,time
current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(target_dir)
# import argparse
from LinkerHand.linker_hand_api import LinkerHandApi


def hand_exec(hand:LinkerHandApi, pose, speed, delay=5, err_thr=10):
    hand.set_speed(speed=speed)
    hand.finger_move(pose=pose)
    
    # current_pose = []
    t_start = time.time()
    while True:
        current_pose = hand.get_state()
        
        err = []
        for i in range(len(current_pose)):
            err_ = current_pose[i] - pose[i]
            err.append(abs(err_))

        # print(err)

        t_current = time.time()
        dt = t_current - t_start
        if max(err) <= err_thr:
            print('机械手到达目标位置：', pose)
            print('耗时：', dt)
            return 1
        
        
        if dt >= delay:
            print('超时!!!')
            return 0
        
        time.sleep(0.2)

def grip_cylinder_pose(diameter):
    pose = [60,60,25,25,25,25,255,255,255,58]
    i = diameter*2
    pose[0] = 60 + i
    pose[2] = 25 + i
    pose[3] = 25 + i
    pose[4] = 25 + i
    pose[5] = 25 + i
    return pose

pose_ready = [255, 70, 255, 255, 255, 255, 255, 255, 255, 121]
speed_ready = [50,50,50,50,50,50,50,50,50,50]

poses_get_bottle = [
    # [220,0,155,146,155,160,255,255,255,121],
    [255, 0, 255, 255, 255, 255, 255, 255, 255, 121],

    [200,0,167,157,169,175,255,255,255,121],
    # [255,0,105,96,105,110,255,255,255,121]
    [180,0,147,137,149,155,255,255,255,121]
]

def get_sync_speed(current_pose:list, target_pose:list, reference_speed:int):
    reference_dist = target_pose[2]-current_pose[2]
    reference_dt = reference_dist / reference_speed

    speeds = []
    for i in range(10):
        if i == 0 or i == 3 or i == 4 or i == 5:
            dist_ = target_pose[i]-current_pose[i]
            speed_ = round(dist_ / reference_dt)
        else:
            speed_ = reference_speed
        
        speeds.append(speed_)

    return speeds


def drop_cylinder(hand:LinkerHandApi):

    # hand = LinkerHandApi(hand_type="right", hand_joint="L10")
    
    torque = hand.get_torque()
    print('力矩为：',torque)

    current_pose = hand.get_state()
    target_pose = poses_get_bottle[1]
    speeds = get_sync_speed(current_pose,target_pose,30)
    hand_exec(hand,target_pose,speeds)

    time.sleep(0.5)

    current_pose = hand.get_state()
    target_pose = poses_get_bottle[0]
    speeds = get_sync_speed(current_pose,target_pose,100)
    hand_exec(hand,target_pose,speeds)

    hand_exec(hand,pose_ready,speed_ready)


def get_cylinder(hand:LinkerHandApi):
    '''
    * description: 抓取直径约为64mm的圆柱体
    '''
    # hand = LinkerHandApi(hand_type="right", hand_joint="L10")
    
    hand_exec(hand,pose_ready,speed_ready)

    hand_exec(hand,poses_get_bottle[0],speed_ready)

    torque = hand.get_torque()
    print('力矩为：',torque)

    # 计算同步速度
    current_pose = hand.get_state()
    target_pose = poses_get_bottle[1]
    speeds = get_sync_speed(current_pose=current_pose,target_pose=target_pose,reference_speed=50)
    # print(speeds)

    time.sleep(1)
    hand_exec(hand,target_pose,speeds)

        # 计算同步速度
    current_pose = hand.get_state()
    target_pose = poses_get_bottle[2]
    speeds = get_sync_speed(current_pose=current_pose,target_pose=target_pose,reference_speed=10)

    time.sleep(1)
    hand_exec(hand,target_pose,speeds)

    torque = hand.get_torque()
    print('力矩为：',torque)


def test():

    hand = LinkerHandApi(hand_type="right", hand_joint="L10")


    torque = hand.get_torque()
    print(torque)
    hand_exec(hand,pose_ready,speed_ready)

    time.sleep(1)

    hand_exec(hand,poses_get_bottle[0],speed_ready)
    time.sleep(0.5)
    hand_exec(hand,poses_get_bottle[1],[10,10,10,10,10])
    torque = hand.get_force()
    print(torque)


if __name__ == '__main__':
    # test()
    hand = LinkerHandApi(hand_type="right", hand_joint="L10")

    get_cylinder(hand)
    # time.sleep(2)
    # drop_cylinder(hand)
