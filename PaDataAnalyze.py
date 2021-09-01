#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
@File           PaDataAnalyze.py
@Brief          PA data analysis
@Unit of File   
                SSetPos                         Unit: internal increment
                CommandedMachinePosCorr         Unit: internal increment
                SActMachinePos                  Unit: internal increment
                PathVelocity                    Unit: internal increment / Ts
                CommandedPathVelocity           Unit: internal increment / Ts
@Unit of Data   
                PA.Data['SetPathVel']           Unit: mm/min
                PA.Data['CmdPathVel']           Unit: mm/min
                PA.Data['SetPathAcc']           Unit: m/s^2
                PA.Data['CmdPathAcc']           Unit: m/s^2
                PA.Data['SetPathJerk']          Unit: m/s^3
                PA.Data['CmdPathJerk']          Unit: m/s^3
                PA.Data['SetPos_X']             Unit: mm
                PA.Data['CmdPos_X']             Unit: mm
                PA.Data['ActPos_X']             Unit: mm
                PA.Data['SetVel_X']             Unit: mm/min
                PA.Data['CmdVel_X']             Unit: mm/min
                PA.Data['ActVel_X']             Unit: mm/min
                PA.Data['SetAcc_X']             Unit: m/s^2
                PA.Data['CmdAcc_X']             Unit: m/s^2
                PA.Data['ActAcc_X']             Unit: m/s^2
                PA.Data['SetJerk_X']            Unit: m/s^3
                PA.Data['CmdJerk_X']            Unit: m/s^3
                PA.Data['ActJerk_X]'            Unit: m/s^3
                
Note            The internal increment defaults to 1um, Ts defaults to 0.001s
"""

############################### Version History #################################
# ---------------------------------Version 4.4--------------------------------- #
# Date: 2021/8/30
# Author: yangxiaosheng
# Update: fix some bug in TimeRange checking
# ---------------------------------Version 4.3--------------------------------- #
# Date: 2021/8/28
# Author: yangxiaosheng
# Update: fix some bug in using mpldatacursor
# ---------------------------------Version 4.2--------------------------------- #
# Date: 2021/8/22
# Author: yangxiaosheng
# Update: add mpldatacursor
# ---------------------------------Version 4.1--------------------------------- #
# Date: 2021/8/17
# Author: yangxiaosheng
# Update: fix some bug in plotting figure
# ---------------------------------Version 4.0--------------------------------- #
# Date: 2021/8/15
# Author: yangxiaosheng
# Update: Refactor code to improve portability, and remove GUI (using matplotlib) because of bad smooth running
# ---------------------------------Version 3.0--------------------------------- #
# Date: 2021/7/20
# Author: yangxiaosheng
# Update: make a GUI using matplotlib
# ---------------------------------Version 2.2--------------------------------- #
# Date: 2021/7/1
# Author: yangxiaosheng
# Update: Plot the polar data of a circular trajectory
# ---------------------------------Version 2.1--------------------------------- #
# Date: 2021/6/30
# Author: yangxiaosheng
# Update: Add Axis Idenx
# ---------------------------------Version 2.0--------------------------------- #
# Date: 2021/5/21
# Author: yangxiaosheng
# Update: Add widgets: Select NC Block
# ---------------------------------Version 1.3--------------------------------- #
# Date: 2021/5/21
# Author: yangxiaosheng
# Update: Add TimeRange and BlockRange
# ---------------------------------Version 1.2--------------------------------- #
# Date: 2021/5/20
# Author: yangxiaosheng
# Update: Add shared axes, add color bar, and optimize color drawing
# ---------------------------------Version 1.1--------------------------------- #
# Date: 2021/5/19
# Author: yangxiaosheng
# Update: Optimize loading speed, and increase loading progress and draw progress
# ---------------------------------Version 1.0--------------------------------- #
# Date: 2021/5/18
# Author: yangxiaosheng
# Update: Init Version
#################################################################################

from mpldatacursor import datacursor
from matplotlib import pyplot as plt
import numpy as np
import matplotlib
import numpy
import sys
import re


class PA_Class:
    
    def __init__(self):
        self.initParam()
    
    def initParam(self):
        ##################################################################################
        # ----------------------------------User Define--------------------------------- #
        ##################################################################################
        self.Precision_um   = 1; # 1 internal incremental = Precision_um * 1um
        self.Ts             = 0.001  # sample time, unit: s
        self.DataFile       = r'F:\CNCVariableTrace.txt'
        self.TimeRange      = [0, 0] # select the sample data in Time range of [minTime, maxTime] (unit: s) ([0, 0] means select all Time)
        self.BlockRange     = [0, 0] # select the sample data in NC Block range of [minBlockNo, maxBlockNo] ([0, 0] means select all NC Block)
        self.Plot           = self.PlotFlag_Class()
        self.AxisID_X       = 0  # 0 means no axis,1 means the first axis
        self.AxisID_Y       = 0  # 0 means no axis,1 means the first axis
        self.AxisID_Z       = 0  # 0 means no axis,1 means the first axis
        self.AxisID_A       = 0  # 0 means no axis,1 means the first axis

        ##################################################################################
        # -------------------------------Internal Param--------------------------------- #
        ##################################################################################
        self.FigNum                 = 0
        self.HMI_Title              = 'PA Data Analysis'
        self.Data                   = dict()
        self.ShareAxes              = self.ShareAxes_Class()
        self.reSplit                = re.compile("[\t\n ]")
        self.reMatch                = re.compile("[-+0-9\\.]*")
        self.ParamName_SetPos       = 'SSetPos[%d]'
        self.ParamName_CmdPos       = 'CommandedMachinePosCorr[%d]'
        self.ParamName_ActPos       = 'SActMachinePos[%d]'
        self.ParamName_SetPathVel   = 'PathVelocity[0]'
        self.ParamName_CmdPathVel   = 'CommandedPathVelocity[0]'
        self.ParamName_BlockNo      = 'BlockNoActive[0]'
    
    class ShareAxes_Class:
        Time = None
        XY = None
        YZ = None
        XZ = None

    class PlotFlag_Class:
        BlockNo         = False
        PathVel         = False
        PathAcc         = False
        PathJerk        = False
        Pos_X           = False
        Vel_X           = False
        Acc_X           = False
        Jerk_X          = False
        Pos_Y           = False
        Vel_Y           = False
        Acc_Y           = False
        Jerk_Y          = False
        Pos_Z           = False
        Vel_Z           = False
        Acc_Z           = False
        Jerk_Z          = False
        Pos_A           = False
        Vel_A           = False
        Acc_A           = False
        Jerk_A          = False
        XY              = False
        XY_Time         = False
        XY_BlockNo      = False
        XY_PathVel      = False
        XY_PathAcc      = False
        XY_PathJerk     = False
        XY_PosErr       = False
        YZ              = False
        YZ_Time         = False
        YZ_BlockNo      = False
        YZ_PathVel      = False
        YZ_PathAcc      = False
        YZ_PathJerk     = False
        YZ_PosErr       = False
        XZ              = False
        XZ_Time         = False
        XZ_BlockNo      = False
        XZ_PathVel      = False
        XZ_PathAcc      = False
        XZ_PathJerk     = False
        XZ_PosErr       = False
        XYZ             = False
        XYZ_Time        = False
        XYZ_Z           = False
        XYZ_PathVel     = False
        XYZ_PathAcc     = False
        XYZ_PathJerk    = False
        CircleErr_XY    = False
        CircleErr_YZ    = False
        CircleErr_XZ    = False

    ##################################################################################
    # -----------------------------------Plot Data---------------------------------- #
    ##################################################################################
    def PlotData(self):
        
        if self.Data['DataLen'] == 0:
            return None
        
        plt.close(fig='all')
        
        # ---------------------------------Plot 1D---------------------------------- #
        # BlockNo
        if self.Plot.BlockNo == True:
            try:
                block = self.Data['BlockNo']
                self.ShareAxes.Time = self.Plot1D(block, dataName='BlockNo', figureName='BlockNo', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError BlockNo\033[0m')

        # PathVel
        if self.Plot.PathVel == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetPathVel'], axisName_1='Vel (mm/min)', dataName='SetPathVel', shareAxes=self.ShareAxes.Time, figureName='PathVel', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdPathVel'], axisName_1='Vel (mm/min)', dataName='CmdPathVel', shareAxes=self.ShareAxes.Time, figureName='PathVel', newFig=False)
                if self.Data['ActPathVel'].__len__() != 0:
                    self.ShareAxes.Time = self.Plot1D(self.Data['ActPathVel'], axisName_1='Vel (mm/min)', dataName='ActPathVel', shareAxes=self.ShareAxes.Time, figureName='PathVel', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError PathVel\033[0m')

        # PathAcc
        if self.Plot.PathAcc == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetPathAcc'], axisName_1='Acc (m/s^2)', dataName='SetPathAcc', shareAxes=self.ShareAxes.Time, figureName='PathAcc', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdPathAcc'], axisName_1='Acc (m/s^2)', dataName='CmdPathAcc', shareAxes=self.ShareAxes.Time, figureName='PathAcc', newFig=False)
                #if self.Data['ActPathAcc'].__len__() != 0:
                    #self.ShareAxes.Time = self.Plot1D(self.Data['ActPathAcc'], axisName_1='Acc (m/s^2)', dataName='ActPathAcc', shareAxes=self.ShareAxes.Time, figureName='PathAcc', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError PathAcc\033[0m')

        # PathJerk
        if self.Plot.PathJerk == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetPathJerk'], axisName_1='Jerk (m/s^3)', dataName='SetPathJerk', shareAxes=self.ShareAxes.Time, figureName='PathJerk', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdPathJerk'], axisName_1='Jerk (m/s^3)', dataName='CmdPathJerk', shareAxes=self.ShareAxes.Time, figureName='PathJerk', newFig=False)
                #if self.Data['ActPathJerk'].__len__() != 0:
                    #self.ShareAxes.Time = self.Plot1D(self.Data['ActPathJerk'], axisName_1='Jerk (m/s^3)', dataName='ActPathJerk', shareAxes=self.ShareAxes.Time, figureName='PathJerk', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError PathJerk\033[0m')

        # X
        # Pos_X
        if self.Plot.Pos_X == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetPos_X'], axisName_1='Pos (mm)', dataName='SetPos_X', shareAxes=self.ShareAxes.Time, figureName='Pos_X', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdPos_X'], axisName_1='Pos (mm)', dataName='CmdPos_X', shareAxes=self.ShareAxes.Time, figureName='Pos_X', newFig=False)
                self.ShareAxes.Time = self.Plot1D(self.Data['ActPos_X'], axisName_1='Pos (mm)', dataName='ActPos_X', shareAxes=self.ShareAxes.Time, figureName='Pos_X', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Pos_X\033[0m')
        # Vel_X
        if self.Plot.Vel_X == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetVel_X'], axisName_1='Vel (mm/min)', dataName='SetVel_X', shareAxes=self.ShareAxes.Time, figureName='Vel_X', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdVel_X'], axisName_1='Vel (mm/min)', dataName='CmdVel_X', shareAxes=self.ShareAxes.Time, figureName='Vel_X', newFig=False)
                self.ShareAxes.Time = self.Plot1D(self.Data['ActVel_X'], axisName_1='Vel (mm/min)', dataName='ActVel_X', shareAxes=self.ShareAxes.Time, figureName='Vel_X', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Vel_X\033[0m')
        # Acc_X
        if self.Plot.Acc_X == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetAcc_X'], axisName_1='Acc (m/s^2)', dataName='SetAcc_X', shareAxes=self.ShareAxes.Time, figureName='Acc_X', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdAcc_X'], axisName_1='Acc (m/s^2)', dataName='CmdAcc_X', shareAxes=self.ShareAxes.Time, figureName='Acc_X', newFig=False)
                self.ShareAxes.Time = self.Plot1D(self.Data['ActAcc_X'], axisName_1='Acc (m/s^2)', dataName='ActAcc_X', shareAxes=self.ShareAxes.Time, figureName='Acc_X', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Acc_X\033[0m')
        # Jerk_X
        if self.Plot.Jerk_X == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetJerk_X'], axisName_1='Jerk (m/s^3)', dataName='SetJerk_X', shareAxes=self.ShareAxes.Time, figureName='Jerk_X', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdJerk_X'], axisName_1='Jerk (m/s^3)', dataName='CmdJerk_X', shareAxes=self.ShareAxes.Time, figureName='Jerk_X', newFig=False)
                # self.ShareAxes.Time = self.Plot1D(self.Data['ActJerk_X'], axisName_1='Jerk (m/s^3)', dataName='ActJerk_X', shareAxes=self.ShareAxes.Time, figureName='Jerk_X', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Jerk_X\033[0m')

        # Y
        # Pos_Y
        if self.Plot.Pos_Y == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetPos_Y'], axisName_1='Pos (mm)', dataName='SetPos_Y', shareAxes=self.ShareAxes.Time, figureName='Pos_Y', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdPos_Y'], axisName_1='Pos (mm)', dataName='CmdPos_Y', shareAxes=self.ShareAxes.Time, figureName='Pos_Y', newFig=False)
                self.ShareAxes.Time = self.Plot1D(self.Data['ActPos_Y'], axisName_1='Pos (mm)', dataName='ActPos_Y', shareAxes=self.ShareAxes.Time, figureName='Pos_Y', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Pos_Y\033[0m')
        # Vel_Y
        if self.Plot.Vel_Y == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetVel_Y'], axisName_1='Vel (mm/min)', dataName='SetVel_Y', shareAxes=self.ShareAxes.Time, figureName='Vel_Y', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdVel_Y'], axisName_1='Vel (mm/min)', dataName='CmdVel_Y', shareAxes=self.ShareAxes.Time, figureName='Vel_Y', newFig=False)
                self.ShareAxes.Time = self.Plot1D(self.Data['ActVel_Y'], axisName_1='Vel (mm/min)', dataName='ActVel_Y', shareAxes=self.ShareAxes.Time, figureName='Vel_Y', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Vel_Y\033[0m')
        # Acc_Y
        if self.Plot.Acc_Y == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetAcc_Y'], axisName_1='Acc (m/s^2)', dataName='SetAcc_Y', shareAxes=self.ShareAxes.Time, figureName='Acc_Y', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdAcc_Y'], axisName_1='Acc (m/s^2)', dataName='CmdAcc_Y', shareAxes=self.ShareAxes.Time, figureName='Acc_Y', newFig=False)
                self.ShareAxes.Time = self.Plot1D(self.Data['ActAcc_Y'], axisName_1='Acc (m/s^2)', dataName='ActAcc_Y', shareAxes=self.ShareAxes.Time, figureName='Acc_Y', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Acc_Y\033[0m')
        # Jerk_Y
        if self.Plot.Jerk_Y == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetJerk_Y'], axisName_1='Jerk (m/s^3)', dataName='SetJerk_Y', shareAxes=self.ShareAxes.Time, figureName='Jerk_Y', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdJerk_Y'], axisName_1='Jerk (m/s^3)', dataName='CmdJerk_Y', shareAxes=self.ShareAxes.Time, figureName='Jerk_Y', newFig=False)
                # self.ShareAxes.Time = self.Plot1D(self.Data['ActJerk_Y'], axisName_1='Jerk (m/s^3)', dataName='ActJerk_Y', shareAxes=self.ShareAxes.Time, figureName='Jerk_Y', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Jerk_Y\033[0m')

        # Z
        #Pos_Z
        if self.Plot.Pos_Z == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetPos_Z'], axisName_1='Pos (mm)', dataName='SetPos_Z', shareAxes=self.ShareAxes.Time, figureName='Pos_Z', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdPos_Z'], axisName_1='Pos (mm)', dataName='CmdPos_Z', shareAxes=self.ShareAxes.Time, figureName='Pos_Z', newFig=False)
                self.ShareAxes.Time = self.Plot1D(self.Data['ActPos_Z'], axisName_1='Pos (mm)', dataName='ActPos_Z', shareAxes=self.ShareAxes.Time, figureName='Pos_Z', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Pos_Z\033[0m')
        #Vel_Z
        if self.Plot.Vel_Z == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetVel_Z'], axisName_1='Vel (mm/min)', dataName='SetVel_Z', shareAxes=self.ShareAxes.Time, figureName='Vel_Z', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdVel_Z'], axisName_1='Vel (mm/min)', dataName='CmdVel_Z', shareAxes=self.ShareAxes.Time, figureName='Vel_Z', newFig=False)
                self.ShareAxes.Time = self.Plot1D(self.Data['ActVel_Z'], axisName_1='Vel (mm/min)', dataName='ActVel_Z', shareAxes=self.ShareAxes.Time, figureName='Vel_Z', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Vel_Z\033[0m')
        #Acc_Z
        if self.Plot.Acc_Z == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetAcc_Z'], axisName_1='Acc (m/s^2)', dataName='SetAcc_Z', shareAxes=self.ShareAxes.Time, figureName='Acc_Z', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdAcc_Z'], axisName_1='Acc (m/s^2)', dataName='CmdAcc_Z', shareAxes=self.ShareAxes.Time, figureName='Acc_Z', newFig=False)
                self.ShareAxes.Time = self.Plot1D(self.Data['ActAcc_Z'], axisName_1='Acc (m/s^2)', dataName='ActAcc_Z', shareAxes=self.ShareAxes.Time, figureName='Acc_Z', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Acc_Z\033[0m')
        # Jerk_Z
        if self.Plot.Jerk_Z == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetJerk_Z'], axisName_1='Jerk (m/s^3)', dataName='SetJerk_Z', shareAxes=self.ShareAxes.Time, figureName='Jerk_Z', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdJerk_Z'], axisName_1='Jerk (m/s^3)', dataName='CmdJerk_Z', shareAxes=self.ShareAxes.Time, figureName='Jerk_Z', newFig=False)
                # self.ShareAxes.Time = self.Plot1D(self.Data['ActJerk_Z'], axisName_1='Jerk (m/s^3)', dataName='ActJerk_Z', shareAxes=self.ShareAxes.Time, figureName='Jerk_Z', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Jerk_Z\033[0m')

        # A
        #Pos_A
        if self.Plot.Pos_A == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetPos_A'], axisName_1='Pos (mm)', dataName='SetPos_A', shareAxes=self.ShareAxes.Time, figureName='Pos_A', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdPos_A'], axisName_1='Pos (mm)', dataName='CmdPos_A', shareAxes=self.ShareAxes.Time, figureName='Pos_A', newFig=False)
                self.ShareAxes.Time = self.Plot1D(self.Data['ActPos_A'], axisName_1='Pos (mm)', dataName='ActPos_A', shareAxes=self.ShareAxes.Time, figureName='Pos_A', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Pos_A\033[0m')
        #Vel_A
        if self.Plot.Vel_A == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetVel_A'], axisName_1='Vel (mm/min)', dataName='SetVel_A', shareAxes=self.ShareAxes.Time, figureName='Vel_A', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdVel_A'], axisName_1='Vel (mm/min)', dataName='CmdVel_A', shareAxes=self.ShareAxes.Time, figureName='Vel_A', newFig=False)
                self.ShareAxes.Time = self.Plot1D(self.Data['ActVel_A'], axisName_1='Vel (mm/min)', dataName='ActVel_A', shareAxes=self.ShareAxes.Time, figureName='Vel_A', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Vel_A\033[0m')
        #Acc_A
        if self.Plot.Acc_A == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetAcc_A'], axisName_1='Acc (m/s^2)', dataName='SetAcc_A', shareAxes=self.ShareAxes.Time, figureName='Acc_A', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdAcc_A'], axisName_1='Acc (m/s^2)', dataName='CmdAcc_A', shareAxes=self.ShareAxes.Time, figureName='Acc_A', newFig=False)
                self.ShareAxes.Time = self.Plot1D(self.Data['ActAcc_A'], axisName_1='Acc (m/s^2)', dataName='ActAcc_A', shareAxes=self.ShareAxes.Time, figureName='Acc_A', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Acc_A\033[0m')
        # Jerk_A
        if self.Plot.Jerk_A == True:
            try:
                self.ShareAxes.Time = self.Plot1D(self.Data['SetJerk_A'], axisName_1='Jerk (m/s^3)', dataName='SetJerk_A', shareAxes=self.ShareAxes.Time, figureName='Jerk_A', newFig=True)
                self.ShareAxes.Time = self.Plot1D(self.Data['CmdJerk_A'], axisName_1='Jerk (m/s^3)', dataName='CmdJerk_A', shareAxes=self.ShareAxes.Time, figureName='Jerk_A', newFig=False)
                # self.ShareAxes.Time = self.Plot1D(self.Data['ActJerk_A'], axisName_1='Jerk (m/s^3)', dataName='ActJerk_A', shareAxes=self.ShareAxes.Time, figureName='Jerk_A', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Jerk_A\033[0m')

        # ---------------------------------Plot 2D---------------------------------- #
        # XY
        if self.Plot.XY == True:
            try:
                self.ShareAxes.XY = self.Plot2D(self.Data['SetPos_X'], self.Data['SetPos_Y'], axisName_1='X (mm)', axisName_2='Y (mm)', dataName='SetPos', shareAxes=self.ShareAxes.XY, figureName='XY', newFig=True)
                self.ShareAxes.XY = self.Plot2D(self.Data['CmdPos_X'], self.Data['CmdPos_Y'], axisName_1='X (mm)', axisName_2='Y (mm)', dataName='CmdPos', shareAxes=self.ShareAxes.XY, figureName='XY', newFig=False)
                self.ShareAxes.XY = self.Plot2D(self.Data['ActPos_X'], self.Data['ActPos_Y'], axisName_1='X (mm)', axisName_2='Y (mm)', dataName='ActPos', shareAxes=self.ShareAxes.XY, figureName='XY', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XY\033[0m')
        # XY with BlockNo
        if self.Plot.XY_BlockNo == True:
            try:
                color = self.Data['BlockNo']
                self.ShareAxes.XY = self.Plot2D(self.Data['SetPos_X'], self.Data['SetPos_Y'], color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='BlockNo', shareAxes=self.ShareAxes.XY, figureName='XY_BlockNo', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError BlockNo\033[0m')
        # XY with Time
        if self.Plot.XY_Time == True:
            try:
                color = self.Data['Time']
                self.ShareAxes.XY = self.Plot2D(self.Data['CmdPos_X'], self.Data['CmdPos_Y'], color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='Time (s)', shareAxes=self.ShareAxes.XY, figureName='XY_Time', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_Time\033[0m')
        #XY with PathVel
        if self.Plot.XY_PathVel == True:
            try:
                color = self.Data['CmdPathVel']
                self.ShareAxes.XY = self.Plot2D(self.Data['CmdPos_X'], self.Data['CmdPos_Y'], color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='PathVel (mm/min)', shareAxes=self.ShareAxes.XY, figureName='XY_PathVel', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_PathVel\033[0m')
        #XY with PathAcc
        if self.Plot.XY_PathAcc == True:
            try:
                color = self.Data['CmdPathAcc']
                self.ShareAxes.XY = self.Plot2D(self.Data['CmdPos_X'], self.Data['CmdPos_Y'], color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='PathAcc (m/s^2)', shareAxes=self.ShareAxes.XY, figureName='XY_PathAcc', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_PathAcc\033[0m')
        #XY with PathJerk
        if self.Plot.XY_PathJerk == True:
            try:
                color = self.Data['CmdPathJerk']
                self.ShareAxes.XY = self.Plot2D(self.Data['CmdPos_X'], self.Data['CmdPos_Y'], color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='PathJerk (m/s^3)', shareAxes=self.ShareAxes.XY, figureName='XY_PathJerk', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_PathJerk\033[0m')
        #XY with PosErr
        if self.Plot.XY_PosErr == True:
            try:
                if self.Data['PosErr'].__len__() != 0:
                    color = self.Data['PosErr']
                    self.ShareAxes.XY = self.Plot2D(self.Data['CmdPos_X'], self.Data['CmdPos_Y'], color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='PosErr (mm)', shareAxes=self.ShareAxes.XY, figureName='XY_PosErr', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_PosErr\033[0m')
        
        # YZ
        if self.Plot.YZ == True:
            try:
                self.ShareAxes.YZ = self.Plot2D(self.Data['SetPos_Y'], self.Data['SetPos_Z'], axisName_1='Y (mm)', axisName_2='Z (mm)', dataName='SetPos', shareAxes=self.ShareAxes.YZ, figureName='YZ', newFig=True)
                self.ShareAxes.YZ = self.Plot2D(self.Data['CmdPos_Y'], self.Data['CmdPos_Z'], axisName_1='Y (mm)', axisName_2='Z (mm)', dataName='CmdPos', shareAxes=self.ShareAxes.YZ, figureName='YZ', newFig=False)
                self.ShareAxes.YZ = self.Plot2D(self.Data['ActPos_Y'], self.Data['ActPos_Z'], axisName_1='Y (mm)', axisName_2='Z (mm)', dataName='ActPos', shareAxes=self.ShareAxes.YZ, figureName='YZ', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ\033[0m')
        # YZ with BlockNo
        if self.Plot.YZ_BlockNo == True:
            try:
                color = self.Data['BlockNo']
                self.ShareAxes.YZ = self.Plot2D(self.Data['SetPos_Y'], self.Data['SetPos_Z'], color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='BlockNo', shareAxes=self.ShareAxes.YZ, figureName='YZ_BlockNo', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_BlockNo\033[0m')
        # YZ with Time
        if self.Plot.YZ_Time == True:
            try:
                color = self.Data['Time']
                self.ShareAxes.YZ = self.Plot2D(self.Data['CmdPos_Y'], self.Data['CmdPos_Z'], color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='Time (s)', shareAxes=self.ShareAxes.YZ, figureName='YZ_Time', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_Time\033[0m')
        #YZ with PathVel
        if self.Plot.YZ_PathVel == True:
            try:
                color = self.Data['CmdPathVel']
                self.ShareAxes.YZ = self.Plot2D(self.Data['CmdPos_Y'], self.Data['CmdPos_Z'], color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='PathVel (mm/min)', shareAxes=self.ShareAxes.YZ, figureName='YZ_PathVel', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_PathVel\033[0m')
        #YZ with PathAcc
        if self.Plot.YZ_PathAcc == True:
            try:
                color = self.Data['CmdPathAcc']
                self.ShareAxes.YZ = self.Plot2D(self.Data['CmdPos_Y'], self.Data['CmdPos_Z'], color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='PathAcc (m/s^2)', shareAxes=self.ShareAxes.YZ, figureName='YZ_PathAcc', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_PathAcc\033[0m')
        #YZ with PathJerk
        if self.Plot.YZ_PathJerk == True:
            try:
                color = self.Data['CmdPathJerk']
                self.ShareAxes.YZ = self.Plot2D(self.Data['CmdPos_Y'], self.Data['CmdPos_Z'], color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='PathJerk (m/s^3)', shareAxes=self.ShareAxes.YZ, figureName='YZ_PathJerk', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_PathJerk\033[0m')
        #YZ with PosErr
        if self.Plot.YZ_PosErr == True:
            try:
                if self.Data['PosErr'].__len__() != 0:
                    color = self.Data['PosErr']
                    self.ShareAxes.YZ = self.Plot2D(self.Data['CmdPos_Y'], self.Data['CmdPos_Z'], color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='PosErr (mm)', shareAxes=self.ShareAxes.YZ, figureName='YZ_PosErr', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_PosErr\033[0m')

        # XZ
        if self.Plot.XZ == True:
            try:
                self.ShareAxes.XZ = self.Plot2D(self.Data['SetPos_X'], self.Data['SetPos_Z'], axisName_1='X (mm)', axisName_2='Z (mm)', dataName='SetPos', shareAxes=self.ShareAxes.XZ, figureName='XZ', newFig=True)
                self.ShareAxes.XZ = self.Plot2D(self.Data['CmdPos_X'], self.Data['CmdPos_Z'], axisName_1='X (mm)', axisName_2='Z (mm)', dataName='CmdPos', shareAxes=self.ShareAxes.XZ, figureName='XZ', newFig=False)
                self.ShareAxes.XZ = self.Plot2D(self.Data['ActPos_X'], self.Data['ActPos_Z'], axisName_1='X (mm)', axisName_2='Z (mm)', dataName='ActPos', shareAxes=self.ShareAxes.XZ, figureName='XZ', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ\033[0m')
        # XZ with BlockNo
        if self.Plot.XZ_BlockNo == True:
            try:
                color = self.Data['BlockNo']
                self.ShareAxes.XZ = self.Plot2D(self.Data['SetPos_X'], self.Data['SetPos_Z'], color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='BlockNo', shareAxes=self.ShareAxes.XZ, figureName='XZ_BlockNo', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_BlockNo\033[0m')
        # XZ with Time
        if self.Plot.XZ_Time == True:
            try:
                color = self.Data['Time']
                self.ShareAxes.XZ = self.Plot2D(self.Data['CmdPos_X'], self.Data['CmdPos_Z'], color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='Time (s)', shareAxes=self.ShareAxes.XZ, figureName='XZ_Time', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_Time\033[0m')
        #XZ with PathVel
        if self.Plot.XZ_PathVel == True:
            try:
                color = self.Data['CmdPathVel']
                self.ShareAxes.XZ = self.Plot2D(self.Data['CmdPos_X'], self.Data['CmdPos_Z'], color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='PathVel (mm/min)', shareAxes=self.ShareAxes.XZ, figureName='XZ_PathVel', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_PathVel\033[0m')
        #XZ with PathAcc
        if self.Plot.XZ_PathAcc == True:
            try:
                color = self.Data['CmdPathAcc']
                self.ShareAxes.XZ = self.Plot2D(self.Data['CmdPos_X'], self.Data['CmdPos_Z'], color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='PathAcc (m/s^2)', shareAxes=self.ShareAxes.XZ, figureName='XZ_PathAcc', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_PathAcc\033[0m')
        #XZ with PathJerk
        if self.Plot.XZ_PathJerk == True:
            try:
                color = self.Data['CmdPathJerk']
                self.ShareAxes.XZ = self.Plot2D(self.Data['CmdPos_X'], self.Data['CmdPos_Z'], color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='PathJerk (m/s^3)', shareAxes=self.ShareAxes.XZ, figureName='XZ_PathJerk', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_PathJerk\033[0m')
        #XZ with PosErr
        if self.Plot.XZ_PosErr == True:
            try:
                if self.Data['PosErr'].__len__() != 0:
                    color = self.Data['PosErr']
                    self.ShareAxes.XZ = self.Plot2D(self.Data['CmdPos_X'], self.Data['CmdPos_Z'], color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='PosErr (mm)', shareAxes=self.ShareAxes.XZ, figureName='XZ_PosErr', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_PosErr\033[0m')

        # ---------------------------------Plot 3D---------------------------------- #
        #XYZ
        if self.Plot.XYZ == True:
            try:
                self.Plot3D(self.Data['SetPos_X'], self.Data['SetPos_Y'], self.Data['SetPos_Z'], axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', dataName='SetPos', figureName='XYZ', newFig=True)
                self.Plot3D(self.Data['CmdPos_X'], self.Data['CmdPos_Y'], self.Data['CmdPos_Z'], axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', dataName='CmdPos', figureName='XYZ', newFig=False)
                self.Plot3D(self.Data['ActPos_X'], self.Data['ActPos_Y'], self.Data['ActPos_Z'], axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', dataName='ActPos', figureName='XYZ', newFig=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ\033[0m')

        #XYZ with Time
        if self.Plot.XYZ_Time == True:
            try:
                color = self.Data['Time']
                self.Plot3D(self.Data['ActPos_X'], self.Data['ActPos_Y'], self.Data['ActPos_Z'], color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='Time (s)', figureName='XYZ_Time', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_Time\033[0m')

        #XYZ with Z
        if self.Plot.XYZ_Z == True:
            try:
                color = self.Data['ActPos_Z']
                self.Plot3D(self.Data['ActPos_X'], self.Data['ActPos_Y'], self.Data['ActPos_Z'], color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='Z (mm)', figureName='XYZ_Z', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_Z\033[0m')

        #XYZ with CmdPathVel
        if self.Plot.XYZ_PathVel == True:
            try:
                color = self.Data['CmdPathVel']
                self.Plot3D(self.Data['ActPos_X'], self.Data['ActPos_Y'], self.Data['ActPos_Z'], color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='PathVel (mm/min)', figureName='XYZ_PathVel', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_PathVel\033[0m')

        #XYZ with CmdPathAcc
        if self.Plot.XYZ_PathAcc == True:
            try:
                color = self.Data['CmdPathAcc']
                self.Plot3D(self.Data['ActPos_X'], self.Data['ActPos_Y'], self.Data['ActPos_Z'], color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='PathAcc (m/s^2)', figureName='XYZ_PathAcc', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_PathAcc\033[0m')

        #XYZ with CmdPathJerk
        if self.Plot.XYZ_PathJerk == True:
            try:
                color = self.Data['CmdPathJerk']
                self.Plot3D(self.Data['ActPos_X'], self.Data['ActPos_Y'], self.Data['ActPos_Z'], color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='PathJerk (m/s^3)', figureName='XYZ_PathJerk', newFig=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_PathJerk\033[0m')

        # ----------------------------Plot Circle Error----------------------------- #
        # circular error of XY
        if self.Plot.CircleErr_XY == True:
            try:
                Center1 = (max(self.Data['SetPos_X']) + min(self.Data['SetPos_X'])) / 2
                Center2 = (max(self.Data['SetPos_Y']) + min(self.Data['SetPos_Y'])) / 2
                R_MaxErr = 0.05
                R = (max(self.Data['SetPos_X']) - min(self.Data['SetPos_X'])) / 2
                self.PlotCircleError(R, R_MaxErr, Center1, Center2, self.Data['CmdPos_X'], self.Data['CmdPos_Y'], self.Data['ActPos_X'], self.Data['ActPos_Y'], F=None, figureName='CircleErr_XY')
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError CircleErr_XY\033[0m')

        # circular error of YZ
        if self.Plot.CircleErr_YZ == True:
            try:
                Center1 = (max(self.Data['SetPos_Y']) + min(self.Data['SetPos_Y'])) / 2
                Center2 = (max(self.Data['SetPos_Z']) + min(self.Data['SetPos_Z'])) / 2
                R_MaxErr = 0.05
                R = (max(self.Data['SetPos_Y']) - min(self.Data['SetPos_Y'])) / 2
                self.PlotCircleError(R, R_MaxErr, Center1, Center2, self.Data['CmdPos_Y'], self.Data['CmdPos_Z'], self.Data['ActPos_Y'], self.Data['ActPos_Z'], F=None, figureName='CircleErr_YZ')
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError CircleErr_YZ\033[0m')

        # circular error of XZ
        if self.Plot.CircleErr_XZ == True:
            try:
                Center1 = (max(self.Data['SetPos_X']) + min(self.Data['SetPos_X'])) / 2
                Center2 = (max(self.Data['SetPos_Z']) + min(self.Data['SetPos_Z'])) / 2
                R_MaxErr = 0.05
                R = (max(self.Data['SetPos_X']) - min(self.Data['SetPos_X'])) / 2
                self.PlotCircleError(R, R_MaxErr, Center1, Center2, self.Data['CmdPos_X'], self.Data['CmdPos_Z'], self.Data['ActPos_X'], self.Data['ActPos_Z'], F=None, figureName='CircleErr_XZ')
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError CircleErr_XZ\033[0m')

        return None

    ##################################################################################
    # ----------------------------------Plot 1D Data-------------------------------- #
    ##################################################################################
    def Plot1D(self, x, axisName_1=None, dataName=None, shareAxes=None, newFig=True, title=None, mark='.-', tLimit=None, xLimit=None, figureName=''):
        plt.rcParams['font.family'] = 'Microsoft YaHei'
        x = np.array(x)
        if newFig:
            self.FigNum += 1
            print('')
        sys.stdout.write("\033[1;34m\rPlotData: \033[0mDrawning Figure %2d  %s\033[0m" % (self.FigNum, figureName))
        fig = plt.figure(self.FigNum)
        if newFig:
            fig.clf()
        if fig.get_axes() == []:
            ax = fig.add_subplot(1, 1, 1, sharex=shareAxes)
        else:
            ax = fig.get_axes()[0]
        ax.plot(self.Data['Time'], x, mark, label=dataName, alpha=0.7)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel(axisName_1)
        if dataName != None:
            ax.legend(loc="upper right")
        if title != None:
            ax.set_title(title)
        else:
            ax.set_title('1D')
        if tLimit != None:
            plt.xlim(tLimit)
        if xLimit != None:
            plt.ylim(xLimit)
        ax.grid('on')
        plt.ion()
        plt.draw()
        plt.pause(0.001)
        sys.stdout.write("\033[1;34m\rPlotData: \033[1;32mDone \033[0mFigure %2d  %s       \033[0m" % (self.FigNum, figureName))
        plt.ioff()
        return ax

    ##################################################################################
    # ----------------------------------Plot 2D Data-------------------------------- #
    ##################################################################################
    def Plot2D(self, x, y, color=None, axisName_1=None, axisName_2=None, colorName=None, dataName=None, shareAxes=None, newFig=True, title=None, mark='.-', xLimit=None, yLimit=None, figureName=''):
        plt.rcParams['font.family'] = 'Microsoft YaHei'
        try:
            len = min(color.__len__(), x.__len__(), y.__len__())
            color = np.array(color[:len])
            colorFlag = True
        except:
            len = min(x.__len__(), y.__len__())
            colorFlag = False
        x = np.array(x[:len])
        y = np.array(y[:len])
        if newFig:
            self.FigNum += 1
            print('')
        sys.stdout.write("\033[1;34m\rPlotData: \033[0mDrawning Figure %2d  %s\033[0m" % (self.FigNum, figureName))
        fig = plt.figure(self.FigNum)
        if newFig:
            fig.clf()
        if fig.get_axes() == []:
            ax = fig.add_subplot(1, 1, 1, sharex=shareAxes, sharey=shareAxes)
        else:
            ax = fig.get_axes()[0]
        if colorFlag:
            scatter = ax.scatter(x, y, c=color, label=dataName, alpha=0.7, cmap='coolwarm')
            if colorName != None:
                cbar = plt.colorbar(scatter)
                cbar.set_label(colorName)
        else:
            ax.plot(x, y, mark, label=dataName, alpha=0.7)
        ax.set_xlabel(axisName_1)
        ax.set_ylabel(axisName_2)
        if dataName != None:
            ax.legend(loc="upper right")
        if title != None:
            ax.set_title(title)
        else:
            ax.set_title('2D')
        if xLimit != None:
            plt.xlim(xLimit)
        if yLimit != None:
            plt.ylim(yLimit)
        ax.grid('on')
        plt.ion()
        plt.draw()
        plt.pause(0.001)
        sys.stdout.write("\033[1;34m\rPlotData: \033[1;32mDone \033[0mFigure %2d  %s       \033[0m" % (self.FigNum, figureName))
        plt.ioff()
        return ax

    ##################################################################################
    # ----------------------------------Plot 3D Data-------------------------------- #
    ##################################################################################
    def Plot3D(self, x, y, z, color=None, axisName_1=None, axisName_2=None, axisName_3=None, colorName=None, dataName=None, newFig=True, title=None, mark='-', xLimit=None, yLimit=None, zLimit=None, figureName=''):
        plt.rcParams['font.family'] = 'Microsoft YaHei'
        try:
            len = min(color.__len__(), x.__len__(), y.__len__(), z.__len__())
            color = np.array(color[:len])
            colorFlag = True
        except:
            len = min(x.__len__(), y.__len__(), z.__len__())
            colorFlag = False
        x = np.array(x[:len])
        y = np.array(y[:len])
        z = np.array(z[:len])
        if newFig:
            self.FigNum += 1
            print('')
        sys.stdout.write("\033[1;34m\rPlotData: \033[0mDrawning Figure %2d  %s\033[0m" % (self.FigNum, figureName))
        fig = plt.figure(self.FigNum)
        if newFig:
            fig.clf()
            ax = fig.add_subplot(projection='3d')
        ax = fig.gca()
        #ax = fig.gca(projection='3d')
        if colorFlag:
            scatter = ax.scatter3D(x, y, z, c=color, label=dataName, alpha=0.7, cmap='coolwarm')
            if colorName != None:
                cbar = plt.colorbar(scatter)
                cbar.set_label(colorName)
        else:
            ax.plot3D(x, y, z, mark, label=dataName, alpha=0.7)
        ax.set_xlabel(axisName_1)
        ax.set_ylabel(axisName_2)
        ax.set_zlabel(axisName_3)
        if dataName != None:
            ax.legend(loc="upper right")
        if title != None:
            ax.set_title(title)
        else:
            ax.set_title('3D')
        if xLimit != None:
            plt.xlim(xLimit)
        if yLimit != None:
            plt.ylim(yLimit)
        if zLimit != None:
            plt.zlim(zLimit)
        ax.grid('on')
        plt.ion()
        plt.draw()
        plt.pause(0.001)
        sys.stdout.write("\033[1;34m\rPlotData: \033[1;32mDone \033[0mFigure %2d  %s       \033[0m" % (self.FigNum, figureName))
        plt.ioff()
        return None

    ##################################################################################
    # -------------------------------Plot Circle Error------------------------------ #
    ##################################################################################
    def PlotCircleError(self, R, R_MaxErr, Center1, Center2, CmdPos1_mm, CmdPos2_mm, ActPos1_mm, ActPos2_mm, F=None, title=None, figureName=''):
        R_Display = 2 * R_MaxErr
        R_DisplayStep = R_MaxErr / 3
        Len = CmdPos1_mm.__len__()
        
        Theta_Set = np.linspace(0, 2 * np.pi, Len)
        R_SetErr = np.zeros(Len)

        Theta_Cmd = np.arctan2(CmdPos2_mm - Center2, CmdPos1_mm - Center1)
        R_Cmd = np.sqrt(np.multiply(CmdPos1_mm - Center1, CmdPos1_mm - Center1) + np.multiply(CmdPos2_mm - Center2, CmdPos2_mm - Center2))
        R_CmdErr = R_Cmd - R
        R_CmdErr_NoNeg = R_CmdErr;
        R_CmdErr_NoNeg[R_CmdErr_NoNeg < -R_Display] = -R_Display

        Theta_Act = np.arctan2(ActPos2_mm - Center2, ActPos1_mm - Center1)
        R_Act = np.sqrt(np.multiply(ActPos1_mm - Center1, ActPos1_mm - Center1) + np.multiply(ActPos2_mm - Center2, ActPos2_mm - Center2))
        R_ActErr = R_Act - R
        R_ActErr_NoNeg = R_ActErr;
        R_ActErr_NoNeg[R_ActErr_NoNeg < -R_Display] = -R_Display

        if title == None:
            if F == None:
                title = 'Circle Error(um)\n(R=%.3fmm)' % (R)
            else:
                Acc = F * F / 3.6 / R # um/s^2
                title = 'Circle Error(um)\n(R=%.3fmm, F=%dmm/min, Acc=%dum/s^2)' % (R, F, Acc)
        
        Thtea = np.array([Theta_Set, Theta_Cmd, Theta_Act]).T
        Radius = np.array([R_SetErr, R_CmdErr_NoNeg, R_ActErr_NoNeg]).T + R_Display
        dataNmae1 = 'SetPos(R=%.3fmm,Err=0um)' % (R)
        dataName2 = 'CmdPos(R=%.3fmm,Err=%.3fum)' % (np.mean(R_Cmd), np.mean(R_CmdErr) * 1e3)
        dataName3 = 'ActPos(R=%.3fmm,Err=%.3fum)' % (np.mean(R_Act), np.mean(R_ActErr) * 1e3)
        dataName = [dataNmae1, dataName2, dataName3]
        
        self.PlotPolar(Thtea, Radius, title=title, dataName=dataName, newFig=True, figureName=figureName)
        plt.yticks(np.array(range(int((R_Display - R_MaxErr) * 1000), int((R_Display + R_MaxErr) * 1000), int(R_DisplayStep * 1000))) / 1000, np.array(range(int(-R_MaxErr * 1000), int(R_MaxErr * 1000), int(R_DisplayStep * 1000))))
        
        return None

    ##################################################################################
    # --------------------------------Plot Polar Data------------------------------- #
    ##################################################################################
    def PlotPolar(self, Theta, Radius, title=None, dataName=None, mark='-', newFig=True, figureName=''):
        plt.rcParams['font.family'] = 'Microsoft YaHei'
        #len = min(Theta.__len__(), Radius.__len__())
        #Theta = np.array(Theta[:len])
        #Radius = np.array(Radius[:len])
        if newFig:
            self.FigNum += 1
            print('')
        sys.stdout.write("\033[1;34m\rPlotData: \033[0mDrawning Figure %2d  %s\033[0m" % (self.FigNum, figureName))
        fig = plt.figure(self.FigNum)
        if newFig:
            fig.clf()
            #fig.add_subplot(111, projection='polar')
        plt.polar(Theta, Radius, mark, alpha=0.5)
        if title != None:
            plt.title(title)
        if dataName != None:
            plt.legend(dataName, loc="upper right")
        plt.grid('on')
        plt.ion()
        plt.draw()
        plt.pause(0.001)
        sys.stdout.write("\033[1;34m\rPlotData: \033[1;32mDone \033[0mFigure %2d  %s       \033[0m" % (self.FigNum, figureName))
        plt.ioff()
        return None

    ##################################################################################
    # -----------------------------Split Data from Str------------------------------ #
    ##################################################################################
    def SplitDataStr(self, str):
        # elementList = re.split("[\t\n ]", str)
        elementList = self.reSplit.split(str)
        data = []
        for element in elementList:
            # if re.match("[-+0-9\\.]*", element).group():
            if self.reMatch.match(element).group():
                data.append(element)
        return data

    ##################################################################################
    # ---------------------------Read ParamName from Str---------------------------- #
    ##################################################################################
    def ReadParamName(self, str):
        elementList = re.split("[#\t\n ]", str)
        self.ParamName = []
        for element in elementList:
            if re.match("[0-9a-zA-Z\\[\\]]*", element).group():
                self.ParamName.append(element)
        print('\033[1;34m\nParamName in the file:\033[0m')
        for i in range(self.ParamName.__len__()):
            print("%02d : \033[1;33m%s\033[0m" % (i + 1, self.ParamName[i]))
        print('')
        return self.ParamName

    ##################################################################################
    # -----------------------------Load Data from File------------------------------ #
    ##################################################################################
    def LoadData(self):

        # -----------------------open file and get textLen------------------------- #
        with open(self.DataFile, 'r') as f:
            txt = f.readlines()
        textLen = txt.__len__() - 2  # Remove last two lines
        if textLen <= 1:
            print('\033[1;34m\nLoadData: \033[1;31mError (CodeLine %d): textLen =%d <= 1 \033[0m' % (sys._getframe().f_lineno, textLen))
            self.Data = dict()
            return None
        minText = 1
        maxText = textLen
        # -----------------------------get ParamName-------------------------------- #
        self.ParamName = self.ReadParamName(txt[0])
        varNum = self.ParamName.__len__()
        if varNum <= 0:
            print('\033[1;34m\nLoadData: \033[1;31mError (CodeLine %d): varNum = %d  <= 0 \033[0m' % (sys._getframe().f_lineno, varNum))
            self.Data = dict()
            return None
        # -----------------------------get TimeRange-------------------------------- #
        if self.TimeRange.__len__() != 2:
            print('\033[1;34m\nLoadData: \033[1;31mError (CodeLine %d): TimeRange.__len__() = %d != 2 \033[0m' % (sys._getframe().f_lineno, self.TimeRange.__len__()))
            self.Data = dict()
            return None
        else:
            self.TimeRange[0] = float(self.TimeRange[0])
            self.TimeRange[1] = float(self.TimeRange[1])
        self.TimeRange[0] = max(0, self.TimeRange[0])
        self.TimeRange[1] = max(0, self.TimeRange[1])
        if self.TimeRange[1] < self.TimeRange[0]:
            self.TimeRange[1] = 0
        # -----------------------------get BlockRange--------------------------------- #
        if self.BlockRange.__len__() != 2:
            print('\033[1;34m\nLoadData: \033[1;31mError (CodeLine %d): BlockRange.__len__() = %d != 2 \033[0m' % (sys._getframe().f_lineno, self.BlockRange.__len__()))
            self.Data = dict()
            return None
        else:
            self.BlockRange[0] = int(self.BlockRange[0])
            self.BlockRange[1] = int(self.BlockRange[1])
        if  self.BlockRange[1] < self.BlockRange[0]:
            self.BlockRange[1] = 0
            
        # ---------------------------------init Data--------------------------------- #
        for i in range(varNum):
            self.Data[self.ParamName[i]] = []
        BlockNoExistFlag = self.ParamName_BlockNo in self.ParamName
        if BlockNoExistFlag:
            BlockNoIndex = self.ParamName.index(self.ParamName_BlockNo)
        self.Data['Time'] = []
        self.Data['BlockNo'] = []
        # ----------load Data ParamName, varNum, BlockRange and TimeRange------------ #
        self.RemainingLineData = []
        LastBlockNo = 0
        dataStartFlag = False
        dataEndFlag = False
        firstDataFlag = True
        Time = 0.0 # unit: s
        for i in range(minText, maxText):
            self.LoadDataProgressPercentage = (i - minText) / (maxText - minText) * 100
            sys.stdout.write("\033[1;34m\rLoadData: \033[0m%3d%%" % (self.LoadDataProgressPercentage))
            self.LineData = self.SplitDataStr(txt[i])
            while True:
                self.LineData = self.RemainingLineData + self.LineData
                if self.LineData.__len__() < varNum:
                    print('\033[1;34m\nLoadData: \033[1;31mError (File Line %d): LineData.__len__ < varNum (%d < %d) \033[0m' % ( i+1, self.LineData.__len__(), varNum))
                    return None
                if BlockNoExistFlag:
                    if float(self.LineData[BlockNoIndex]) >= 1.23456789e308:
                        self.LineData[BlockNoIndex] = LastBlockNo
                    if dataStartFlag == False and (Time + 1e-10) >= self.TimeRange[0] and float(self.LineData[BlockNoIndex]) >= self.BlockRange[0]:
                        dataStartFlag = True
                    if dataEndFlag == False and (((Time + 1e-10) > self.TimeRange[1] and self.TimeRange[1] > 0) or (float(self.LineData[BlockNoIndex]) > self.BlockRange[1] and self.BlockRange[1] > 0)):
                        dataEndFlag = True
                    if dataStartFlag == True and dataEndFlag == False:
                        for j in range(varNum):
                            self.Data[self.ParamName[j]].append(float(self.LineData[j]))
                        if firstDataFlag:
                            firstDataFlag = False
                            maxBlockNo = minBlockNo = float(self.LineData[BlockNoIndex])
                            minTime = maxTime = float(Time)
                        else:
                            minBlockNo = min(minBlockNo, float(self.LineData[BlockNoIndex]))
                            maxBlockNo = max(maxBlockNo, float(self.LineData[BlockNoIndex]))
                            minTime = min(minTime, Time)
                            maxTime = max(maxTime, Time)
                    LastBlockNo = self.LineData[BlockNoIndex]
                else:
                    if dataStartFlag == False and Time >= self.TimeRange[0]:
                        dataStartFlag = True
                    if dataEndFlag == False and Time > self.TimeRange[1] and self.TimeRange[1] > 0:
                        dataEndFlag = True
                    if dataStartFlag == True and dataEndFlag == False:
                        for j in range(varNum):
                            self.Data[self.ParamName[j]].append(float(self.LineData[j]))
                        if firstDataFlag:
                            firstDataFlag = False
                            minTime = maxTime = float(Time)
                        else:
                            minTime = min(minTime, float(Time))
                            maxTime = min(maxTime, float(Time))
                Time += self.Ts
                self.RemainingLineData = self.LineData[varNum:]
                self.LineData = []
                if self.RemainingLineData.__len__() < varNum:
                    break
        # ---------------------------output Data----------------------------------- #
        for i in range(varNum):
            self.Data[self.ParamName[i]] = np.array(self.Data[self.ParamName[i]])
        self.Data['DataLen'] = self.Data[self.ParamName[0]].__len__()
        if self.Data.__len__() <= 0 or self.Data['DataLen'] <= 0:
            print('\033[1;34m\nLoadData: \033[1;31mError: Data Len = %d! (CodeLine %d) \033[0m' % (self.Data['DataLen'], sys._getframe().f_lineno))
            return None
        if BlockNoExistFlag:
            self.Data['TimeRange']  = [float(minTime), float(maxTime)]
            self.Data['BlockRange'] = [int(minBlockNo), int(maxBlockNo)]
            print('\033[1;34m\rLoadData: \033[1;32m100%%\033[0m\nDataLen=%d, TimeRange=[%.3f, %.3f], BlockRange=[%d, %d] \033[0m' % (self.Data['DataLen'], minTime, maxTime, minBlockNo, maxBlockNo))
        else:
            self.Data['TimeRange']  = [float(minTime), float(maxTime)]
            print('\033[1;34m\rLoadData: \033[1;32m100%%\033[0m\nDataLen=%d, TimeRange=[%.3f, %.3f] \033[0m' % (self.Data['DataLen'], minTime, maxTime))

        # --------------------------------init Data-------------------------------- #
        #Time
        if self.Ts > 0:
            self.Data['Time'] = np.array(range(0, self.Data['DataLen'])) * self.Ts + minTime
            
        #BlockNo
        if self.ParamName_BlockNo in self.ParamName:
            self.Data['BlockNo'] = self.Data[self.ParamName_BlockNo]
            
        # X
        if self.ParamName_SetPos % (self.AxisID_X - 1) in self.ParamName:
            self.Data['SetPos_X'] = np.array(self.Data[self.ParamName_SetPos % (self.AxisID_X - 1)]) * self.Precision_um / 1e3 # mm
            self.Data['SetVel_X'] = np.diff(self.Data['SetPos_X'])/ self.Ts * 60 # mm/min
            data = self.Data['SetVel_X']; data = np.append(data, data[-1])
            self.Data['SetVel_X'] = data
            self.Data['SetAcc_X'] = np.diff(np.diff(self.Data['SetPos_X'])) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data['SetAcc_X']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['SetAcc_X'] = data
            self.Data['SetJerk_X'] = np.diff(np.diff(np.diff(self.Data['SetPos_X']))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data['SetJerk_X']; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['SetJerk_X'] = data
        if self.ParamName_CmdPos % (self.AxisID_X - 1) in self.ParamName:
            self.Data['CmdPos_X'] = np.array(self.Data[self.ParamName_CmdPos % (self.AxisID_X - 1)]) * self.Precision_um / 1e3 # mm
            self.Data['CmdVel_X'] = np.diff(self.Data['CmdPos_X'])/ self.Ts * 60 # mm/min
            data = self.Data['CmdVel_X']; data = np.append(data, data[-1])
            self.Data['CmdVel_X'] = data
            self.Data['CmdAcc_X'] = np.diff(np.diff(self.Data['CmdPos_X'])) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data['CmdAcc_X']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['CmdAcc_X'] = data
            self.Data['CmdJerk_X'] = np.diff(np.diff(np.diff(self.Data['CmdPos_X']))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data['CmdJerk_X']; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['CmdJerk_X'] = data
        if self.ParamName_ActPos % (self.AxisID_X - 1) in self.ParamName:
            self.Data['ActPos_X'] = np.array(self.Data[self.ParamName_ActPos % (self.AxisID_X - 1)]) * self.Precision_um / 1e3 # mm
            self.Data['ActVel_X'] = np.diff(self.Data['ActPos_X'])/ self.Ts * 60 # mm/min
            data = self.Data['ActVel_X']; data = np.append(data, data[-1])
            self.Data['ActVel_X'] = data
            self.Data['ActAcc_X'] = np.diff(np.diff(self.Data['ActPos_X'])) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data['ActAcc_X']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['ActAcc_X'] = data
            self.Data['ActJerk_X'] = np.diff(np.diff(np.diff(self.Data['ActPos_X']))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data['ActJerk_X']; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['ActJerk_X'] = data
            
        # Y
        if self.ParamName_SetPos % (self.AxisID_Y - 1) in self.ParamName:
            self.Data['SetPos_Y'] = np.array(self.Data[self.ParamName_SetPos % (self.AxisID_Y - 1)]) * self.Precision_um / 1e3 # mm
            self.Data['SetVel_Y'] = np.diff(self.Data['SetPos_Y'])/ self.Ts * 60 # mm/min
            data = self.Data['SetVel_Y']; data = np.append(data, data[-1])
            self.Data['SetVel_Y'] = data
            self.Data['SetAcc_Y'] = np.diff(np.diff(self.Data['SetPos_Y'])) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data['SetAcc_Y']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['SetAcc_Y'] = data
            self.Data['SetJerk_Y'] = np.diff(np.diff(np.diff(self.Data['SetPos_Y']))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data['SetJerk_Y']; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['SetJerk_Y'] = data
        if self.ParamName_CmdPos % (self.AxisID_Y - 1) in self.ParamName:
            self.Data['CmdPos_Y'] = np.array(self.Data[self.ParamName_CmdPos % (self.AxisID_Y - 1)]) * self.Precision_um / 1e3 # mm
            self.Data['CmdVel_Y'] = np.diff(self.Data['CmdPos_Y'])/ self.Ts * 60 # mm/min
            data = self.Data['CmdVel_Y']; data = np.append(data, data[-1])
            self.Data['CmdVel_Y'] = data
            self.Data['CmdAcc_Y'] = np.diff(np.diff(self.Data['CmdPos_Y'])) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data['CmdAcc_Y']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['CmdAcc_Y'] = data
            self.Data['CmdJerk_Y'] = np.diff(np.diff(np.diff(self.Data['CmdPos_Y']))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data['CmdJerk_Y']; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['CmdJerk_Y'] = data
        if self.ParamName_ActPos % (self.AxisID_Y - 1) in self.ParamName:
            self.Data['ActPos_Y'] = np.array(self.Data[self.ParamName_ActPos % (self.AxisID_Y - 1)]) * self.Precision_um / 1e3 # mm
            self.Data['ActVel_Y'] = np.diff(self.Data['ActPos_Y'])/ self.Ts * 60 # mm/min
            data = self.Data['ActVel_Y']; data = np.append(data, data[-1])
            self.Data['ActVel_Y'] = data
            self.Data['ActAcc_Y'] = np.diff(np.diff(self.Data['ActPos_Y'])) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data['ActAcc_Y']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['ActAcc_Y'] = data
            self.Data['ActJerk_Y'] = np.diff(np.diff(np.diff(self.Data['ActPos_Y']))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data['ActJerk_Y']; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['ActJerk_Y'] = data
            
        # Z
        if self.ParamName_SetPos % (self.AxisID_Z - 1) in self.ParamName:
            self.Data['SetPos_Z'] = np.array(self.Data[self.ParamName_SetPos % (self.AxisID_Z - 1)]) * self.Precision_um / 1e3 # mm
            self.Data['SetVel_Z'] = np.diff(self.Data['SetPos_Z'])/ self.Ts * 60 # mm/min
            data = self.Data['SetVel_Z']; data = np.append(data, data[-1])
            self.Data['SetVel_Z'] = data
            self.Data['SetAcc_Z'] = np.diff(np.diff(self.Data['SetPos_Z'])) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data['SetAcc_Z']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['SetAcc_Z'] = data
            self.Data['SetJerk_Z'] = np.diff(np.diff(np.diff(self.Data['SetPos_Z']))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data['SetJerk_Z']; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['SetJerk_Z'] = data
        if self.ParamName_CmdPos % (self.AxisID_Z - 1) in self.ParamName:
            self.Data['CmdPos_Z'] = np.array(self.Data[self.ParamName_CmdPos % (self.AxisID_Z - 1)]) * self.Precision_um / 1e3 # mm
            self.Data['CmdVel_Z'] = np.diff(self.Data['CmdPos_Z'])/ self.Ts * 60 # mm/min
            data = self.Data['CmdVel_Z']; data = np.append(data, data[-1])
            self.Data['CmdVel_Z'] = data
            self.Data['CmdAcc_Z'] = np.diff(np.diff(self.Data['CmdPos_Z'])) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data['CmdAcc_Z']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['CmdAcc_Z'] = data
            self.Data['CmdJerk_Z'] = np.diff(np.diff(np.diff(self.Data['CmdPos_Z']))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data['CmdJerk_Z']; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['CmdJerk_Z'] = data
        if self.ParamName_ActPos % (self.AxisID_Z - 1) in self.ParamName:
            self.Data['ActPos_Z'] = np.array(self.Data[self.ParamName_ActPos % (self.AxisID_Z - 1)]) * self.Precision_um / 1e3 # mm
            self.Data['ActVel_Z'] = np.diff(self.Data['ActPos_Z'])/ self.Ts * 60 # mm/min
            data = self.Data['ActVel_Z']; data = np.append(data, data[-1])
            self.Data['ActVel_Z'] = data
            self.Data['ActAcc_Z'] = np.diff(np.diff(self.Data['ActPos_Z'])) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data['ActAcc_Z']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['ActAcc_Z'] = data
            self.Data['ActJerk_Z'] = np.diff(np.diff(np.diff(self.Data['ActPos_Z']))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data['ActJerk_Z']; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['ActJerk_Z'] = data
            
        # A
        if self.ParamName_SetPos % (self.AxisID_A - 1) in self.ParamName:
            self.Data['SetPos_A'] = np.array(self.Data[self.ParamName_SetPos % (self.AxisID_A - 1)]) * self.Precision_um / 1e3 # mm
            self.Data['SetVel_A'] = np.diff(self.Data['SetPos_A'])/ self.Ts * 60 # mm/min
            data = self.Data['SetVel_A']; data = np.append(data, data[-1])
            self.Data['SetVel_A'] = data
            self.Data['SetAcc_A'] = np.diff(np.diff(self.Data['SetPos_A'])) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data['SetAcc_A']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['SetAcc_A'] = data
            self.Data['SetJerk_A'] = np.diff(np.diff(np.diff(self.Data['SetPos_A']))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data['SetJerk_A']; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['SetJerk_A'] = data
        if self.ParamName_CmdPos % (self.AxisID_A - 1) in self.ParamName:
            self.Data['CmdPos_A'] = np.array(self.Data[self.ParamName_CmdPos % (self.AxisID_A - 1)]) * self.Precision_um / 1e3 # mm
            self.Data['CmdVel_A'] = np.diff(self.Data['CmdPos_A'])/ self.Ts * 60 # mm/min
            data = self.Data['CmdVel_A']; data = np.append(data, data[-1])
            self.Data['CmdVel_A'] = data
            self.Data['CmdAcc_A'] = np.diff(np.diff(self.Data['CmdPos_A'])) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data['CmdAcc_A']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['CmdAcc_A'] = data
            self.Data['CmdJerk_A'] = np.diff(np.diff(np.diff(self.Data['CmdPos_A']))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data['CmdJerk_A']; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['CmdJerk_A'] = data
        if self.ParamName_ActPos % (self.AxisID_A - 1) in self.ParamName:
            self.Data['ActPos_A'] = np.array(self.Data[self.ParamName_ActPos % (self.AxisID_A - 1)]) * self.Precision_um / 1e3 # mm
            self.Data['ActVel_A'] = np.diff(self.Data['ActPos_A'])/ self.Ts * 60 # mm/min
            data = self.Data['ActVel_A']; data = np.append(data, data[-1])
            self.Data['ActVel_A'] = data
            self.Data['ActAcc_A'] = np.diff(np.diff(self.Data['ActPos_A'])) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data['ActAcc_A']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['ActAcc_A'] = data
            self.Data['ActJerk_A'] = np.diff(np.diff(np.diff(self.Data['ActPos_A']))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data['ActJerk_A']; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['ActJerk_A'] = data
            
        #PathVel
        if self.ParamName_SetPathVel in self.ParamName:
            self.Data['SetPathVel'] = np.array(self.Data[self.ParamName_SetPathVel]) * self.Precision_um /1e3 / self.Ts * 60 # mm/min
            self.Data['SetPathAcc'] = np.diff(self.Data['SetPathVel'] / 1e3 / 60) / self.Ts # m/s^2
            self.Data['SetPathJerk'] = np.diff(self.Data['SetPathAcc']) / self.Ts # m/s^3
            data = self.Data['SetPathAcc']; data = np.append(data, data[-1])
            self.Data['SetPathAcc'] = data
            data = self.Data['SetPathJerk']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['SetPathJerk'] = data
        if self.ParamName_CmdPathVel in self.ParamName:
            self.Data['CmdPathVel'] = np.array(self.Data[self.ParamName_CmdPathVel]) * self.Precision_um /1e3 / self.Ts * 60 # mm/min
            self.Data['CmdPathAcc'] = np.diff(self.Data['CmdPathVel'] / 1e3 / 60) / self.Ts # m/s^2
            self.Data['CmdPathJerk'] = np.diff(self.Data['CmdPathAcc']) / self.Ts # m/s^3
            data = self.Data['CmdPathAcc']; data = np.append(data, data[-1])
            self.Data['CmdPathAcc'] = data
            data = self.Data['CmdPathJerk']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['CmdPathJerk'] = data
        data = 0;
        if self.ParamName_SetPos % (self.AxisID_X - 1) in self.ParamName:
            data += self.Data['ActVel_X'] ** 2
        if self.ParamName_SetPos % (self.AxisID_Y - 1) in self.ParamName:
            data += self.Data['ActVel_Y'] ** 2
        if self.ParamName_SetPos % (self.AxisID_Z - 1) in self.ParamName:
            data += self.Data['ActVel_Z'] ** 2
        try:
            self.Data['ActPathVel'] = np.sqrt(data) # mm/min
        except:
            self.Data['ActPathVel'] = []
        if self.Data['ActPathVel'].__len__() != 0:
            self.Data['ActPathAcc'] = np.diff(self.Data['ActPathVel']) / 1e3 / 60 / self.Ts # m/s^2
            self.Data['ActPathJerk'] = np.diff(self.Data['ActPathAcc']) / self.Ts # m/s^3
            data = self.Data['ActPathAcc']; data = np.append(data, data[-1])
            self.Data['ActPathAcc'] = data
            data = self.Data['ActPathJerk']; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data['ActPathJerk'] = data
        else:
            self.Data['ActPathAcc'] = []
            self.Data['ActPathJerk'] = []
            
        #PosErr
        data = 0
        if self.ParamName_CmdPos % (self.AxisID_X - 1) in self.ParamName and self.ParamName_ActPos % (self.AxisID_X - 1) in self.ParamName:
                data += (self.Data['CmdPos_X'] - self.Data['ActPos_X']) ** 2
        if self.ParamName_CmdPos % (self.AxisID_Y - 1) in self.ParamName and self.ParamName_ActPos % (self.AxisID_Y - 1) in self.ParamName:
                data += (self.Data['CmdPos_Y'] - self.Data['ActPos_Y']) ** 2
        if self.ParamName_CmdPos % (self.AxisID_Z - 1) in self.ParamName and self.ParamName_ActPos % (self.AxisID_Z - 1) in self.ParamName:
                data += (self.Data['CmdPos_Z'] - self.Data['ActPos_Z']) ** 2
        try:
            self.Data['PosErr'] = np.sqrt(data) # mm/min
        except:
            self.Data['PosErr'] = []
        
        return None
    
    def ShowFigure(self):
        plt.show()
        
    def DataInfo(self, *DataInfo, infoName = []):
        if self.Data['DataLen'] == 0:
            return None
        figs = [plt.figure(Num) for Num in range(1, self.FigNum + 1)]
        axes = [ax for fig in figs for ax in fig.axes]
        lines = [line for ax in axes for line in ax.lines]
        lines2D = list(filter(lambda line: type(line) == matplotlib.lines.Line2D, lines))
        scatters = [collection for ax in axes for collection in ax.collections]
        scatters2D = list(filter(lambda scatter: type(scatter) == matplotlib.collections.PathCollection, scatters))
        artists = lines2D + scatters2D
        if DataInfo.__len__() == 0:
            datacursor(artists, display='multiple', draggable=True)
            print("\033[1;34m\n\nAddDataInfo: \033[1;32mDone\033[0m")
            return None
        try:
            self.InfoValueList = []
            for info in DataInfo:
                if info.__len__() != self.Data['DataLen']:
                    print('\033[1;34m\n\nAddDataInfo: \033[1;33mWarnning: info.__len__() \033[0m')
                    break
                self.InfoValueList.append(info)
            self.InfoText = []
            for i in range(self.Data['DataLen']):
                text = ''
                for j in range(self.InfoValueList.__len__()):
                    if type(self.InfoValueList[j][i]) == int           or \
                       type(self.InfoValueList[j][i]) == float         or \
                       type(self.InfoValueList[j][i]) == numpy.int32   or \
                       type(self.InfoValueList[j][i]) == numpy.float64 :
                        InfoValue = '%.7g' % self.InfoValueList[j][i]
                    else:
                        InfoValue = str(self.InfoValueList[j][i])
                    if j < infoName.__len__():
                        text += str(infoName[j]) + ': ' + InfoValue
                    else:
                        text += 'Info[' + str(j+1) + ']: ' + InfoValue
                    if j < self.InfoValueList.__len__() - 1:
                        text += '\n'
                self.InfoText.append(str(text))
            datacursor(artists, display='multiple', draggable=True, formatter=lambda **param: self.InfoText[param['ind'][0]])
            print("\033[1;34m\n\nAddDataInfo: \033[1;32mDone\033[0m")
        except:
            print('\033[1;34m\n\nAddDataInfo: \033[1;31mError\033[0m')
            return None

##################################################################################
# --------------------------------Main Function--------------------------------- #
##################################################################################
print(__name__)
if __name__ == '__main__':
    PA = PA_Class()
    
    PA.DataFile = r'D:\汇川\采样数据\20210717_迈盛达\象限痕数据集\F2000D55N620.txt'
    PA.Ts = 0.001
    PA.BlockRange = [620, 630]
    PA.TimeRange = [12.447, 0]
    PA.AxisID_X = 7
    PA.AxisID_Y = 1
    PA.AxisID_Z = 5
    
    PA.LoadData()

    """
    PA.Plot.BlockNo         = True
    PA.Plot.PathVel         = True
    PA.Plot.PathAcc         = True
    PA.Plot.Pos_X           = True
    PA.Plot.Vel_X           = True
    PA.Plot.Acc_X           = True
    PA.Plot.Jerk_X          = True
    PA.Plot.Pos_Y           = True
    PA.Plot.Vel_Y           = True
    PA.Plot.Acc_Y           = True
    PA.Plot.Jerk_Y          = True
    PA.Plot.Pos_Z           = True
    PA.Plot.Vel_Z           = True
    PA.Plot.Acc_Z           = True
    PA.Plot.Jerk_Z          = True
    PA.Plot.XY              = True
    PA.Plot.XY_Time         = True
    PA.Plot.XY_BlockNo      = True
    PA.Plot.XY_PathVel      = True
    PA.Plot.XY_PathAcc      = True
    PA.Plot.XY_PathJerk     = True
    PA.Plot.XY_PosErr       = True
    PA.Plot.YZ              = True
    PA.Plot.YZ_Time         = True
    PA.Plot.YZ_BlockNo      = True
    PA.Plot.YZ_PathVel      = True
    PA.Plot.YZ_PathAcc      = True
    PA.Plot.YZ_PathJerk     = True
    PA.Plot.YZ_PosErr       = True
    PA.Plot.XZ              = True
    PA.Plot.XZ_Time         = True
    PA.Plot.XZ_BlockNo      = True
    PA.Plot.XZ_PathVel      = True
    PA.Plot.XZ_PathAcc      = True
    PA.Plot.XZ_PathJerk     = True
    PA.Plot.XZ_PosErr       = True
    PA.Plot.XYZ             = True
    PA.Plot.XYZ_Time        = True
    PA.Plot.XYZ_Z           = True
    PA.Plot.XYZ_PathVel     = True
    PA.Plot.XYZ_PathAcc     = True
    PA.Plot.XYZ_PathJerk    = True
    PA.Plot.CircleErr_XY    = True
    PA.Plot.CircleErr_YZ    = True
    PA.Plot.CircleErr_XZ    = True
    """
    
    PA.Plot.PathVel         = True
    PA.Plot.PathAcc         = True
    PA.Plot.Pos_X           = True
    PA.Plot.Vel_X           = True
    PA.Plot.Acc_X           = True
    PA.Plot.XY              = True
    PA.Plot.XY_Time         = True
    PA.Plot.CircleErr_XY    = True
    PA.Plot.XYZ             = True
    PA.Plot.XYZ_Time        = True
    
    PA.PlotData()
    PA.DataInfo(PA.Data['Time'], PA.Data['BlockNo'], infoName=['Time(s)', 'BlockNo'])
    PA.ShowFigure()
    
    