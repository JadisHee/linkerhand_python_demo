import sys,os,time
current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(target_dir)
from JAKA import jkrc
import LinkerHand_ctrler
from LinkerHand.linker_hand_api import LinkerHandApi
import keyboard


hand_ctrl = LinkerHand_ctrler.hand_program()
hand_teach_point = LinkerHand_ctrler.teach_data()

class jaka_teach_point():
    def __init__(self):
        self.get_cylinder = [
            [15.0, -360.0, 50.0, -1.5707963, -0.0, 3.1415926],
            [15.0, -360.0, -125.0, -1.5707963, -0.0, 3.1415926]
        ]

        self.get_box = [
            [50.0, -520.0, 250.0, -3.0766839109453086, -0.7112390938944856, -1.5677769328054325],
            [50.0, -520.0, 18.0, -3.0766839109453086, -0.7112390938944856, -1.5677769328054325]
        ]


        self.get_bag = [
            [50.0, -520.0, 250.0, -3.076460404085111, -0.6523808503880111, -1.5679178506868345],
            [50.0, -520.0,  25.0, -3.076460404085111, -0.6523808503880111, -1.5679178506868345],
            [50.0, -520.0,  -8.5, -3.076460404085111, -0.6523808503880111, -1.5679178506868345]
        ]

        pass

jaka_points = jaka_teach_point()

def bag_demo(jaka, hand:LinkerHandApi, type):
    if type == 0:
        jaka_move_points = jaka_points.get_cylinder
        hand_move_points = hand_teach_point.poses_get_cylinder
        hand_torque = hand_teach_point.torque_get_cylinder
        type_str = '水瓶'
    elif type == 1:
        jaka_move_points = jaka_points.get_box
        hand_move_points = hand_teach_point.poses_get_box
        hand_torque = hand_teach_point.torque_get_box
        type_str = '纸巾'
    elif type == 2:
        jaka_move_points = jaka_points.get_bag
        hand_move_points = hand_teach_point.poses_get_bag
        hand_torque = hand_teach_point.torque_get_bag
        type_str = '装有软物体的塑料袋'
    # elif type == 2:

    # 控制机械臂来到抓取位置上方
    jaka.linear_move(jaka_move_points[0],0,True,300)

    # 张开灵巧手
    # hand_ctrl.drop(hand,hand_move_points)
    hand_ctrl.sync_exec(hand,hand_move_points[0],dt=2)


    print(f"按空格键开始抓取 [{type_str}]")
    keyboard.wait('space')
    
    # time.sleep(1)
    
    # 控制机械臂来到抓取位置
    jaka.linear_move(jaka_move_points[1],0,True,300)
    
    # 控制灵巧手执行抓取动作
    ret = hand_ctrl.sync_exec(hand,hand_move_points[1],dt=2)
    if ret != 1:
        print('手指未到位')
        return 0
    # hand_ctrl.crawl(
    #     hand=hand,
    #     target_pose_list=hand_move_points,
    #     target_torque=hand_torque
    # )

    if type == 2:
        # 下到更下方压紧
        jaka.linear_move(jaka_move_points[2],0,False,10)
        t=40
    else:
        t=2

    # 控制灵巧手握紧动作
    hand_ctrl.sync_exec(hand,hand_move_points[2],dt=t, Torque=hand_torque)
    print('当前力矩为：',hand.get_torque())
    
    time.sleep(1)
    
    # 控制灵巧手回到抓取上方
    jaka.linear_move(jaka_move_points[1],0,True,20)

    jaka.linear_move(jaka_move_points[0],0,True,300)
    
    print(f"按空格键放下 [{type_str}]")
    keyboard.wait('space')
    
    # 控制机械臂来到抓取位置
    jaka.linear_move(jaka_move_points[1],0,True,300)
    
    # 张开灵巧手
    hand_ctrl.sync_exec(hand,hand_move_points[0],dt=2)
    # hand_ctrl.drop(hand,hand_move_points)

    # 控制灵巧手回到抓取上方
    jaka.linear_move(jaka_move_points[0],0,True,300)




