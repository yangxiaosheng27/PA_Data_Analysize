#!/usr/bin/env python
# -*-coding:utf-8 -*-

from PaDataAnalyze import PA_Data_Analyze

PA = PA_Data_Analyze()
PA.DataFile = r'D:\汇川\采样数据\20210829-盛利达过切\CNCVariableTrace-盛利达按键过切.txt'

"""
PA.Ts = 0.001
PA.TimeRange = [0, 2]
PA.AxisID_X = 1
PA.AxisID_Y = 2
PA.AxisID_Z = 5
PA.AxisID_A = 13
PA.LoadData()
"""

PA.DataName = []

PA.Data.Length = 4
PA.Data.Time = [1,2,3,4]
PA.Data.SetPos_X=[1,2,3,4]
PA.Data.CmdPos_X=[1,2,3,4]
PA.Data.ActPos_X=[1,2,3,4]
PA.Plot.Pos_X     = True
PA.PlotData()
PA.DataInfo()

from matplotlib import pyplot as plt 

#plt.ion()
fig = plt.figure(1)
fig.clf()
plt.close('all')
a = plt.axis('auto')


PA.Data.Length = 2
PA.Data.Time = [1,2]
PA.Data.SetPos_X=[1,2]
PA.Data.CmdPos_X=[1,2]
PA.Data.ActPos_X=[1,2]
PA.Plot.Pos_X     = True
if 0:
    PA.PlotData()
else:
    PA.FigNum = 0
    PA.Plot1D([1,2], axisName_1='Pos (mm)', dataName='SetPos_X', shareAxes=PA.ShareAxes.Time, figureName='Pos_X', newFig=True)
PA.DataInfo()




PA.ShowFigure()




