#!/usr/bin/env python
# -*-coding:utf-8 -*-

from PaDataAnalyze import PA_Class

PA = PA_Class()
#PA.DataFile = r'F:\yangxiaosheng\1.txt';PA.TimeRange = [10.922, 17.617]
#PA.DataFile = r'F:\yangxiaosheng\2.txt';PA.TimeRange = [9.8, 17.617]
#PA.DataFile = r'F:\yangxiaosheng\3.txt';PA.TimeRange = [9.8, 17.617]
#PA.DataFile = r'F:\yangxiaosheng\4.txt';PA.TimeRange = [0.565, 1.319]
#PA.DataFile = r'F:\yangxiaosheng\5.txt';
#PA.DataFile = r'F:\yangxiaosheng\6.txt';PA.TimeRange = [4.381, 11.11]
PA.DataFile = r'F:\yangxiaosheng\7.txt';PA.TimeRange = [15.555, 21.266]

PA.Ts = 0.001
PA.AxisID_X = 1
PA.AxisID_Y = 2
PA.AxisID_Z = 3
PA.AxisID_A = 13


PA.LoadData()

"""
PA.Data.SetPos_Z = PA.Data.SetPos_A
PA.Data.SetVel_Z = PA.Data.SetVel_A
PA.Data.SetAcc_Z = PA.Data.SetAcc_A
PA.Data.SetJerk_Z = PA.Data.SetJerk_A

PA.Plot.Pos_X      = True
PA.Plot.Vel_X      = True
PA.Plot.Acc_X      = True
PA.Plot.Pos_Y      = True
PA.Plot.Vel_Y      = True
PA.Plot.XY         = True
"""

PA.Plot.PathVel      = True

PA.Plot.Pos_X      = True
PA.Plot.Vel_X      = True
PA.Plot.Acc_X      = True

PA.Plot.Pos_Y      = True
PA.Plot.Vel_Y      = True
PA.Plot.Acc_Y      = True

PA.Plot.XY       = True
PA.Plot.XY_Time       = True
PA.Plot.XY_PathVel         = True
PA.Plot.XY_PathAcc         = True
PA.Plot.XY_PathJerk         = True


PA.Plot.XYZ_Time         = True

PA.PlotData()


#PA.DataInfo(PA.Data.Time, PA.Data.ActVel_X, PA.Data.Var['SCcReal[18]'], infoName=['Time(s)', 'ActVel_X(mm/min)', 'CompValue_X'])
PA.DataInfo()
PA.ShowFigure()