def crawl_demo(jaka,hand,type):
    if type == 0:
        jaka_move_points = jaka_points.get_cylinder
        hand_move_points = hand_teach_point.poses_get_cylinder
        hand_torque = hand_teach_point.torque_get_cylinder
        type_str = '水瓶'
    elif type == 1:
        jaka_move_points = jaka_points.get_box
        hand_move_points = hand_teach_point.poses_get_box
        hand_torque = hand_teach_point.torque_get_box
        type_str = '纸巾'
    # elif type == 2:

    # 控制机械臂来到抓取位置上方
    jaka.linear_move(jaka_move_points[0],0,True,300)

    # 张开灵巧手
    hand_ctrl.drop(hand,hand_move_points)

    print(f"按空格键开始抓取 [{type_str}]")
    keyboard.wait('space')
    
    # time.sleep(1)
    
    # 控制机械臂来到抓取位置
    jaka.linear_move(jaka_move_points[1],0,True,300)
    
    # 控制灵巧手执行抓取动作
    hand_ctrl.crawl(
        hand=hand,
        target_pose_list=hand_move_points,
        target_torque=hand_torque
    )

    time.sleep(1)
    
    # 控制灵巧手回到抓取上方
    jaka.linear_move(jaka_move_points[0],0,True,300)
    
    print(f"按空格键放下 [{type_str}]")
    keyboard.wait('space')
    
    # 控制机械臂来到抓取位置
    jaka.linear_move(jaka_move_points[1],0,True,300)
    
    # 张开灵巧手
    hand_ctrl.drop(hand,hand_move_points)

    # 控制灵巧手回到抓取上方
    jaka.linear_move(jaka_move_points[0],0,True,300)




def crawl_cylinder_demo(jaka,hand):
    # 控制机械臂来到抓取位置上方
    jaka.linear_move(jaka_points.get_cylinder[0],0,True,300)

    # 张开灵巧手
    hand_ctrl.drop(hand,hand_teach_point.poses_get_cylinder)

    print("按空格键开始抓取水瓶...")
    keyboard.wait('space')
    
    # time.sleep(1)
    
    # 控制机械臂来到抓取位置
    jaka.linear_move(jaka_points.get_cylinder[1],0,True,300)
    
    # 控制灵巧手执行抓取动作
    hand_ctrl.crawl(
        hand=hand,
        target_pose_list=hand_teach_point.poses_get_cylinder,
        target_torque=hand_teach_point.torque_get_cylinder
    )

    time.sleep(1)
    
    # 控制灵巧手回到抓取上方
    jaka.linear_move(jaka_points.get_cylinder[0],0,True,300)
    
    print("按空格键放下水瓶...")
    keyboard.wait('space')
    
    # 控制机械臂来到抓取位置
    jaka.linear_move(jaka_points.get_cylinder[1],0,True,300)
    
    # 张开灵巧手
    hand_ctrl.drop(hand,hand_teach_point.poses_get_cylinder)

    # 控制灵巧手回到抓取上方
    jaka.linear_move(jaka_points.get_cylinder[0],0,True,300)

def crawl_box_demo(jaka,hand):
    # 控制机械臂来到抓取位置上方
    jaka.linear_move(jaka_points.get_box[0],0,True,300)
    
    # 张开灵巧手
    hand_ctrl.drop(hand,hand_teach_point.poses_get_box)

    print("按空格键开始抓取纸巾...")
    keyboard.wait('space')
    
    # time.sleep(1)
    
    # 控制机械臂来到抓取位置
    jaka.linear_move(jaka_points.get_box[1],0,True,300)
    
    # 控制灵巧手执行抓取动作
    hand_ctrl.crawl(
        hand=hand,
        target_pose_list=hand_teach_point.poses_get_box,
        target_torque=hand_teach_point.torque_get_box
    )

    time.sleep(1)
    
    # 控制灵巧手回到抓取上方
    jaka.linear_move(jaka_points.get_box[0],0,True,300)
    
    print("按空格键放下纸巾...")
    keyboard.wait('space')
    
    # 控制机械臂来到抓取位置
    jaka.linear_move(jaka_points.get_box[1],0,True,300)
    
    # 张开灵巧手
    hand_ctrl.drop(hand,hand_teach_point.poses_get_box)

    # 控制灵巧手回到抓取上方
    jaka.linear_move(jaka_points.get_box[0],0,True,300)
    


def main():
    hand = LinkerHandApi(hand_type="right", hand_joint="L10")

    jaka = jkrc.RC("10.5.5.100")
    jaka.login()
    # crawl_box_demo(jaka,hand)
    # crawl_cylinder_demo(jaka,hand)
    # crawl_demo(jaka,hand,1)
    # pose = jaka.get_tcp_position() 
    # print(pose)  4
    bag_demo(jaka,hand,2)

if __name__ == '__main__': 
    main()