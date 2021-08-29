#!/usr/bin/env python
# -*-coding:utf-8 -*-

from PaDataAnalyze import PA_Class

PA = PA_Class()
PA.DataFile = r'E:\\CNCVariableTrace.txt'
PA.DataFile = r'C:\PACnc\CNCVariableTrace.txt'
PA.DataFile = r'D:\汇川\采样数据\20210826-久久象限痕\CNCVariableTrace-QEC滤波位置-圆弧补偿.txt'
PA.DataFile = r'D:\汇川\采样数据\20210829-盛利达过切\CNCVariableTrace-盛利达按键过切.txt'

PA.Ts = 0.001
PA.BlockRange = [500, 389480]
#PA.BlockRange = [184320, 186810]
PA.AxisID_X = 1
PA.AxisID_Y = 2
PA.AxisID_Z = 5
PA.AxisID_A = 13

PA.LoadData()

PA.Data['SetPos_Z'] = PA.Data['SetPos_A']
PA.Data['SetVel_Z'] = PA.Data['SetVel_A']
PA.Data['SetAcc_Z'] = PA.Data['SetAcc_A']
PA.Data['SetJerk_Z'] = PA.Data['SetJerk_A']

"""
PA.PlotFlag.Pos_X      = True
PA.PlotFlag.Vel_X      = True
PA.PlotFlag.Acc_X      = True
PA.PlotFlag.Pos_Y      = True
PA.PlotFlag.Vel_Y      = True
PA.PlotFlag.XY          = True
"""

PA.PlotFlag.Pos_X      = True
PA.PlotFlag.Vel_X      = True
PA.PlotFlag.Acc_X      = True
PA.PlotFlag.Jerk_X      = True

PA.PlotFlag.Pos_Z      = True
PA.PlotFlag.Vel_Z      = True
PA.PlotFlag.Acc_Z      = True
PA.PlotFlag.Jerk_Z      = True

PA.PlotFlag.XY_BlockNo         = True
PA.PlotFlag.XZ_BlockNo         = True

PA.PlotFlag.XYZ_Time         = True

PA.PlotFlag.XY_Time       = True
PA.PlotFlag.XY_PathVel         = True
PA.PlotFlag.XY_PathAcc         = True
PA.PlotFlag.XY_PathJerk         = True

PA.PlotFlag.XZ_Y         = True
PA.PlotFlag.XZ_Time         = True
PA.PlotFlag.XZ_PathVel         = True
PA.PlotFlag.XZ_PathAcc         = True
PA.PlotFlag.XZ_PathJerk         = True

PA.PlotData()

PA.ShareAxes.Time = PA.Plot1D(PA.Data['CmdPos_Z'] - PA.Data['SetPos_Z'], dataName='CmdPos_Z - ActPos_Z', shareAxes=PA.ShareAxes.Time)

PA.ShareAxes.XY = PA.Plot2D(PA.Data['ActPos_X'], PA.Data['ActPos_Y'], axis1Label='X (mm)', axis2Label='Y (mm)',color=PA.Data['ActPos_Z'], colorLabel='ActZ', dataName='XY_ActZ', shareAxes=PA.ShareAxes.XY, newFig=True)
PA.ShareAxes.XY = PA.Plot2D(PA.Data['CmdPos_X'], PA.Data['CmdPos_Y'], axis1Label='X (mm)', axis2Label='Y (mm)',color=PA.Data['CmdPos_Z'], colorLabel='CmdZ', dataName='XY_CmdZ', shareAxes=PA.ShareAxes.XY, newFig=True)


"""

PA.ShareAxes.Time = PA.Plot1D(PA.Data['SCcReal[0]'],dataName='accX', shareAxes=PA.ShareAxes.Time)
PA.ShareAxes.Time = PA.Plot1D(PA.Data['SCcReal[18]'],dataName='CompX', shareAxes=PA.ShareAxes.Time)
PA.ShareAxes.Time = PA.Plot1D(PA.Data['SCcReal[19]'],dataName='CompY', shareAxes=PA.ShareAxes.Time)


x2 = PA.Data['CmdPos_X']
y2 = PA.Data['CmdPos_Y']
PA.ShareAxes.Time = PA.Plot1D(x2, axis1Label='Pos (mm)', dataName='CmdPosX', shareAxes=PA.ShareAxes.Time, newFig=True, title='X轴发给伺服的指令位置')

PA.ShareAxes.Time = PA.Plot1D(y2, axis1Label='Pos (mm)', dataName='CmdPosU', shareAxes=PA.ShareAxes.Time, newFig=True, title='U轴发给伺服的指令位置')

PA.ShareAxes.Time = PA.Plot1D(x2-y2, axis1Label='PosErr (mm)', dataName='CmdPosX - CmdPosU', shareAxes=PA.ShareAxes.Time, newFig=True, title='X和U轴的指令偏差')
"""

#PA.AddDataInfo(PA.Data['Time'], PA.Data['ActVel_X'], PA.Data['SCcReal[18]'], infoName=['Time(s)', 'ActVel_X(mm/min)', 'CompValue_X'])
PA.AddDataInfo(PA.Data['BlockNo'], PA.Data['CmdPos_Z'], PA.Data['ActPos_Z'], infoName=['BlockNo','CmdPos_Z','ActPos_Z'])
PA.ShowFigure()




