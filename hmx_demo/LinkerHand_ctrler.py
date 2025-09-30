import sys,os,time
current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(target_dir)
# import argparse
from LinkerHand.linker_hand_api import LinkerHandApi
from LinkerHand.utils.color_msg import ColorMsg


class hand_ctrler():
    
    def __init__(self):
        pass

    def get_sync_speed(self, current_pose, target_pose, reference_dt):
        '''
        * description: 计算五根手指同步到达目标点所需的速度
        * params:
            current_pose: 当前位置
            target_pose: 目标位置
            reference_de: 参考时间
        * return:
            speeds: 各关节所需速度
        '''
        speeds = []
        for i in range(len(current_pose)):
            dist_ = target_pose[i] - current_pose[i]
            # print(dist_)
            if abs(dist_) >= 5:
                speed_ = abs(dist_ / reference_dt)
                if speed_ > 255:
                    speed_ = 255
            else:
                speed_ = 50
            speeds.append(speed_)
        return speeds
    
    def hand_exec(self, hand:LinkerHandApi, target_pose, speeds, err_thr=10, delay=5, target_torque=None, is_block=True):
        '''
        * description: 控制灵巧手执行
        * params:
            hand: 实例化的灵巧手api
            target_pose: 目标位置
            speeds: 执行速度
            err_thr: 到位误差阈值，默认为10
            delay: 延时，默认为5s
            target_torque: 目标力矩，默认为空
            is_block: 是否阻塞，默认为True
        * returns
            err_code: 
                -2: 发生异常
                -1: 控制超时
                0: 不阻塞的情况下指令发送完成
                1: 运动到位
                2: 已经抓紧
        '''
        try:
            hand.set_torque(torque=[255,255,255,255,255,255,255,255,255,255])

            hand.set_speed(speed=speeds)
            hand.finger_move(pose=target_pose)

            t_start = time.time()

            while is_block:
                current_pose = hand.get_state()
                err = []
                for i in range(len(current_pose)):
                    err_ = target_pose[i] - current_pose[i]
                    err.append(abs(err_))

                t_current = time.time()
                dt = t_current - t_start
                if max(err) <= err_thr:
                    # print(f'灵巧手到达目标位置，耗时: {dt} s')
                    ColorMsg(msg=f'灵巧手到达目标位置，耗时: {dt} s',color='green')
                    return 1
                else:       
                    if dt < delay:
                        if target_torque is not None:
                            current_torque = hand.get_torque()
                            
                            target_torques_ = [
                                target_torque[0],
                                target_torque[2],
                                target_torque[3],
                                target_torque[4],
                                target_torque[5],
                            ]
                            current_torques_ = [
                                current_torque[0],
                                current_torque[2],
                                current_torque[3],
                                current_torque[4],
                                current_torque[5]
                            ]

                            err_torque = abs(min(target_torques_)-min(current_torques_))
                            if err_torque <= 10:
                                ColorMsg(msg=f'灵巧手已抓紧，耗时：{dt} s  各轴力矩：{current_torque}',color='green')
                                # print(f'灵巧手已抓紧，耗时：{dt} s  各轴力矩：{current_torque}')
                                return 2
                    else:
                        ColorMsg(msg='灵巧手运动超时 ! ! !',color='red')
                        # print('灵巧手运动超时')
                        return -1
            return 0
        except Exception as e:
            ColorMsg(msg=f'灵巧手发生错误：{e}',color='red')
            # print('灵巧手发生错误: ',e)
            return -2
        
