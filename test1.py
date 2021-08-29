from untitled1 import *

PA = PaClass()
PA.DataFile = r'D:\汇川\采样数据\20210814_快克耦合轴BUG\CNCVariableTrace.txt'
PA.DataFile = r'D:\汇川\采样数据\20210814_快克耦合轴BUG\35Hz.txt'
PA.Ts = 0.001
PA.AxisID_X = 1
PA.AxisID_Y = 2

"""
PA.PlotFlag.NcBlock         = True
PA.PlotFlag.PathVel         = True
PA.PlotFlag.PathAcc         = True
PA.PlotFlag.PosX            = True
PA.PlotFlag.VelX            = True
PA.PlotFlag.AccX            = True
PA.PlotFlag.JerkX           = True
PA.PlotFlag.PosY            = True
PA.PlotFlag.VelY            = True
PA.PlotFlag.AccY            = True
PA.PlotFlag.JerkY           = True
PA.PlotFlag.PosZ            = True
PA.PlotFlag.VelZ            = True
PA.PlotFlag.AccZ            = True
PA.PlotFlag.JerkZ           = True
PA.PlotFlag.XY              = True
PA.PlotFlag.XY_Time         = True
PA.PlotFlag.XY_BlockNo      = True
PA.PlotFlag.XY_PathVel      = True
PA.PlotFlag.XY_PathAcc      = True
PA.PlotFlag.XY_FollowPosErr = True
PA.PlotFlag.YZ              = True
PA.PlotFlag.YZ_Time         = True
PA.PlotFlag.YZ_BlockNo      = True
PA.PlotFlag.YZ_PathVel      = True
PA.PlotFlag.YZ_PathAcc      = True
PA.PlotFlag.YZ_FollowPosErr = True
PA.PlotFlag.XZ              = True
PA.PlotFlag.XZ_Time         = True
PA.PlotFlag.XZ_BlockNo      = True
PA.PlotFlag.XZ_PathVel      = True
PA.PlotFlag.XZ_PathAcc      = True
PA.PlotFlag.XZ_FollowPosErr = True
PA.PlotFlag.XYZ             = True
PA.PlotFlag.XYZ_Time        = True
PA.PlotFlag.XYZ_Z           = True
PA.PlotFlag.XYZ_CmdPathVel  = True
PA.PlotFlag.XYZ_CmdPathAcc  = True
PA.PlotFlag.CircleErr_XY    = True
PA.PlotFlag.CircleErr_YZ    = True
PA.PlotFlag.CircleErr_XZ    = True
"""

PA.LoadData()
PA.PlotData()

x2 = PA.Data[PA.INDEX_CmdPos_X] / 1e3
y2 = PA.Data[PA.INDEX_CmdPos_Y] / 1e3

PA.ShareAxes.Time = PA.Plot1D(x2, axis1Label='Pos (mm)', dataName='CmdPosX', shareAxes=PA.ShareAxes.Time, newFig=True, title='X轴发给伺服的指令位置')

PA.ShareAxes.Time = PA.Plot1D(y2, axis1Label='Pos (mm)', dataName='CmdPosU', shareAxes=PA.ShareAxes.Time, newFig=True, title='U轴发给伺服的指令位置')

PA.ShareAxes.Time = PA.Plot1D(x2-y2, axis1Label='PosErr (mm)', dataName='CmdPosX - CmdPosU', shareAxes=PA.ShareAxes.Time, newFig=True, title='X和U轴的指令偏差')


plt.show()




