#!/usr/bin/env python
# -*-coding:utf-8 -*-

from PaDataAnalyze import PA_Data_Analyze

PA = PA_Data_Analyze()
PA.DataFileName = r'D:\汇川\采样数据\20210829-盛利达过切\CNCVariableTrace-盛利达按键过切.txt'

PA.Ts = 0.001
PA.BlockRange = [500, 389480]
#PA.BlockRange = [184320, 186810]
PA.AxisID_X = 1
PA.AxisID_Y = 2
PA.AxisID_Z = 5
PA.AxisID_A = 13

PA.LoadData()

PA.Data.SetPos_Z = PA.Data.SetPos_A
PA.Data.SetVel_Z = PA.Data.SetVel_A
PA.Data.SetAcc_Z = PA.Data.SetAcc_A
PA.Data.SetJerk_Z = PA.Data.SetJerk_A

"""
PA.Plot.Pos_X      = True
PA.Plot.Vel_X      = True
PA.Plot.Acc_X      = True
PA.Plot.Pos_Y      = True
PA.Plot.Vel_Y      = True
PA.Plot.XY         = True
"""

PA.Plot.Pos_X      = True
PA.Plot.Vel_X      = True
PA.Plot.Acc_X      = True
PA.Plot.Jerk_X      = True

PA.Plot.Pos_Z      = True
PA.Plot.Vel_Z      = True
PA.Plot.Acc_Z      = True
PA.Plot.Jerk_Z      = True

PA.Plot.XY_BlockNo         = True
PA.Plot.XZ_BlockNo         = True

PA.Plot.XYZ_Time         = True

PA.Plot.XY_Time       = True
PA.Plot.XY_PathVel         = True
PA.Plot.XY_PathAcc         = True
PA.Plot.XY_PathJerk         = True

PA.Plot.XZ_Y         = True
PA.Plot.XZ_Time         = True
PA.Plot.XZ_PathVel         = True
PA.Plot.XZ_PathAcc         = True
PA.Plot.XZ_PathJerk         = True

PA.PlotData()

PA.Plot1D(PA.Data['CmdPos_Z'] - PA.Data['SetPos_Z'], dataName='CmdPos_Z - ActPos_Z', shareAxes=PA.ShareAxes.Time)

PA.Plot2D(PA.Data.ActPos_X, PA.Data.ActPos_Y, axisName_1='X (mm)', axisName_2='Y (mm)',color=PA.Data.ActPos_Z, colorName='ActZ', dataName='XY_ActZ', shareAxes=PA.ShareAxes.XY)
PA.Plot2D(PA.Data.CmdPos_X, PA.Data.CmdPos_Y, axisName_1='X (mm)', axisName_2='Y (mm)',color=PA.Data.CmdPos_Z, colorName='CmdZ', dataName='XY_CmdZ', shareAxes=PA.ShareAxes.XY)


PA.DataInfo()
PA.ShowFigure()