class teach_data():
    def __init__(self):
        
        self.poses_get_cylinder = [
            [255,   0, 255, 255, 255, 255, 255, 255, 255, 121],
            [200,   0, 167, 157, 169, 175, 255, 255, 255, 121],
            [140,   0, 107, 97, 109, 115, 255, 255, 255, 121]
        ]
        self.torque_get_cylinder = [115, 15, 116, 112, 118, 115, 13, 8, 6, 62]



        self.poses_get_box = [
            [255,  55, 255, 255, 255, 255, 255, 255, 255,  57],
            [206,  55, 206, 197, 206, 210, 255, 255, 255,  57],
            # [156,  55, 156, 147, 156, 160, 255, 255, 255,  57]
            # [156,  55, 206, 197, 206, 210, 255, 255, 255,  57],
            [156,  55, 186, 177, 186, 190, 255, 255, 255,  57]
        ]
        self.torque_get_box = [117, 5, 111, 110, 110, 117, 10, 7, 5, 6]


        self.poses_get_bag = [
            [255,  76, 255, 255, 255, 255, 255, 255, 255,  62],
            # [190,  50, 220, 220, 220, 220, 255, 255, 255,  50],
            [190,  76, 200, 190, 200, 200, 255, 255, 255,  62],
            [  0,  76,   0,   0,   0,   0, 255, 255, 255,  62]
        ]
        self.torque_get_bag = [113, 16, 115, 114, 111, 111, 6, 6, 9, 34]
        
        pass

class hand_program():
    def __init__(self):
        
        self.hand = hand_ctrler()
        self.pose_ready_to_grip = [255, 70, 255, 255, 255, 255, 255, 255, 255, 121]
        self.speed_defaut = [50,50,50,50,50,50,50,50,50,50]
        
        self.poses_get_cylinder = [
            [255,   0, 255, 255, 255, 255, 255, 255, 255, 121],
            [200,   0, 167, 157, 169, 175, 255, 255, 255, 121],
            [180,   0, 147, 137, 149, 155, 255, 255, 255, 121]
        ]
        self.torque_get_cylinder = [115, 15, 116, 112, 118, 115, 13, 8, 6, 62]
        pass

    def sync_exec(self,hand:LinkerHandApi,target_pose,dt,Torque=None):
        current_pose = hand.get_state()
        speeds = self.hand.get_sync_speed(
            current_pose=current_pose,
            target_pose=target_pose,
            reference_dt=dt
        )
        
        ret = self.hand.hand_exec(
            hand=hand,
            target_pose=target_pose,
            speeds=speeds,
            target_torque=Torque
        )
        return ret

    def crawl(self,hand:LinkerHandApi, target_pose_list, target_torque):
        '''
        * description: 抓取直径约为64mm的圆柱体
        '''
        try:
            # 张开至抓取预备姿态
            self.hand.hand_exec(hand,self.pose_ready_to_grip,self.speed_defaut)

            # 运动至抓取圆柱起始姿态
            # self.hand.hand_exec(hand,target_pose_list[0],self.speed_defaut)
            self.sync_exec(hand,target_pose_list[0],dt=2)

            time.sleep(2)

            # 同步运动至贴合状态
            self.sync_exec(hand,target_pose_list[1],dt=3)

            time.sleep(0.5)
            # 同步发力至抓紧状态
            self.sync_exec(hand,target_pose_list[2],dt=3,Torque=target_torque)

            return 1
        except Exception as e:
            print('执行发生错误: ',e)
            return 0


    def drop(self,hand:LinkerHandApi,target_pose_list):
        '''
        * description: 放开直径约为64mm的圆柱体
        '''
        try:
            # 同步放松至贴合状态
            self.sync_exec(hand,target_pose_list[1],dt=3)

            time.sleep(1)
            
            # 同步张开至抓取圆柱起始状态
            self.sync_exec(hand,target_pose_list[0],dt=2)

            time.sleep(1)

            # 张开至抓取预备姿态
            self.hand.hand_exec(hand,self.pose_ready_to_grip,self.speed_defaut)  

            return 1
        except Exception as e:
            print('执行发生错误: ',e)
            return 0



def get_teach_pose_torque():
    hand = LinkerHandApi(hand_type="right", hand_joint="L10")
    data = teach_data()
    program = hand_program()
    target_pose = data.poses_get_cylinder
    torque = data.torque_get_cylinder
    # program.sync_exec(hand,target_pose,dt=3)
    program.crawl(hand,target_pose,torque)
    
    time.sleep(2)
    program.drop(hand,target_pose)
    print(hand.get_torque())
    

# if __name__ == '__main__':

    
#     get_teach_pose_torque()
    
