#!/usr/bin/env python
# -*-coding:utf-8 -*-

from PaDataAnalyze import PA_Class

PA = PA_Class()
PA.DataFile = r'E:\\CNCVariableTrace.txt'
PA.DataFile = r'C:\PACnc\CNCVariableTrace.txt'
PA.DataFile = r'D:\汇川\采样数据\20210826-久久象限痕\CNCVariableTrace-QEC滤波位置-圆弧补偿.txt'

PA.Ts = 0.001
PA.BlockRange = [0, 0]
PA.AxisID_X = 1
PA.AxisID_Y = 2
PA.AxisID_Z = 3


PA.PlotFlag.Pos_X      = True
PA.PlotFlag.Vel_X      = True
PA.PlotFlag.Acc_X      = True
PA.PlotFlag.Pos_Y      = True
PA.PlotFlag.Vel_Y      = True
PA.PlotFlag.XY          = True


PA.LoadData()
PA.PlotData()

PA.ShareAxes.Time = PA.Plot1D(PA.Data['SCcReal[0]'],dataName='accX', shareAxes=PA.ShareAxes.Time)
PA.ShareAxes.Time = PA.Plot1D(PA.Data['SCcReal[18]'],dataName='CompX', shareAxes=PA.ShareAxes.Time)
PA.ShareAxes.Time = PA.Plot1D(PA.Data['SCcReal[19]'],dataName='CompY', shareAxes=PA.ShareAxes.Time)

"""
x2 = PA.Data['CmdPos_X']
y2 = PA.Data['CmdPos_Y']
PA.ShareAxes.Time = PA.Plot1D(x2, axis1Label='Pos (mm)', dataName='CmdPosX', shareAxes=PA.ShareAxes.Time, newFig=True, title='X轴发给伺服的指令位置')

PA.ShareAxes.Time = PA.Plot1D(y2, axis1Label='Pos (mm)', dataName='CmdPosU', shareAxes=PA.ShareAxes.Time, newFig=True, title='U轴发给伺服的指令位置')

PA.ShareAxes.Time = PA.Plot1D(x2-y2, axis1Label='PosErr (mm)', dataName='CmdPosX - CmdPosU', shareAxes=PA.ShareAxes.Time, newFig=True, title='X和U轴的指令偏差')
"""

PA.AddDataInfo(PA.Data['Time'], PA.Data['ActVel_X'], PA.Data['SCcReal[18]'], infoName=['Time(s)', 'ActVel_X(mm/min)', 'CompValue_X'])
#PA.AddDataInfo()
PA.ShowFigure()




