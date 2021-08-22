#!/usr/bin/env python
# -*-coding:utf-8 -*-

from PaDataAnalyze import PA_Class

PA = PA_Class()
PA.DataFile = r'C:\PACnc\CNCVariableTrace.txt'
PA.Ts = 0.002
PA.BlockRange = [192000, 0]
PA.AxisID_X = 1
PA.AxisID_Y = 2
PA.AxisID_Z = 3

PA.PlotFlag.BlockNo         = True
PA.PlotFlag.PathVel         = True
PA.PlotFlag.XY_PathAcc         = True
PA.PlotFlag.XY_PathVel           = True
PA.PlotFlag.XYZ_PathVel           = True


PA.LoadData()
PA.PlotData()

x2 = PA.Data['CmdPos_X']
y2 = PA.Data['CmdPos_Y']

"""
PA.ShareAxes.Time = PA.Plot1D(x2, axis1Label='Pos (mm)', dataName='CmdPosX', shareAxes=PA.ShareAxes.Time, newFig=True, title='X轴发给伺服的指令位置')

PA.ShareAxes.Time = PA.Plot1D(y2, axis1Label='Pos (mm)', dataName='CmdPosU', shareAxes=PA.ShareAxes.Time, newFig=True, title='U轴发给伺服的指令位置')

PA.ShareAxes.Time = PA.Plot1D(x2-y2, axis1Label='PosErr (mm)', dataName='CmdPosX - CmdPosU', shareAxes=PA.ShareAxes.Time, newFig=True, title='X和U轴的指令偏差')
"""
PA.AddDataInfo()
PA.ShowFigure()




