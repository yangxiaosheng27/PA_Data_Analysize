#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
@File           PaDataAnalyze.py
@Brief          PA data analyze
@Unit of File
                SSetPos                         Unit: internal increment
                CommandedMachinePosCorr         Unit: internal increment
                SActMachinePos                  Unit: internal increment
                PathVelocity                    Unit: internal increment / Ts
                CommandedPathVelocity           Unit: internal increment / Ts
                (The internal increment defaults to 1um, Ts defaults to 0.001s)
@Unit of Data
                PA.Data.SetPathVel              Unit: mm/min
                PA.Data.CmdPathVel              Unit: mm/min
                PA.Data.SetPathAcc              Unit: m/s^2
                PA.Data.CmdPathAcc              Unit: m/s^2
                PA.Data.SetPathJerk             Unit: m/s^3
                PA.Data.CmdPathJerk             Unit: m/s^3
                PA.Data.SetPos_X                Unit: mm
                PA.Data.CmdPos_X                Unit: mm
                PA.Data.ActPos_X                Unit: mm
                PA.Data.SetVel_X                Unit: mm/min
                PA.Data.CmdVel_X                Unit: mm/min
                PA.Data.ActVel_X                Unit: mm/min
                PA.Data.SetAcc_X                Unit: m/s^2
                PA.Data.CmdAcc_X                Unit: m/s^2
                PA.Data.ActAcc_X                Unit: m/s^2
                PA.Data.SetJerk_X               Unit: m/s^3
                PA.Data.CmdJerk_X               Unit: m/s^3
                PA.Data.ActJerk_X               Unit: m/s^3
@Plot Flag
                PA.Plot.BlockNo                 = True
                PA.Plot.PathVel                 = True
                PA.Plot.PathAcc                 = True
                PA.Plot.PathJerk                = True
                PA.Plot.Pos_X                   = True
                PA.Plot.Vel_X                   = True
                PA.Plot.Acc_X                   = True
                PA.Plot.Jerk_X                  = True
                PA.Plot.Pos_Y                   = True
                PA.Plot.Vel_Y                   = True
                PA.Plot.Acc_Y                   = True
                PA.Plot.Jerk_Y                  = True
                PA.Plot.Pos_Z                   = True
                PA.Plot.Vel_Z                   = True
                PA.Plot.Acc_Z                   = True
                PA.Plot.Jerk_Z                  = True
                PA.Plot.XY                      = True
                PA.Plot.XY_Time                 = True
                PA.Plot.XY_BlockNo              = True
                PA.Plot.XY_PathVel              = True
                PA.Plot.XY_PathAcc              = True
                PA.Plot.XY_PathJerk             = True
                PA.Plot.XY_PosErr               = True
                PA.Plot.XY_Z                    = True
                PA.Plot.YZ                      = True
                PA.Plot.YZ_Time                 = True
                PA.Plot.YZ_BlockNo              = True
                PA.Plot.YZ_PathVel              = True
                PA.Plot.YZ_PathAcc              = True
                PA.Plot.YZ_PathJerk             = True
                PA.Plot.YZ_PosErr               = True
                PA.Plot.YZ_X                    = True
                PA.Plot.XZ                      = True
                PA.Plot.XZ_Time                 = True
                PA.Plot.XZ_BlockNo              = True
                PA.Plot.XZ_PathVel              = True
                PA.Plot.XZ_PathAcc              = True
                PA.Plot.XZ_PathJerk             = True
                PA.Plot.XZ_PosErr               = True
                PA.Plot.XZ_Y                    = True
                PA.Plot.XYZ                     = True
                PA.Plot.XYZ_Time                = True
                PA.Plot.XYZ_Z                   = True
                PA.Plot.XYZ_PathVel             = True
                PA.Plot.XYZ_PathAcc             = True
                PA.Plot.XYZ_PathJerk            = True
                PA.Plot.CircleErr_XY            = True
                PA.Plot.CircleErr_YZ            = True
                PA.Plot.CircleErr_XZ            = True
"""

Version = '1.6.0'
################################ Version History ##################################
# ---------------------------------Version 1.6.0--------------------------------- #
# Date: 2021/9/12
# Author: yangxiaosheng
# Update: add user code in GUI
# ---------------------------------Version 1.5.2--------------------------------- #
# Date: 2021/9/11
# Author: yangxiaosheng
# Update: add output message in GUI
# ---------------------------------Version 1.5.1--------------------------------- #
# Date: 2021/9/9
# Author: yangxiaosheng
# Update: fix some bug in using Tkinter
# ---------------------------------Version 1.5.0--------------------------------- #
# Date: 2021/9/7
# Author: yangxiaosheng
# Update: make a GUI using Tkinter
# ---------------------------------Version 1.4.4--------------------------------- #
# Date: 2021/8/30
# Author: yangxiaosheng
# Update: fix some bug in TimeRange checking
# ---------------------------------Version 1.4.3--------------------------------- #
# Date: 2021/8/28
# Author: yangxiaosheng
# Update: fix some bug in using mpldatacursor
# ---------------------------------Version 1.4.2--------------------------------- #
# Date: 2021/8/22
# Author: yangxiaosheng
# Update: add mpldatacursor
# ---------------------------------Version 1.4.1--------------------------------- #
# Date: 2021/8/17
# Author: yangxiaosheng
# Update: fix some bug in plotting figure
# ---------------------------------Version 1.4.0--------------------------------- #
# Date: 2021/8/15
# Author: yangxiaosheng
# Update: Refactor code to improve portability, and remove GUI (using matplotlib) because of bad smooth running
# ---------------------------------Version 1.3.0--------------------------------- #
# Date: 2021/7/20
# Author: yangxiaosheng
# Update: make a GUI using matplotlib
# ---------------------------------Version 1.2.2--------------------------------- #
# Date: 2021/7/1
# Author: yangxiaosheng
# Update: Plot the polar data of a circular trajectory
# ---------------------------------Version 1.2.1--------------------------------- #
# Date: 2021/6/30
# Author: yangxiaosheng
# Update: Add Axis Idenx
# ---------------------------------Version 1.2.0--------------------------------- #
# Date: 2021/5/21
# Author: yangxiaosheng
# Update: Add widgets: Select NC Block
# ---------------------------------Version 1.1.2--------------------------------- #
# Date: 2021/5/21
# Author: yangxiaosheng
# Update: Add TimeRange and BlockRange
# ---------------------------------Version 1.1.1--------------------------------- #
# Date: 2021/5/20
# Author: yangxiaosheng
# Update: Add shared axes, add color bar, and optimize color drawing
# ---------------------------------Version 1.1.0--------------------------------- #
# Date: 2021/5/19
# Author: yangxiaosheng
# Update: Optimize loading speed, and increase loading progress and draw progress
# ---------------------------------Version 1.0.0--------------------------------- #
# Date: 2021/5/18
# Author: yangxiaosheng
# Update: Init Version
##################################################################################

from matplotlib import pyplot as plt
import numpy as np
import matplotlib
import numpy
import time
import sys
import re

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext

class PA_Data_Analyze:
    def __init__(self):
        self.initParam()
    
    def initParam(self):
        ##################################################################################
        # ----------------------------------User Define--------------------------------- #
        ##################################################################################
        self.Precision_um   = 1; # 1 internal incremental = Precision_um * 1um
        self.Ts             = 0.001  # sample time, unit: s
        self.DataFileName   = r'C:\PACnc\CNCVariableTrace.txt'
        self.TimeRange      = [0, 0] # select the sample data in Time range of [minTime, maxTime] (unit: s) ([0, 0] means select all Time)
        self.BlockRange     = [0, 0] # select the sample data in NC Block range of [minBlockNo, maxBlockNo] ([0, 0] means select all NC Block)
        self.Plot           = self.PlotFlag_Class()
        self.AxisID_X       = 0  # 0 means no axis,1 means the first axis
        self.AxisID_Y       = 0  # 0 means no axis,1 means the first axis
        self.AxisID_Z       = 0  # 0 means no axis,1 means the first axis
        self.AxisID_A       = 0  # 0 means no axis,1 means the first axis
        self.AxisID_B       = 0  # 0 means no axis,1 means the first axis

        ##################################################################################
        # -------------------------------Internal Param--------------------------------- #
        ##################################################################################
        self.FigNum                 = 0
        self.GuiText                = None
        self.DataInfoExist          = False
        self.Data                   = self.Data_Class()
        self.ShareAxes              = self.ShareAxes_Class()
        self.reSplit                = re.compile("[\t\n ]")
        self.reMatch                = re.compile("[-+0-9\\.]*")
        self.DataName_SetPos        = 'SSetPos[%d]'
        self.DataName_CmdPos        = 'CommandedMachinePosCorr[%d]'
        self.DataName_ActPos        = 'SActMachinePos[%d]'
        self.DataName_SetPathVel    = 'PathVelocity[0]'
        self.DataName_CmdPathVel    = 'CommandedPathVelocity[0]'
        self.DataName_BlockNo       = 'BlockNoActive[0]'

    class Data_Class:
        Var     = dict()
        Length  = 0

    class ShareAxes_Class:
        Time    = None
        XY      = None
        YZ      = None
        XZ      = None

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
        Pos_B           = False
        Vel_B           = False
        Acc_B           = False
        Jerk_B          = False
        XY              = False
        XY_Time         = False
        XY_BlockNo      = False
        XY_PathVel      = False
        XY_PathAcc      = False
        XY_PathJerk     = False
        XY_PosErr       = False
        XY_Z            = False
        YZ              = False
        YZ_Time         = False
        YZ_BlockNo      = False
        YZ_PathVel      = False
        YZ_PathAcc      = False
        YZ_PathJerk     = False
        YZ_PosErr       = False
        YZ_X            = False
        XZ              = False
        XZ_Time         = False
        XZ_BlockNo      = False
        XZ_PathVel      = False
        XZ_PathAcc      = False
        XZ_PathJerk     = False
        XZ_PosErr       = False
        XZ_Y            = False
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
        
        print('[%s]\n\033[1;34m\n\nPlotData: \033[0mStarting......' % time.strftime('%Y-%m-%d %H:%M:%S'))
        self.OutputMessageToGUI('\n\n[%s]\nPlotData: Starting......' % time.strftime('%Y-%m-%d %H:%M:%S'))
        
        if self.Data.Length == 0:
            print('\033[1;34m\nPlotData: \033[1;31mError No Data\033[0m')
            self.OutputMessageToGUI('\nPlotData: Error No Data')
            return None

        plt.close(fig='all')
        self.FigNum         = 0
        self.ShareAxes.Time = None
        self.ShareAxes.XY   = None
        self.ShareAxes.YZ   = None
        self.ShareAxes.XZ   = None
        self.DataInfoExist  = False
            
        # ---------------------------------Plot 1D---------------------------------- #
        # BlockNo
        if self.Plot.BlockNo == True:
            try:
                block = self.Data.BlockNo
                self.Plot1D(block, dataName='BlockNo', figureName='BlockNo', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError BlockNo\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error BlockNo')

        # PathVel
        if self.Plot.PathVel == True:
            try:
                self.Plot1D(self.Data.SetPathVel, axisName_1='Vel (mm/min)', dataName='SetPathVel', shareAxes=self.ShareAxes.Time, figureName='PathVel', newFigure=True)
                self.Plot1D(self.Data.CmdPathVel, axisName_1='Vel (mm/min)', dataName='CmdPathVel', shareAxes=self.ShareAxes.Time, figureName='PathVel', newFigure=False)
                if self.Data.ActPathVel.__len__() != 0:
                    self.Plot1D(self.Data.ActPathVel, axisName_1='Vel (mm/min)', dataName='ActPathVel', shareAxes=self.ShareAxes.Time, figureName='PathVel', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError PathVel\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error PathVel')

        # PathAcc
        if self.Plot.PathAcc == True:
            try:
                self.Plot1D(self.Data.SetPathAcc, axisName_1='Acc (m/s^2)', dataName='SetPathAcc', shareAxes=self.ShareAxes.Time, figureName='PathAcc', newFigure=True)
                self.Plot1D(self.Data.CmdPathAcc, axisName_1='Acc (m/s^2)', dataName='CmdPathAcc', shareAxes=self.ShareAxes.Time, figureName='PathAcc', newFigure=False)
                #if self.Data.ActPathAcc.__len__() != 0:
                    #self.Plot1D(self.Data.ActPathAcc, axisName_1='Acc (m/s^2)', dataName='ActPathAcc', shareAxes=self.ShareAxes.Time, figureName='PathAcc', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError PathAcc\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error PathAcc')

        # PathJerk
        if self.Plot.PathJerk == True:
            try:
                self.Plot1D(self.Data.SetPathJerk, axisName_1='Jerk (m/s^3)', dataName='SetPathJerk', shareAxes=self.ShareAxes.Time, figureName='PathJerk', newFigure=True)
                self.Plot1D(self.Data.CmdPathJerk, axisName_1='Jerk (m/s^3)', dataName='CmdPathJerk', shareAxes=self.ShareAxes.Time, figureName='PathJerk', newFigure=False)
                #if self.Data.ActPathJerk.__len__() != 0:
                    #self.Plot1D(self.Data.ActPathJerk, axisName_1='Jerk (m/s^3)', dataName='ActPathJerk', shareAxes=self.ShareAxes.Time, figureName='PathJerk', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError PathJerk\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error PathJerk')

        # X
        # Pos_X
        if self.Plot.Pos_X == True:
            try:
                self.Plot1D(self.Data.SetPos_X, axisName_1='Pos (mm)', dataName='SetPos_X', shareAxes=self.ShareAxes.Time, figureName='Pos_X', newFigure=True)
                self.Plot1D(self.Data.CmdPos_X, axisName_1='Pos (mm)', dataName='CmdPos_X', shareAxes=self.ShareAxes.Time, figureName='Pos_X', newFigure=False)
                self.Plot1D(self.Data.ActPos_X, axisName_1='Pos (mm)', dataName='ActPos_X', shareAxes=self.ShareAxes.Time, figureName='Pos_X', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Pos_X\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Pos_X')
        # Vel_X
        if self.Plot.Vel_X == True:
            try:
                self.Plot1D(self.Data.SetVel_X, axisName_1='Vel (mm/min)', dataName='SetVel_X', shareAxes=self.ShareAxes.Time, figureName='Vel_X', newFigure=True)
                self.Plot1D(self.Data.CmdVel_X, axisName_1='Vel (mm/min)', dataName='CmdVel_X', shareAxes=self.ShareAxes.Time, figureName='Vel_X', newFigure=False)
                self.Plot1D(self.Data.ActVel_X, axisName_1='Vel (mm/min)', dataName='ActVel_X', shareAxes=self.ShareAxes.Time, figureName='Vel_X', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Vel_X\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Vel_X')
        # Acc_X
        if self.Plot.Acc_X == True:
            try:
                self.Plot1D(self.Data.SetAcc_X, axisName_1='Acc (m/s^2)', dataName='SetAcc_X', shareAxes=self.ShareAxes.Time, figureName='Acc_X', newFigure=True)
                self.Plot1D(self.Data.CmdAcc_X, axisName_1='Acc (m/s^2)', dataName='CmdAcc_X', shareAxes=self.ShareAxes.Time, figureName='Acc_X', newFigure=False)
                self.Plot1D(self.Data.ActAcc_X, axisName_1='Acc (m/s^2)', dataName='ActAcc_X', shareAxes=self.ShareAxes.Time, figureName='Acc_X', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Acc_X\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Acc_X')
        # Jerk_X
        if self.Plot.Jerk_X == True:
            try:
                self.Plot1D(self.Data.SetJerk_X, axisName_1='Jerk (m/s^3)', dataName='SetJerk_X', shareAxes=self.ShareAxes.Time, figureName='Jerk_X', newFigure=True)
                self.Plot1D(self.Data.CmdJerk_X, axisName_1='Jerk (m/s^3)', dataName='CmdJerk_X', shareAxes=self.ShareAxes.Time, figureName='Jerk_X', newFigure=False)
                # self.Plot1D(self.Data.ActJerk_X, axisName_1='Jerk (m/s^3)', dataName='ActJerk_X', shareAxes=self.ShareAxes.Time, figureName='Jerk_X', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Jerk_X\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Jerk_X')

        # Y
        # Pos_Y
        if self.Plot.Pos_Y == True:
            try:
                self.Plot1D(self.Data.SetPos_Y, axisName_1='Pos (mm)', dataName='SetPos_Y', shareAxes=self.ShareAxes.Time, figureName='Pos_Y', newFigure=True)
                self.Plot1D(self.Data.CmdPos_Y, axisName_1='Pos (mm)', dataName='CmdPos_Y', shareAxes=self.ShareAxes.Time, figureName='Pos_Y', newFigure=False)
                self.Plot1D(self.Data.ActPos_Y, axisName_1='Pos (mm)', dataName='ActPos_Y', shareAxes=self.ShareAxes.Time, figureName='Pos_Y', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Pos_Y\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Pos_Y')
        # Vel_Y
        if self.Plot.Vel_Y == True:
            try:
                self.Plot1D(self.Data.SetVel_Y, axisName_1='Vel (mm/min)', dataName='SetVel_Y', shareAxes=self.ShareAxes.Time, figureName='Vel_Y', newFigure=True)
                self.Plot1D(self.Data.CmdVel_Y, axisName_1='Vel (mm/min)', dataName='CmdVel_Y', shareAxes=self.ShareAxes.Time, figureName='Vel_Y', newFigure=False)
                self.Plot1D(self.Data.ActVel_Y, axisName_1='Vel (mm/min)', dataName='ActVel_Y', shareAxes=self.ShareAxes.Time, figureName='Vel_Y', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Vel_Y\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Vel_Y')
        # Acc_Y
        if self.Plot.Acc_Y == True:
            try:
                self.Plot1D(self.Data.SetAcc_Y, axisName_1='Acc (m/s^2)', dataName='SetAcc_Y', shareAxes=self.ShareAxes.Time, figureName='Acc_Y', newFigure=True)
                self.Plot1D(self.Data.CmdAcc_Y, axisName_1='Acc (m/s^2)', dataName='CmdAcc_Y', shareAxes=self.ShareAxes.Time, figureName='Acc_Y', newFigure=False)
                self.Plot1D(self.Data.ActAcc_Y, axisName_1='Acc (m/s^2)', dataName='ActAcc_Y', shareAxes=self.ShareAxes.Time, figureName='Acc_Y', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Acc_Y\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Acc_Y')
        # Jerk_Y
        if self.Plot.Jerk_Y == True:
            try:
                self.Plot1D(self.Data.SetJerk_Y, axisName_1='Jerk (m/s^3)', dataName='SetJerk_Y', shareAxes=self.ShareAxes.Time, figureName='Jerk_Y', newFigure=True)
                self.Plot1D(self.Data.CmdJerk_Y, axisName_1='Jerk (m/s^3)', dataName='CmdJerk_Y', shareAxes=self.ShareAxes.Time, figureName='Jerk_Y', newFigure=False)
                # self.Plot1D(self.Data.ActJerk_Y, axisName_1='Jerk (m/s^3)', dataName='ActJerk_Y', shareAxes=self.ShareAxes.Time, figureName='Jerk_Y', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Jerk_Y\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Jerk_Y')

        # Z
        #Pos_Z
        if self.Plot.Pos_Z == True:
            try:
                self.Plot1D(self.Data.SetPos_Z, axisName_1='Pos (mm)', dataName='SetPos_Z', shareAxes=self.ShareAxes.Time, figureName='Pos_Z', newFigure=True)
                self.Plot1D(self.Data.CmdPos_Z, axisName_1='Pos (mm)', dataName='CmdPos_Z', shareAxes=self.ShareAxes.Time, figureName='Pos_Z', newFigure=False)
                self.Plot1D(self.Data.ActPos_Z, axisName_1='Pos (mm)', dataName='ActPos_Z', shareAxes=self.ShareAxes.Time, figureName='Pos_Z', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Pos_Z\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Pos_Z')
        #Vel_Z
        if self.Plot.Vel_Z == True:
            try:
                self.Plot1D(self.Data.SetVel_Z, axisName_1='Vel (mm/min)', dataName='SetVel_Z', shareAxes=self.ShareAxes.Time, figureName='Vel_Z', newFigure=True)
                self.Plot1D(self.Data.CmdVel_Z, axisName_1='Vel (mm/min)', dataName='CmdVel_Z', shareAxes=self.ShareAxes.Time, figureName='Vel_Z', newFigure=False)
                self.Plot1D(self.Data.ActVel_Z, axisName_1='Vel (mm/min)', dataName='ActVel_Z', shareAxes=self.ShareAxes.Time, figureName='Vel_Z', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Vel_Z\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Vel_Z')
        #Acc_Z
        if self.Plot.Acc_Z == True:
            try:
                self.Plot1D(self.Data.SetAcc_Z, axisName_1='Acc (m/s^2)', dataName='SetAcc_Z', shareAxes=self.ShareAxes.Time, figureName='Acc_Z', newFigure=True)
                self.Plot1D(self.Data.CmdAcc_Z, axisName_1='Acc (m/s^2)', dataName='CmdAcc_Z', shareAxes=self.ShareAxes.Time, figureName='Acc_Z', newFigure=False)
                self.Plot1D(self.Data.ActAcc_Z, axisName_1='Acc (m/s^2)', dataName='ActAcc_Z', shareAxes=self.ShareAxes.Time, figureName='Acc_Z', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Acc_Z\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Acc_Z')
        # Jerk_Z
        if self.Plot.Jerk_Z == True:
            try:
                self.Plot1D(self.Data.SetJerk_Z, axisName_1='Jerk (m/s^3)', dataName='SetJerk_Z', shareAxes=self.ShareAxes.Time, figureName='Jerk_Z', newFigure=True)
                self.Plot1D(self.Data.CmdJerk_Z, axisName_1='Jerk (m/s^3)', dataName='CmdJerk_Z', shareAxes=self.ShareAxes.Time, figureName='Jerk_Z', newFigure=False)
                # self.Plot1D(self.Data.ActJerk_Z, axisName_1='Jerk (m/s^3)', dataName='ActJerk_Z', shareAxes=self.ShareAxes.Time, figureName='Jerk_Z', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Jerk_Z\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Jerk_Z')

        # A
        #Pos_A
        if self.Plot.Pos_A == True:
            try:
                self.Plot1D(self.Data.SetPos_A, axisName_1='Pos (mm)', dataName='SetPos_A', shareAxes=self.ShareAxes.Time, figureName='Pos_A', newFigure=True)
                self.Plot1D(self.Data.CmdPos_A, axisName_1='Pos (mm)', dataName='CmdPos_A', shareAxes=self.ShareAxes.Time, figureName='Pos_A', newFigure=False)
                self.Plot1D(self.Data.ActPos_A, axisName_1='Pos (mm)', dataName='ActPos_A', shareAxes=self.ShareAxes.Time, figureName='Pos_A', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Pos_A\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Pos_A')
        #Vel_A
        if self.Plot.Vel_A == True:
            try:
                self.Plot1D(self.Data.SetVel_A, axisName_1='Vel (mm/min)', dataName='SetVel_A', shareAxes=self.ShareAxes.Time, figureName='Vel_A', newFigure=True)
                self.Plot1D(self.Data.CmdVel_A, axisName_1='Vel (mm/min)', dataName='CmdVel_A', shareAxes=self.ShareAxes.Time, figureName='Vel_A', newFigure=False)
                self.Plot1D(self.Data.ActVel_A, axisName_1='Vel (mm/min)', dataName='ActVel_A', shareAxes=self.ShareAxes.Time, figureName='Vel_A', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Vel_A\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Vel_A')
        #Acc_A
        if self.Plot.Acc_A == True:
            try:
                self.Plot1D(self.Data.SetAcc_A, axisName_1='Acc (m/s^2)', dataName='SetAcc_A', shareAxes=self.ShareAxes.Time, figureName='Acc_A', newFigure=True)
                self.Plot1D(self.Data.CmdAcc_A, axisName_1='Acc (m/s^2)', dataName='CmdAcc_A', shareAxes=self.ShareAxes.Time, figureName='Acc_A', newFigure=False)
                self.Plot1D(self.Data.ActAcc_A, axisName_1='Acc (m/s^2)', dataName='ActAcc_A', shareAxes=self.ShareAxes.Time, figureName='Acc_A', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Acc_A\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Acc_A')
        # Jerk_A
        if self.Plot.Jerk_A == True:
            try:
                self.Plot1D(self.Data.SetJerk_A, axisName_1='Jerk (m/s^3)', dataName='SetJerk_A', shareAxes=self.ShareAxes.Time, figureName='Jerk_A', newFigure=True)
                self.Plot1D(self.Data.CmdJerk_A, axisName_1='Jerk (m/s^3)', dataName='CmdJerk_A', shareAxes=self.ShareAxes.Time, figureName='Jerk_A', newFigure=False)
                # self.Plot1D(self.Data.ActJerk_A, axisName_1='Jerk (m/s^3)', dataName='ActJerk_A', shareAxes=self.ShareAxes.Time, figureName='Jerk_A', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Jerk_A\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Jerk_A')

        # B
        #Pos_B
        if self.Plot.Pos_B == True:
            try:
                self.Plot1D(self.Data.SetPos_B, axisName_1='Pos (mm)', dataName='SetPos_B', shareAxes=self.ShareAxes.Time, figureName='Pos_B', newFigure=True)
                self.Plot1D(self.Data.CmdPos_B, axisName_1='Pos (mm)', dataName='CmdPos_B', shareAxes=self.ShareAxes.Time, figureName='Pos_B', newFigure=False)
                self.Plot1D(self.Data.ActPos_B, axisName_1='Pos (mm)', dataName='ActPos_B', shareAxes=self.ShareAxes.Time, figureName='Pos_B', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Pos_B\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Pos_B')
        #Vel_B
        if self.Plot.Vel_B == True:
            try:
                self.Plot1D(self.Data.SetVel_B, axisName_1='Vel (mm/min)', dataName='SetVel_B', shareAxes=self.ShareAxes.Time, figureName='Vel_B', newFigure=True)
                self.Plot1D(self.Data.CmdVel_B, axisName_1='Vel (mm/min)', dataName='CmdVel_B', shareAxes=self.ShareAxes.Time, figureName='Vel_B', newFigure=False)
                self.Plot1D(self.Data.ActVel_B, axisName_1='Vel (mm/min)', dataName='ActVel_B', shareAxes=self.ShareAxes.Time, figureName='Vel_B', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Vel_B\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Vel_B')
        #Acc_B
        if self.Plot.Acc_B == True:
            try:
                self.Plot1D(self.Data.SetAcc_B, axisName_1='Acc (m/s^2)', dataName='SetAcc_B', shareAxes=self.ShareAxes.Time, figureName='Acc_B', newFigure=True)
                self.Plot1D(self.Data.CmdAcc_B, axisName_1='Acc (m/s^2)', dataName='CmdAcc_B', shareAxes=self.ShareAxes.Time, figureName='Acc_B', newFigure=False)
                self.Plot1D(self.Data.ActAcc_B, axisName_1='Acc (m/s^2)', dataName='ActAcc_B', shareAxes=self.ShareAxes.Time, figureName='Acc_B', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Acc_B\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Acc_B')
        # Jerk_B
        if self.Plot.Jerk_B == True:
            try:
                self.Plot1D(self.Data.SetJerk_B, axisName_1='Jerk (m/s^3)', dataName='SetJerk_B', shareAxes=self.ShareAxes.Time, figureName='Jerk_B', newFigure=True)
                self.Plot1D(self.Data.CmdJerk_B, axisName_1='Jerk (m/s^3)', dataName='CmdJerk_B', shareAxes=self.ShareAxes.Time, figureName='Jerk_B', newFigure=False)
                # self.Plot1D(self.Data.ActJerk_B, axisName_1='Jerk (m/s^3)', dataName='ActJerk_B', shareAxes=self.ShareAxes.Time, figureName='Jerk_B', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError Jerk_B\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error Jerk_B')

        # ---------------------------------Plot 2D---------------------------------- #
        # XY
        if self.Plot.XY == True:
            try:
                self.Plot2D(self.Data.SetPos_X, self.Data.SetPos_Y, axisName_1='X (mm)', axisName_2='Y (mm)', dataName='SetPos', shareAxes=self.ShareAxes.XY, figureName='XY', newFigure=True)
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, axisName_1='X (mm)', axisName_2='Y (mm)', dataName='CmdPos', shareAxes=self.ShareAxes.XY, figureName='XY', newFigure=False)
                self.Plot2D(self.Data.ActPos_X, self.Data.ActPos_Y, axisName_1='X (mm)', axisName_2='Y (mm)', dataName='ActPos', shareAxes=self.ShareAxes.XY, figureName='XY', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XY\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XY')
        # XY with BlockNo
        if self.Plot.XY_BlockNo == True:
            try:
                color = self.Data.BlockNo
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='BlockNo', shareAxes=self.ShareAxes.XY, figureName='XY_BlockNo', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError BlockNo\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error BlockNo')
        # XY with Time
        if self.Plot.XY_Time == True:
            try:
                color = self.Data.Time
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='Time (s)', shareAxes=self.ShareAxes.XY, figureName='XY_Time', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_Time\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XY_Time')
        #XY with PathVel
        if self.Plot.XY_PathVel == True:
            try:
                color = self.Data.CmdPathVel
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='PathVel (mm/min)', shareAxes=self.ShareAxes.XY, figureName='XY_PathVel', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_PathVel\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XY_PathVel')
        #XY with PathAcc
        if self.Plot.XY_PathAcc == True:
            try:
                color = self.Data.CmdPathAcc
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='PathAcc (m/s^2)', shareAxes=self.ShareAxes.XY, figureName='XY_PathAcc', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_PathAcc\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XY_PathAcc')
        #XY with PathJerk
        if self.Plot.XY_PathJerk == True:
            try:
                color = self.Data.CmdPathJerk
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='PathJerk (m/s^3)', shareAxes=self.ShareAxes.XY, figureName='XY_PathJerk', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_PathJerk\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XY_PathJerk')
        #XY with PosErr
        if self.Plot.XY_PosErr == True:
            try:
                if self.Data.PosErr.__len__() != 0:
                    color = self.Data.PosErr
                    self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='PosErr (mm)', shareAxes=self.ShareAxes.XY, figureName='XY_PosErr', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_PosErr\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XY_PosErr')
        #XY with Z
        if self.Plot.XY_Z == True:
            try:
                color = self.Data.CmdPos_Z
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='Z (mm)', shareAxes=self.ShareAxes.XY, figureName='XY_Z', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_Z\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XY_Z')
        
        # YZ
        if self.Plot.YZ == True:
            try:
                self.Plot2D(self.Data.SetPos_Y, self.Data.SetPos_Z, axisName_1='Y (mm)', axisName_2='Z (mm)', dataName='SetPos', shareAxes=self.ShareAxes.YZ, figureName='YZ', newFigure=True)
                self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, axisName_1='Y (mm)', axisName_2='Z (mm)', dataName='CmdPos', shareAxes=self.ShareAxes.YZ, figureName='YZ', newFigure=False)
                self.Plot2D(self.Data.ActPos_Y, self.Data.ActPos_Z, axisName_1='Y (mm)', axisName_2='Z (mm)', dataName='ActPos', shareAxes=self.ShareAxes.YZ, figureName='YZ', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error YZ')
        # YZ with BlockNo
        if self.Plot.YZ_BlockNo == True:
            try:
                color = self.Data.BlockNo
                self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='BlockNo', shareAxes=self.ShareAxes.YZ, figureName='YZ_BlockNo', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_BlockNo\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error YZ_BlockNo')
        # YZ with Time
        if self.Plot.YZ_Time == True:
            try:
                color = self.Data.Time
                self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='Time (s)', shareAxes=self.ShareAxes.YZ, figureName='YZ_Time', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_Time\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error YZ_Time')
        #YZ with PathVel
        if self.Plot.YZ_PathVel == True:
            try:
                color = self.Data.CmdPathVel
                self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='PathVel (mm/min)', shareAxes=self.ShareAxes.YZ, figureName='YZ_PathVel', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_PathVel\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error YZ_PathVel')
        #YZ with PathAcc
        if self.Plot.YZ_PathAcc == True:
            try:
                color = self.Data.CmdPathAcc
                self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='PathAcc (m/s^2)', shareAxes=self.ShareAxes.YZ, figureName='YZ_PathAcc', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_PathAcc\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error YZ_PathAcc')
        #YZ with PathJerk
        if self.Plot.YZ_PathJerk == True:
            try:
                color = self.Data.CmdPathJerk
                self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='PathJerk (m/s^3)', shareAxes=self.ShareAxes.YZ, figureName='YZ_PathJerk', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_PathJerk\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error YZ_PathJerk')
        #YZ with PosErr
        if self.Plot.YZ_PosErr == True:
            try:
                if self.Data.PosErr.__len__() != 0:
                    color = self.Data.PosErr
                    self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='PosErr (mm)', shareAxes=self.ShareAxes.YZ, figureName='YZ_PosErr', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_PosErr\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error YZ_PosErr')
        #YZ with X
        if self.Plot.YZ_X == True:
            try:
                color = self.Data.CmdPos_X
                self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='X (mm)', shareAxes=self.ShareAxes.YZ, figureName='YZ_X', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_X\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error YZ_X')

        # XZ
        if self.Plot.XZ == True:
            try:
                self.Plot2D(self.Data.SetPos_X, self.Data.SetPos_Z, axisName_1='X (mm)', axisName_2='Z (mm)', dataName='SetPos', shareAxes=self.ShareAxes.XZ, figureName='XZ', newFigure=True)
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, axisName_1='X (mm)', axisName_2='Z (mm)', dataName='CmdPos', shareAxes=self.ShareAxes.XZ, figureName='XZ', newFigure=False)
                self.Plot2D(self.Data.ActPos_X, self.Data.ActPos_Z, axisName_1='X (mm)', axisName_2='Z (mm)', dataName='ActPos', shareAxes=self.ShareAxes.XZ, figureName='XZ', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XZ')
        # XZ with BlockNo
        if self.Plot.XZ_BlockNo == True:
            try:
                color = self.Data.BlockNo
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='BlockNo', shareAxes=self.ShareAxes.XZ, figureName='XZ_BlockNo', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_BlockNo\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XZ_BlockNo')
        # XZ with Time
        if self.Plot.XZ_Time == True:
            try:
                color = self.Data.Time
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='Time (s)', shareAxes=self.ShareAxes.XZ, figureName='XZ_Time', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_Time\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XZ_Time')
        #XZ with PathVel
        if self.Plot.XZ_PathVel == True:
            try:
                color = self.Data.CmdPathVel
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='PathVel (mm/min)', shareAxes=self.ShareAxes.XZ, figureName='XZ_PathVel', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_PathVel\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XZ_PathVel')
        #XZ with PathAcc
        if self.Plot.XZ_PathAcc == True:
            try:
                color = self.Data.CmdPathAcc
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='PathAcc (m/s^2)', shareAxes=self.ShareAxes.XZ, figureName='XZ_PathAcc', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_PathAcc\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XZ_PathAcc')
        #XZ with PathJerk
        if self.Plot.XZ_PathJerk == True:
            try:
                color = self.Data.CmdPathJerk
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='PathJerk (m/s^3)', shareAxes=self.ShareAxes.XZ, figureName='XZ_PathJerk', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_PathJerk\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XZ_PathJerk')
        #XZ with PosErr
        if self.Plot.XZ_PosErr == True:
            try:
                if self.Data.PosErr.__len__() != 0:
                    color = self.Data.PosErr
                    self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='PosErr (mm)', shareAxes=self.ShareAxes.XZ, figureName='XZ_PosErr', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_PosErr\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XZ_PosErr')
        #XZ with Y
        if self.Plot.XZ_Y == True:
            try:
                color = self.Data.CmdPos_Y
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='Y (mm)', shareAxes=self.ShareAxes.XZ, figureName='XZ_Y', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_Y\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XZ_Y')

        # ---------------------------------Plot 3D---------------------------------- #
        #XYZ
        if self.Plot.XYZ == True:
            try:
                self.Plot3D(self.Data.SetPos_X, self.Data.SetPos_Y, self.Data.SetPos_Z, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', dataName='SetPos', figureName='XYZ', newFigure=True)
                self.Plot3D(self.Data.CmdPos_X, self.Data.CmdPos_Y, self.Data.CmdPos_Z, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', dataName='CmdPos', figureName='XYZ', newFigure=False)
                self.Plot3D(self.Data.ActPos_X, self.Data.ActPos_Y, self.Data.ActPos_Z, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', dataName='ActPos', figureName='XYZ', newFigure=False)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XYZ')

        #XYZ with Time
        if self.Plot.XYZ_Time == True:
            try:
                color = self.Data.Time
                self.Plot3D(self.Data.ActPos_X, self.Data.ActPos_Y, self.Data.ActPos_Z, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='Time (s)', figureName='XYZ_Time', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_Time\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XYZ_Time')

        #XYZ with Z
        if self.Plot.XYZ_Z == True:
            try:
                color = self.Data.ActPos_Z
                self.Plot3D(self.Data.ActPos_X, self.Data.ActPos_Y, self.Data.ActPos_Z, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='Z (mm)', figureName='XYZ_Z', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_Z\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XYZ_Z')

        #XYZ with CmdPathVel
        if self.Plot.XYZ_PathVel == True:
            try:
                color = self.Data.CmdPathVel
                self.Plot3D(self.Data.ActPos_X, self.Data.ActPos_Y, self.Data.ActPos_Z, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='PathVel (mm/min)', figureName='XYZ_PathVel', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_PathVel\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XYZ_PathVel')

        #XYZ with CmdPathAcc
        if self.Plot.XYZ_PathAcc == True:
            try:
                color = self.Data.CmdPathAcc
                self.Plot3D(self.Data.ActPos_X, self.Data.ActPos_Y, self.Data.ActPos_Z, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='PathAcc (m/s^2)', figureName='XYZ_PathAcc', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_PathAcc\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XYZ_PathAcc')

        #XYZ with CmdPathJerk
        if self.Plot.XYZ_PathJerk == True:
            try:
                color = self.Data.CmdPathJerk
                self.Plot3D(self.Data.ActPos_X, self.Data.ActPos_Y, self.Data.ActPos_Z, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='PathJerk (m/s^3)', figureName='XYZ_PathJerk', newFigure=True)
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_PathJerk\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error XYZ_PathJerk')

        # ----------------------------Plot Circle Error----------------------------- #
        # circular error of XY
        if self.Plot.CircleErr_XY == True:
            try:
                Center1 = (max(self.Data.SetPos_X) + min(self.Data.SetPos_X)) / 2
                Center2 = (max(self.Data.SetPos_Y) + min(self.Data.SetPos_Y)) / 2
                R_MaxErr = 0.05
                R = (max(self.Data.SetPos_X) - min(self.Data.SetPos_X)) / 2
                self.PlotCircleError(R, R_MaxErr, Center1, Center2, self.Data.CmdPos_X, self.Data.CmdPos_Y, self.Data.ActPos_X, self.Data.ActPos_Y, F=None, figureName='CircleErr_XY')
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError CircleErr_XY\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error CircleErr_XY')

        # circular error of YZ
        if self.Plot.CircleErr_YZ == True:
            try:
                Center1 = (max(self.Data.SetPos_Y) + min(self.Data.SetPos_Y)) / 2
                Center2 = (max(self.Data.SetPos_Z) + min(self.Data.SetPos_Z)) / 2
                R_MaxErr = 0.05
                R = (max(self.Data.SetPos_Y) - min(self.Data.SetPos_Y)) / 2
                self.PlotCircleError(R, R_MaxErr, Center1, Center2, self.Data.CmdPos_Y, self.Data.CmdPos_Z, self.Data.ActPos_Y, self.Data.ActPos_Z, F=None, figureName='CircleErr_YZ')
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError CircleErr_YZ\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error CircleErr_YZ')

        # circular error of XZ
        if self.Plot.CircleErr_XZ == True:
            try:
                Center1 = (max(self.Data.SetPos_X) + min(self.Data.SetPos_X)) / 2
                Center2 = (max(self.Data.SetPos_Z) + min(self.Data.SetPos_Z)) / 2
                R_MaxErr = 0.05
                R = (max(self.Data.SetPos_X) - min(self.Data.SetPos_X)) / 2
                self.PlotCircleError(R, R_MaxErr, Center1, Center2, self.Data.CmdPos_X, self.Data.CmdPos_Z, self.Data.ActPos_X, self.Data.ActPos_Z, F=None, figureName='CircleErr_XZ')
            except:
                print('\033[1;34m\nPlotData: \033[1;31mError CircleErr_XZ\033[0m')
                self.OutputMessageToGUI('\nPlotData: Error CircleErr_XZ')

        
        # ---------------------------------end---------------------------------- #
        if self.FigNum == 0:
            print('\033[1;34m\nPlotData: \033[1;31mNo Figure\033[0m')
            self.OutputMessageToGUI('\nPlotData: No Figure')
        return None

    ##################################################################################
    # ----------------------------------Plot 1D Data-------------------------------- #
    ##################################################################################
    def Plot1D(self, x, axisName_1=None, dataName=None, shareAxes=None, newFigure=True, title=None, mark='.-', tLimit=None, xLimit=None, figureName=''):
        plt.rcParams['font.family'] = 'Microsoft YaHei'
        plt.rcParams.update({'figure.max_open_warning': 0})
        x = np.array(x)
        if newFigure:
            self.FigNum += 1
            print('')
            self.OutputMessageToGUI('\n')
        sys.stdout.write("\033[1;34m\rPlotData: \033[0mDrawing Figure %2d  %s\033[0m" % (self.FigNum, figureName))
        self.OutputMessageToGUI('PlotData: Drawing Figure %2d  %s' % (self.FigNum, figureName), overwrite=True)
        fig = plt.figure(self.FigNum)
        if newFigure:
            fig.clf()
        if fig.get_axes() == []:
            ax = fig.add_subplot(1, 1, 1, sharex=shareAxes)
        else:
            ax = fig.get_axes()[0]
        ax.plot(self.Data.Time, x, mark, label=dataName, alpha=0.7)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel(axisName_1)
        if dataName != None:
            ax.legend(loc="upper right")
        if title != None:
            ax.set_title(title)
        elif figureName != '':
            ax.set_title(figureName)
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
        sys.stdout.write("\033[1;34m\rPlotData: \033[1;32mDone    \033[0mFigure %2d  %s       \033[0m" % (self.FigNum, figureName))
        self.OutputMessageToGUI('PlotData: Done    Figure %2d  %s       ' % (self.FigNum, figureName), overwrite=True)
        plt.ioff()
        if shareAxes == self.ShareAxes.Time:
            self.ShareAxes.Time = ax
        return ax

    ##################################################################################
    # ----------------------------------Plot 2D Data-------------------------------- #
    ##################################################################################
    def Plot2D(self, x, y, color=None, axisName_1=None, axisName_2=None, colorName=None, dataName=None, shareAxes=None, newFigure=True, title=None, mark='.-', xLimit=None, yLimit=None, figureName=''):
        plt.rcParams['font.family'] = 'Microsoft YaHei'
        plt.rcParams.update({'figure.max_open_warning': 0})
        try:
            len = min(color.__len__(), x.__len__(), y.__len__())
            color = np.array(color[:len])
            colorFlag = True
        except:
            len = min(x.__len__(), y.__len__())
            colorFlag = False
        x = np.array(x[:len])
        y = np.array(y[:len])
        if newFigure:
            self.FigNum += 1
            print('')
            self.OutputMessageToGUI('\n')
        sys.stdout.write("\033[1;34m\rPlotData: \033[0mDrawing Figure %2d  %s\033[0m" % (self.FigNum, figureName))
        self.OutputMessageToGUI('PlotData: Drawing Figure %2d  %s' % (self.FigNum, figureName), overwrite=True)
        fig = plt.figure(self.FigNum)
        if newFigure:
            fig.clf()
        if fig.get_axes() == []:
            ax = fig.add_subplot(1, 1, 1, sharex=shareAxes, sharey=shareAxes)
        else:
            ax = fig.get_axes()[0]
        if colorFlag:
            scatter = ax.scatter(x, y, c=color, label=dataName, alpha=0.7, cmap='coolwarm')
            cbar = plt.colorbar(scatter)
            if colorName != None:
                cbar.set_label(colorName)
        else:
            ax.plot(x, y, mark, label=dataName, alpha=0.7)
        ax.set_xlabel(axisName_1)
        ax.set_ylabel(axisName_2)
        if dataName != None:
            ax.legend(loc="upper right")
        if title != None:
            ax.set_title(title)
        elif figureName != '':
            ax.set_title(figureName)
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
        sys.stdout.write("\033[1;34m\rPlotData: \033[1;32mDone    \033[0mFigure %2d  %s       \033[0m" % (self.FigNum, figureName))
        self.OutputMessageToGUI('PlotData: Done    Figure %2d  %s       ' % (self.FigNum, figureName), overwrite=True)
        plt.ioff()
        if shareAxes == self.ShareAxes.XY:
            self.ShareAxes.XY = ax
        elif shareAxes == self.ShareAxes.YZ:
            self.ShareAxes.YZ = ax
        elif shareAxes == self.ShareAxes.XZ:
            self.ShareAxes.XZ = ax
        return ax

    ##################################################################################
    # ----------------------------------Plot 3D Data-------------------------------- #
    ##################################################################################
    def Plot3D(self, x, y, z, color=None, axisName_1=None, axisName_2=None, axisName_3=None, colorName=None, dataName=None, newFigure=True, title=None, mark='-', xLimit=None, yLimit=None, zLimit=None, figureName=''):
        plt.rcParams['font.family'] = 'Microsoft YaHei'
        plt.rcParams.update({'figure.max_open_warning': 0})
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
        if newFigure:
            self.FigNum += 1
            print('')
            self.OutputMessageToGUI('\n')
        sys.stdout.write("\033[1;34m\rPlotData: \033[0mDrawing Figure %2d  %s\033[0m" % (self.FigNum, figureName))
        self.OutputMessageToGUI('PlotData: Drawing Figure %2d  %s' % (self.FigNum, figureName), overwrite=True)
        fig = plt.figure(self.FigNum)
        if newFigure:
            fig.clf()
            ax = fig.add_subplot(projection='3d')
        ax = fig.gca()
        #ax = fig.gca(projection='3d')
        if colorFlag:
            scatter = ax.scatter3D(x, y, z, c=color, label=dataName, alpha=0.7, cmap='coolwarm')
            cbar = plt.colorbar(scatter)
            if colorName != None:
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
        elif figureName != '':
            ax.set_title(figureName)
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
        sys.stdout.write("\033[1;34m\rPlotData: \033[1;32mDone    \033[0mFigure %2d  %s       \033[0m" % (self.FigNum, figureName))
        self.OutputMessageToGUI('PlotData: Done    Figure %2d  %s       ' % (self.FigNum, figureName), overwrite=True)
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
        
        self.PlotPolar(Thtea, Radius, title=title, dataName=dataName, newFigure=True, figureName=figureName)
        plt.yticks(np.array(range(int((R_Display - R_MaxErr) * 1000), int((R_Display + R_MaxErr) * 1000), int(R_DisplayStep * 1000))) / 1000, np.array(range(int(-R_MaxErr * 1000), int(R_MaxErr * 1000), int(R_DisplayStep * 1000))))
        
        return None

    ##################################################################################
    # --------------------------------Plot Polar Data------------------------------- #
    ##################################################################################
    def PlotPolar(self, Theta, Radius, title=None, dataName=None, mark='-', newFigure=True, figureName=''):
        plt.rcParams['font.family'] = 'Microsoft YaHei'
        plt.rcParams.update({'figure.max_open_warning': 0})
        #len = min(Theta.__len__(), Radius.__len__())
        #Theta = np.array(Theta[:len])
        #Radius = np.array(Radius[:len])
        if newFigure:
            self.FigNum += 1
            print('')
            self.OutputMessageToGUI('\n')
        sys.stdout.write("\033[1;34m\rPlotData: \033[0mDrawing Figure %2d  %s\033[0m" % (self.FigNum, figureName))
        self.OutputMessageToGUI('PlotData: Drawing Figure %2d  %s' % (self.FigNum, figureName), overwrite=True)
        fig = plt.figure(self.FigNum)
        if newFigure:
            fig.clf()
            #fig.add_subplot(111, projection='polar')
        plt.polar(Theta, Radius, mark, alpha=0.5)
        if title != None:
            plt.title(title)
        elif figureName != '':
            plt.title(figureName)
        if dataName != None:
            plt.legend(dataName, loc="upper right")
        plt.grid('on')
        plt.ion()
        plt.draw()
        plt.pause(0.001)
        sys.stdout.write("\033[1;34m\rPlotData: \033[1;32mDone    \033[0mFigure %2d  %s       \033[0m" % (self.FigNum, figureName))
        self.OutputMessageToGUI('PlotData: Done    Figure %2d  %s       ' % (self.FigNum, figureName), overwrite=True)
        plt.ioff()
        return None
    
    ##################################################################################
    # -----------------------------Output message to GUI------------------------------ #
    ##################################################################################
    def OutputMessageToGUI(self, message, overwrite=False):
        if self.GuiText != None:
            lineIndex = str(int(float(self.GuiText.index('end')))-1)
            if overwrite:
                self.GuiText.delete(lineIndex+'.0', lineIndex+'.end')
            self.GuiText.insert(lineIndex+'.end', message)
            self.GuiText.update()
            self.GuiText.see('end')

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
    # ---------------------------Read DataName from Str---------------------------- #
    ##################################################################################
    def ReadDataName(self, str):
        elementList = re.split("[#\t\n ]", str)
        self.DataName = []
        for element in elementList:
            if re.match("[0-9a-zA-Z\\[\\]]*", element).group():
                self.DataName.append(element)
        print('\033[1;34m\nDataName in the file:\033[0m')
        self.OutputMessageToGUI('\n\nDataName in the file:\n')
        for i in range(self.DataName.__len__()):
            print('%02d : \033[1;33m%s\033[0m' % (i + 1, self.DataName[i]))
            self.OutputMessageToGUI('%02d : %s\n' % (i + 1, self.DataName[i]))
        print('')
        self.OutputMessageToGUI('\n')
        return self.DataName

    ##################################################################################
    # -----------------------------Load Data from File------------------------------ #
    ##################################################################################
    def LoadData(self):
        
        print('[%s]\n\033[1;34m\n\nLoadData: \033[0mStarting......' % time.strftime('%Y-%m-%d %H:%M:%S'))
        self.OutputMessageToGUI('\n\n[%s]\nLoadData: Starting......' % time.strftime('%Y-%m-%d %H:%M:%S'))

        # -----------------------open file and get textLen------------------------- #
        self.Data.Length = 0
        try:
            with open(self.DataFileName, 'r') as f:
                txt = f.readlines()
        except:
            print('\033[1;34m\nLoadData: \033[1;31mError (CodeLine %d): DataFileName %s\033[0m' % (sys._getframe().f_lineno, self.DataFileName))
            self.OutputMessageToGUI('\nLoadData: Error (CodeLine %d): DataFileName %s\n' % (sys._getframe().f_lineno, self.DataFileName))
            self.Data.Var = dict()
            self.Data.Length = 0
            return None
        textLen = txt.__len__() - 2  # Remove last two lines
        if textLen <= 1:
            print('\033[1;34m\nLoadData: \033[1;31mError (CodeLine %d): textLen =%d <= 1 \033[0m' % (sys._getframe().f_lineno, textLen))
            self.OutputMessageToGUI('\nLoadData: Error (CodeLine %d): textLen =%d <= 1 \n' % (sys._getframe().f_lineno, textLen))
            self.Data.Var = dict()
            self.Data.Length = 0
            return None
        minText = 1
        maxText = textLen
        # -----------------------------get DataName-------------------------------- #
        self.DataName = self.ReadDataName(txt[0])
        varNum = self.DataName.__len__()
        if varNum <= 0:
            print('\033[1;34m\nLoadData: \033[1;31mError (CodeLine %d): varNum = %d  <= 0 \033[0m' % (sys._getframe().f_lineno, varNum))
            self.OutputMessageToGUI('\nLoadData: Error (CodeLine %d): varNum = %d  <= 0 \n' % (sys._getframe().f_lineno, varNum))
            self.Data.Var = dict()
            self.Data.Length = 0
            return None
        # -----------------------------get TimeRange-------------------------------- #
        if self.TimeRange.__len__() != 2:
            print('\033[1;34m\nLoadData: \033[1;31mError (CodeLine %d): TimeRange.__len__() = %d != 2 \033[0m' % (sys._getframe().f_lineno, self.TimeRange.__len__()))
            self.OutputMessageToGUI('\nLoadData: Error (CodeLine %d): TimeRange.__len__() = %d != 2 \n' % (sys._getframe().f_lineno, self.TimeRange.__len__()))
            self.Data.Var = dict()
            self.Data.Length = 0
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
            self.OutputMessageToGUI('\nLoadData: Error (CodeLine %d): BlockRange.__len__() = %d != 2 \n' % (sys._getframe().f_lineno, self.BlockRange.__len__()))
            self.Data.Var = dict()
            self.Data.Length = 0
            return None
        else:
            self.BlockRange[0] = int(self.BlockRange[0])
            self.BlockRange[1] = int(self.BlockRange[1])
        if  self.BlockRange[1] < self.BlockRange[0]:
            self.BlockRange[1] = 0
            
        # ---------------------------------init Data--------------------------------- #
        for i in range(varNum):
            self.Data.Var[self.DataName[i]] = []
        BlockNoExistFlag = self.DataName_BlockNo in self.DataName
        if BlockNoExistFlag:
            BlockNoIndex = self.DataName.index(self.DataName_BlockNo)
        self.Data.Time = []
        self.Data.BlockNo = []
        # ----------load Data DataName, varNum, BlockRange and TimeRange------------ #
        self.RemainingLineData = []
        LastBlockNo = 0
        dataStartFlag = False
        dataEndFlag = False
        firstDataFlag = True
        Time = 0.0 # unit: s
        self.LoadDataPercentageOld = 0.0
        for i in range(minText, maxText):
            self.LoadDataPercentage = (i - minText) / (maxText - minText) * 100
            if int(self.LoadDataPercentage) > int(self.LoadDataPercentageOld):
                sys.stdout.write('\033[1;34m\rLoadData: \033[0m%3d%%' % (self.LoadDataPercentage))
                self.OutputMessageToGUI('LoadData: %3d%%' % (self.LoadDataPercentage), overwrite=True)
            self.LoadDataPercentageOld = self.LoadDataPercentage
            self.LineData = self.SplitDataStr(txt[i])
            while True:
                self.LineData = self.RemainingLineData + self.LineData
                if self.LineData.__len__() < varNum:
                    print('\033[1;34m\nLoadData: \033[1;31mError (DataFileLine %d): LineData.__len__ < varNum (%d < %d) \033[0m' % ( i+1, self.LineData.__len__(), varNum))
                    self.OutputMessageToGUI('\nLoadData: Error (DataFileLine %d): LineData.__len__ < varNum (%d < %d) \n' % ( i+1, self.LineData.__len__(), varNum))
                    self.Data.Length = 0
                    return None
                if BlockNoExistFlag:
                    if float(self.LineData[BlockNoIndex]) >= 1.23456789e308:
                        self.LineData[BlockNoIndex] = LastBlockNo
                    if dataStartFlag == False and Time >= self.TimeRange[0] and float(self.LineData[BlockNoIndex]) >= self.BlockRange[0]:
                        dataStartFlag = True
                    if dataEndFlag == False and ((Time > self.TimeRange[1] and self.TimeRange[1] > 0) or (float(self.LineData[BlockNoIndex]) > self.BlockRange[1] and self.BlockRange[1] > 0)):
                        dataEndFlag = True
                    if dataStartFlag == True and dataEndFlag == False:
                        for j in range(varNum):
                            self.Data.Var[self.DataName[j]].append(float(self.LineData[j]))
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
                            self.Data.Var[self.DataName[j]].append(float(self.LineData[j]))
                        if firstDataFlag:
                            firstDataFlag = False
                            minTime = maxTime = float(Time)
                        else:
                            minTime = min(minTime, float(Time))
                            maxTime = min(maxTime, float(Time))
                Time += self.Ts
                Time = round(Time, 6)
                self.RemainingLineData = self.LineData[varNum:]
                self.LineData = []
                if self.RemainingLineData.__len__() < varNum:
                    break
            if dataEndFlag == True:
                break
        # ---------------------------output Data----------------------------------- #
        for i in range(varNum):
            self.Data.Var[self.DataName[i]] = np.array(self.Data.Var[self.DataName[i]])
        
        self.Data.Length = self.Data.Var[self.DataName[0]].__len__()
        if self.Data.Var.__len__() <= 0 or self.Data.Length <= 0:
            print('\033[1;34m\nLoadData: \033[1;31mError (CodeLine %d): Data Len = %d! \033[0m' % (sys._getframe().f_lineno, self.Data.Length))
            self.OutputMessageToGUI('\nLoadData: Error (CodeLine %d): Data Len = %d! \n' % (sys._getframe().f_lineno, self.Data.Length))
            self.Data.Length = 0
            return None
        if BlockNoExistFlag:
            self.Data.TimeRange  = [float(minTime), float(maxTime)]
            self.Data.BlockRange = [int(minBlockNo), int(maxBlockNo)]
            print('\033[1;34m\rLoadData: \033[1;32m100%%\033[0m\nDataLength=%d, TimeRange=[%.3f, %.3f], BlockRange=[%d, %d] \033[0m' % (self.Data.Length, minTime, maxTime, minBlockNo, maxBlockNo))
            self.OutputMessageToGUI('LoadData: 100%%      DataLength=%d, BlockRange=[%d, %d], TimeRange=[%.3f, %.3f]' % (self.Data.Length, minBlockNo, maxBlockNo, minTime, maxTime), overwrite=True)
        else:
            self.Data.TimeRange  = [float(minTime), float(maxTime)]
            print('\033[1;34m\rLoadData: \033[1;32m100%%\033[0m\nDataLength=%d, TimeRange=[%.3f, %.3f] \033[0m' % (self.Data.Length, minTime, maxTime))
            self.OutputMessageToGUI('LoadData: 100%%      DataLength=%d, TimeRange=[%.3f, %.3f]' % (self.Data.Length, minTime, maxTime), overwrite=True)

        # --------------------------------init Data-------------------------------- #
        #Time
        if self.Ts > 0:
            self.Data.Time = np.array(range(0, self.Data.Length)) * self.Ts + minTime
            
        #BlockNo
        if self.DataName_BlockNo in self.DataName:
            self.Data.BlockNo = self.Data.Var[self.DataName_BlockNo]
            
        # X
        if self.DataName_SetPos % (self.AxisID_X - 1) in self.DataName:
            self.Data.SetPos_X = np.array(self.Data.Var[self.DataName_SetPos % (self.AxisID_X - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.SetVel_X = np.diff(self.Data.SetPos_X)/ self.Ts * 60 # mm/min
            data = self.Data.SetVel_X; data = np.append(data, data[-1])
            self.Data.SetVel_X = data
            self.Data.SetAcc_X = np.diff(np.diff(self.Data.SetPos_X)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.SetAcc_X; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.SetAcc_X = data
            self.Data.SetJerk_X = np.diff(np.diff(np.diff(self.Data.SetPos_X))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.SetJerk_X; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.SetJerk_X = data
        if self.DataName_CmdPos % (self.AxisID_X - 1) in self.DataName:
            self.Data.CmdPos_X = np.array(self.Data.Var[self.DataName_CmdPos % (self.AxisID_X - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.CmdVel_X = np.diff(self.Data.CmdPos_X)/ self.Ts * 60 # mm/min
            data = self.Data.CmdVel_X; data = np.append(data, data[-1])
            self.Data.CmdVel_X = data
            self.Data.CmdAcc_X = np.diff(np.diff(self.Data.CmdPos_X)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.CmdAcc_X; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.CmdAcc_X = data
            self.Data.CmdJerk_X = np.diff(np.diff(np.diff(self.Data.CmdPos_X))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.CmdJerk_X; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.CmdJerk_X = data
        if self.DataName_ActPos % (self.AxisID_X - 1) in self.DataName:
            self.Data.ActPos_X = np.array(self.Data.Var[self.DataName_ActPos % (self.AxisID_X - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.ActVel_X = np.diff(self.Data.ActPos_X)/ self.Ts * 60 # mm/min
            data = self.Data.ActVel_X; data = np.append(data, data[-1])
            self.Data.ActVel_X = data
            self.Data.ActAcc_X = np.diff(np.diff(self.Data.ActPos_X)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.ActAcc_X; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.ActAcc_X = data
            self.Data.ActJerk_X = np.diff(np.diff(np.diff(self.Data.ActPos_X))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.ActJerk_X; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.ActJerk_X = data
            
        # Y
        if self.DataName_SetPos % (self.AxisID_Y - 1) in self.DataName:
            self.Data.SetPos_Y = np.array(self.Data.Var[self.DataName_SetPos % (self.AxisID_Y - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.SetVel_Y = np.diff(self.Data.SetPos_Y)/ self.Ts * 60 # mm/min
            data = self.Data.SetVel_Y; data = np.append(data, data[-1])
            self.Data.SetVel_Y = data
            self.Data.SetAcc_Y = np.diff(np.diff(self.Data.SetPos_Y)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.SetAcc_Y; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.SetAcc_Y = data
            self.Data.SetJerk_Y = np.diff(np.diff(np.diff(self.Data.SetPos_Y))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.SetJerk_Y; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.SetJerk_Y = data
        if self.DataName_CmdPos % (self.AxisID_Y - 1) in self.DataName:
            self.Data.CmdPos_Y = np.array(self.Data.Var[self.DataName_CmdPos % (self.AxisID_Y - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.CmdVel_Y = np.diff(self.Data.CmdPos_Y)/ self.Ts * 60 # mm/min
            data = self.Data.CmdVel_Y; data = np.append(data, data[-1])
            self.Data.CmdVel_Y = data
            self.Data.CmdAcc_Y = np.diff(np.diff(self.Data.CmdPos_Y)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.CmdAcc_Y; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.CmdAcc_Y = data
            self.Data.CmdJerk_Y = np.diff(np.diff(np.diff(self.Data.CmdPos_Y))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.CmdJerk_Y; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.CmdJerk_Y = data
        if self.DataName_ActPos % (self.AxisID_Y - 1) in self.DataName:
            self.Data.ActPos_Y = np.array(self.Data.Var[self.DataName_ActPos % (self.AxisID_Y - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.ActVel_Y = np.diff(self.Data.ActPos_Y)/ self.Ts * 60 # mm/min
            data = self.Data.ActVel_Y; data = np.append(data, data[-1])
            self.Data.ActVel_Y = data
            self.Data.ActAcc_Y = np.diff(np.diff(self.Data.ActPos_Y)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.ActAcc_Y; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.ActAcc_Y = data
            self.Data.ActJerk_Y = np.diff(np.diff(np.diff(self.Data.ActPos_Y))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.ActJerk_Y; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.ActJerk_Y = data
            
        # Z
        if self.DataName_SetPos % (self.AxisID_Z - 1) in self.DataName:
            self.Data.SetPos_Z = np.array(self.Data.Var[self.DataName_SetPos % (self.AxisID_Z - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.SetVel_Z = np.diff(self.Data.SetPos_Z)/ self.Ts * 60 # mm/min
            data = self.Data.SetVel_Z; data = np.append(data, data[-1])
            self.Data.SetVel_Z = data
            self.Data.SetAcc_Z = np.diff(np.diff(self.Data.SetPos_Z)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.SetAcc_Z; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.SetAcc_Z = data
            self.Data.SetJerk_Z = np.diff(np.diff(np.diff(self.Data.SetPos_Z))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.SetJerk_Z; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.SetJerk_Z = data
        if self.DataName_CmdPos % (self.AxisID_Z - 1) in self.DataName:
            self.Data.CmdPos_Z = np.array(self.Data.Var[self.DataName_CmdPos % (self.AxisID_Z - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.CmdVel_Z = np.diff(self.Data.CmdPos_Z)/ self.Ts * 60 # mm/min
            data = self.Data.CmdVel_Z; data = np.append(data, data[-1])
            self.Data.CmdVel_Z = data
            self.Data.CmdAcc_Z = np.diff(np.diff(self.Data.CmdPos_Z)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.CmdAcc_Z; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.CmdAcc_Z = data
            self.Data.CmdJerk_Z = np.diff(np.diff(np.diff(self.Data.CmdPos_Z))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.CmdJerk_Z; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.CmdJerk_Z = data
        if self.DataName_ActPos % (self.AxisID_Z - 1) in self.DataName:
            self.Data.ActPos_Z = np.array(self.Data.Var[self.DataName_ActPos % (self.AxisID_Z - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.ActVel_Z = np.diff(self.Data.ActPos_Z)/ self.Ts * 60 # mm/min
            data = self.Data.ActVel_Z; data = np.append(data, data[-1])
            self.Data.ActVel_Z = data
            self.Data.ActAcc_Z = np.diff(np.diff(self.Data.ActPos_Z)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.ActAcc_Z; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.ActAcc_Z = data
            self.Data.ActJerk_Z = np.diff(np.diff(np.diff(self.Data.ActPos_Z))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.ActJerk_Z; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.ActJerk_Z = data
            
        # A
        if self.DataName_SetPos % (self.AxisID_A - 1) in self.DataName:
            self.Data.SetPos_A = np.array(self.Data.Var[self.DataName_SetPos % (self.AxisID_A - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.SetVel_A = np.diff(self.Data.SetPos_A)/ self.Ts * 60 # mm/min
            data = self.Data.SetVel_A; data = np.append(data, data[-1])
            self.Data.SetVel_A = data
            self.Data.SetAcc_A = np.diff(np.diff(self.Data.SetPos_A)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.SetAcc_A; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.SetAcc_A = data
            self.Data.SetJerk_A = np.diff(np.diff(np.diff(self.Data.SetPos_A))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.SetJerk_A; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.SetJerk_A = data
        if self.DataName_CmdPos % (self.AxisID_A - 1) in self.DataName:
            self.Data.CmdPos_A = np.array(self.Data.Var[self.DataName_CmdPos % (self.AxisID_A - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.CmdVel_A = np.diff(self.Data.CmdPos_A)/ self.Ts * 60 # mm/min
            data = self.Data.CmdVel_A; data = np.append(data, data[-1])
            self.Data.CmdVel_A = data
            self.Data.CmdAcc_A = np.diff(np.diff(self.Data.CmdPos_A)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.CmdAcc_A; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.CmdAcc_A = data
            self.Data.CmdJerk_A = np.diff(np.diff(np.diff(self.Data.CmdPos_A))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.CmdJerk_A; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.CmdJerk_A = data
        if self.DataName_ActPos % (self.AxisID_A - 1) in self.DataName:
            self.Data.ActPos_A = np.array(self.Data.Var[self.DataName_ActPos % (self.AxisID_A - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.ActVel_A = np.diff(self.Data.ActPos_A)/ self.Ts * 60 # mm/min
            data = self.Data.ActVel_A; data = np.append(data, data[-1])
            self.Data.ActVel_A = data
            self.Data.ActAcc_A = np.diff(np.diff(self.Data.ActPos_A)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.ActAcc_A; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.ActAcc_A = data
            self.Data.ActJerk_A = np.diff(np.diff(np.diff(self.Data.ActPos_A))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.ActJerk_A; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.ActJerk_A = data
            
        # B
        if self.DataName_SetPos % (self.AxisID_B - 1) in self.DataName:
            self.Data.SetPos_B = np.array(self.Data.Var[self.DataName_SetPos % (self.AxisID_B - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.SetVel_B = np.diff(self.Data.SetPos_B)/ self.Ts * 60 # mm/min
            data = self.Data.SetVel_B; data = np.append(data, data[-1])
            self.Data.SetVel_B = data
            self.Data.SetAcc_B = np.diff(np.diff(self.Data.SetPos_B)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.SetAcc_B; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.SetAcc_B = data
            self.Data.SetJerk_B = np.diff(np.diff(np.diff(self.Data.SetPos_B))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.SetJerk_B; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.SetJerk_B = data
        if self.DataName_CmdPos % (self.AxisID_B - 1) in self.DataName:
            self.Data.CmdPos_B = np.array(self.Data.Var[self.DataName_CmdPos % (self.AxisID_B - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.CmdVel_B = np.diff(self.Data.CmdPos_B)/ self.Ts * 60 # mm/min
            data = self.Data.CmdVel_B; data = np.append(data, data[-1])
            self.Data.CmdVel_B = data
            self.Data.CmdAcc_B = np.diff(np.diff(self.Data.CmdPos_B)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.CmdAcc_B; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.CmdAcc_B = data
            self.Data.CmdJerk_B = np.diff(np.diff(np.diff(self.Data.CmdPos_B))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.CmdJerk_B; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.CmdJerk_B = data
        if self.DataName_ActPos % (self.AxisID_B - 1) in self.DataName:
            self.Data.ActPos_B = np.array(self.Data.Var[self.DataName_ActPos % (self.AxisID_B - 1)]) * self.Precision_um / 1e3 # mm
            self.Data.ActVel_B = np.diff(self.Data.ActPos_B)/ self.Ts * 60 # mm/min
            data = self.Data.ActVel_B; data = np.append(data, data[-1])
            self.Data.ActVel_B = data
            self.Data.ActAcc_B = np.diff(np.diff(self.Data.ActPos_B)) / 1e3 / self.Ts / self.Ts # m/s^2
            data = self.Data.ActAcc_B; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.ActAcc_B = data
            self.Data.ActJerk_B = np.diff(np.diff(np.diff(self.Data.ActPos_B))) / 1e3 / self.Ts / self.Ts / self.Ts # m/s^3
            data = self.Data.ActJerk_B; data = np.append(data, data[-1]); data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.ActJerk_B = data
            
        #PathVel
        if self.DataName_SetPathVel in self.DataName:
            self.Data.SetPathVel = np.array(self.Data.Var[self.DataName_SetPathVel]) * self.Precision_um /1e3 / self.Ts * 60 # mm/min
            self.Data.SetPathAcc = np.diff(self.Data.SetPathVel / 1e3 / 60) / self.Ts # m/s^2
            self.Data.SetPathJerk = np.diff(self.Data.SetPathAcc) / self.Ts # m/s^3
            data = self.Data.SetPathAcc; data = np.append(data, data[-1])
            self.Data.SetPathAcc = data
            data = self.Data.SetPathJerk; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.SetPathJerk = data
        if self.DataName_CmdPathVel in self.DataName:
            self.Data.CmdPathVel = np.array(self.Data.Var[self.DataName_CmdPathVel]) * self.Precision_um /1e3 / self.Ts * 60 # mm/min
            self.Data.CmdPathAcc = np.diff(self.Data.CmdPathVel / 1e3 / 60) / self.Ts # m/s^2
            self.Data.CmdPathJerk = np.diff(self.Data.CmdPathAcc) / self.Ts # m/s^3
            data = self.Data.CmdPathAcc; data = np.append(data, data[-1])
            self.Data.CmdPathAcc = data
            data = self.Data.CmdPathJerk; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.CmdPathJerk = data
        data = np.zeros(self.Data.Length)
        if self.DataName_SetPos % (self.AxisID_X - 1) in self.DataName:
            data += self.Data.ActVel_X ** 2
        if self.DataName_SetPos % (self.AxisID_Y - 1) in self.DataName:
            data += self.Data.ActVel_Y ** 2
        if self.DataName_SetPos % (self.AxisID_Z - 1) in self.DataName:
            data += self.Data.ActVel_Z ** 2
        try:
            self.Data.ActPathVel = np.sqrt(data) # mm/min
        except:
            self.Data.ActPathVel = []
        if self.Data.ActPathVel.__len__() != 0:
            self.Data.ActPathAcc = np.diff(self.Data.ActPathVel) / 1e3 / 60 / self.Ts # m/s^2
            self.Data.ActPathJerk = np.diff(self.Data.ActPathAcc) / self.Ts # m/s^3
            data = self.Data.ActPathAcc; data = np.append(data, data[-1])
            self.Data.ActPathAcc = data
            data = self.Data.ActPathJerk; data = np.append(data, data[-1]); data = np.append(data, data[-1])
            self.Data.ActPathJerk = data
        else:
            self.Data.ActPathAcc = []
            self.Data.ActPathJerk = []
            
        #PosErr
        data = np.zeros(self.Data.Length)
        if self.DataName_CmdPos % (self.AxisID_X - 1) in self.DataName and self.DataName_ActPos % (self.AxisID_X - 1) in self.DataName:
                data += (self.Data.CmdPos_X - self.Data.ActPos_X) ** 2
        if self.DataName_CmdPos % (self.AxisID_Y - 1) in self.DataName and self.DataName_ActPos % (self.AxisID_Y - 1) in self.DataName:
                data += (self.Data.CmdPos_Y - self.Data.ActPos_Y) ** 2
        if self.DataName_CmdPos % (self.AxisID_Z - 1) in self.DataName and self.DataName_ActPos % (self.AxisID_Z - 1) in self.DataName:
                data += (self.Data.CmdPos_Z - self.Data.ActPos_Z) ** 2
        try:
            self.Data.PosErr = np.sqrt(data) # mm/min
        except:
            self.Data.PosErr = []
        
        return None
    
    def ShowFigure(self):
        plt.show()
        
    def DataInfo(self, *DataInfo, infoName = []):
        try:
            import mpldatacursor
        except:
            return None
        if self.DataInfoExist:
            return None
        if self.Data.Length == 0 or self.FigNum == 0:
            return None
        figs = [plt.figure(Num) for Num in range(1, self.FigNum + 1)]
        axes = [ax for fig in figs for ax in fig.axes]
        lines = [line for ax in axes for line in ax.lines]
        lines2D = list(filter(lambda line: type(line) == matplotlib.lines.Line2D, lines))
        scatters = [collection for ax in axes for collection in ax.collections]
        scatters2D = list(filter(lambda scatter: type(scatter) == matplotlib.collections.PathCollection, scatters))
        artists = lines2D + scatters2D
        if DataInfo.__len__() == 0:
            if self.DataName_BlockNo in self.DataName:
                DataInfo = [self.Data.Time, self.Data.BlockNo]
                infoName = ['Time(s)', 'BlockNo']
            else:
                DataInfo = [self.Data.Time]
                infoName = ['Time(s)']
        try:
            self.InfoValueList = []
            for info in DataInfo:
                if info.__len__() != self.Data.Length:
                    print('\033[1;34m\n\nDataInfo: \033[1;33mWarnning: info.__len__() = %d != self.Data.Length\033[0m' % info.__len__())
                    self.OutputMessageToGUI('\n\nDataInfo: Warnning: info.__len__() = %d != self.Data.Length \n' % info.__len__())
                    break
                self.InfoValueList.append(info)
            self.InfoText = []
            for i in range(self.Data.Length):
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
            mpldatacursor.datacursor(artists, display='multiple', draggable=True, formatter=lambda **param: self.InfoText[param['ind'][0]])
            self.DataInfoExist = True
            #print('\033[1;34m\n\nDataInfo: \033[1;32mDone\033[0m')
            #self.OutputMessageToGUI('\n\nDataInfo: Done \n')
        except:
            print('\033[1;34m\n\nDataInfo: \033[1;31mError\033[0m')
            self.OutputMessageToGUI('\n\nDataInfo: Error \n')
        return None

##################################################################################
# -------------------------------------GUI-------------------------------------- #
##################################################################################
if __name__ == '__main__':

    PA = PA_Data_Analyze()
    PA.AxisID_X = 1
    PA.AxisID_Y = 2
    PA.AxisID_Z = 3

    TextBox         = dict()
    Button          = dict()
    Entry           = dict()
    Label           = dict()
    StringVar       = dict()
    Combobox        = dict()
    ScrolledText    = dict()
    LabelFrame      = dict()
    CheckButton     = dict()
    CheckVar        = dict()
    Notebook        = dict()
    Frame           = dict()

    window = tk.Tk()
    window.title('PA Data Analyze v%s' % Version)
    #window.geometry('1000x615')
    window.geometry('1300x800')
    #弹出窗口
    window.iconify()
    window.update()
    window.deiconify()

    def open_file():
        filename = filedialog.askopenfilename(title='打开文件', filetypes=[('txt', '*.txt')])
        if filename != '':
            Entry['文件路径'].delete(0, tk.END)
            Entry['文件路径'].insert('insert', filename)

    def load_file():
        PA.DataFileName = Entry['文件路径'].get()
        PA.Ts = float(Entry['Ts'].get())

        PA.BlockRange[0] = int(Entry['BlockRange_0'].get()) if Entry['BlockRange_0'].get() != '无' and Entry['BlockRange_0'].get() != '' else 0
        PA.BlockRange[1] = int(Entry['BlockRange_1'].get()) if Entry['BlockRange_1'].get() != '无' and Entry['BlockRange_1'].get() != '' else 0

        PA.TimeRange[0] = float(Entry['TimeRange_0'].get()) if Entry['TimeRange_0'].get() != '无' and Entry['TimeRange_0'].get() != '' else 0
        PA.TimeRange[1] = float(Entry['TimeRange_1'].get()) if Entry['TimeRange_1'].get() != '无' and Entry['TimeRange_1'].get() != '' else 0

        PA.AxisID_X = int(Combobox['AxisID_X'].get()) if Combobox['AxisID_X'].get() != '无' else 0
        PA.AxisID_Y = int(Combobox['AxisID_Y'].get()) if Combobox['AxisID_Y'].get() != '无' else 0
        PA.AxisID_Z = int(Combobox['AxisID_Z'].get()) if Combobox['AxisID_Z'].get() != '无' else 0
        PA.AxisID_A = int(Combobox['AxisID_A'].get()) if Combobox['AxisID_A'].get() != '无' else 0
        PA.AxisID_B = int(Combobox['AxisID_B'].get()) if Combobox['AxisID_B'].get() != '无' else 0

        if PA.AxisID_X == 0 and PA.AxisID_Y == 0 and PA.AxisID_Z == 0 and PA.AxisID_A == 0:
            return None
        PA.GuiText = ScrolledText['输出消息']
        PA.LoadData()

    def plot_data():
        PA.Plot.BlockNo = int(CheckVar['BlockNo'].get())
        PA.Plot.PathVel = int(CheckVar['PathVel'].get())
        PA.Plot.PathAcc = int(CheckVar['PathAcc'].get())
        PA.Plot.PathJerk = int(CheckVar['PathJerk'].get())
        PA.Plot.Pos_X = int(CheckVar['Pos_X'].get())
        PA.Plot.Vel_X = int(CheckVar['Vel_X'].get())
        PA.Plot.Acc_X = int(CheckVar['Acc_X'].get())
        PA.Plot.Jerk_X = int(CheckVar['Jerk_X'].get())
        PA.Plot.Pos_Y = int(CheckVar['Pos_Y'].get())
        PA.Plot.Vel_Y = int(CheckVar['Vel_Y'].get())
        PA.Plot.Acc_Y = int(CheckVar['Acc_Y'].get())
        PA.Plot.Jerk_Y = int(CheckVar['Jerk_Y'].get())
        PA.Plot.Pos_Z = int(CheckVar['Pos_Z'].get())
        PA.Plot.Vel_Z = int(CheckVar['Vel_Z'].get())
        PA.Plot.Acc_Z = int(CheckVar['Acc_Z'].get())
        PA.Plot.Jerk_Z = int(CheckVar['Jerk_Z'].get())
        PA.Plot.Pos_A = int(CheckVar['Pos_A'].get())
        PA.Plot.Vel_A = int(CheckVar['Vel_A'].get())
        PA.Plot.Acc_A = int(CheckVar['Acc_A'].get())
        PA.Plot.Jerk_A = int(CheckVar['Jerk_A'].get())
        PA.Plot.Pos_B = int(CheckVar['Pos_B'].get())
        PA.Plot.Vel_B = int(CheckVar['Vel_B'].get())
        PA.Plot.Acc_B = int(CheckVar['Acc_B'].get())
        PA.Plot.Jerk_B = int(CheckVar['Jerk_B'].get())

        PA.Plot.XY = int(CheckVar['XY'].get())
        PA.Plot.XY_Time = int(CheckVar['XY_Time'].get())
        PA.Plot.XY_BlockNo = int(CheckVar['XY_BlockNo'].get())
        PA.Plot.XY_PathVel = int(CheckVar['XY_PathVel'].get())
        PA.Plot.XY_PathAcc = int(CheckVar['XY_PathAcc'].get())
        PA.Plot.XY_PathJerk = int(CheckVar['XY_PathJerk'].get())
        PA.Plot.XY_PosErr = int(CheckVar['XY_PosErr'].get())
        PA.Plot.XY_Z = int(CheckVar['XY_Z'].get())
        PA.Plot.YZ = int(CheckVar['YZ'].get())
        PA.Plot.YZ_Time = int(CheckVar['YZ_Time'].get())
        PA.Plot.YZ_BlockNo = int(CheckVar['YZ_BlockNo'].get())
        PA.Plot.YZ_PathVel = int(CheckVar['YZ_PathVel'].get())
        PA.Plot.YZ_PathAcc = int(CheckVar['YZ_PathAcc'].get())
        PA.Plot.YZ_PathJerk = int(CheckVar['YZ_PathJerk'].get())
        PA.Plot.YZ_PosErr = int(CheckVar['YZ_PosErr'].get())
        PA.Plot.YZ_X = int(CheckVar['YZ_X'].get())
        PA.Plot.XZ = int(CheckVar['XZ'].get())
        PA.Plot.XZ_Time = int(CheckVar['XZ_Time'].get())
        PA.Plot.XZ_BlockNo = int(CheckVar['XZ_BlockNo'].get())
        PA.Plot.XZ_PathVel = int(CheckVar['XZ_PathVel'].get())
        PA.Plot.XZ_PathAcc = int(CheckVar['XZ_PathAcc'].get())
        PA.Plot.XZ_PathJerk = int(CheckVar['XZ_PathJerk'].get())
        PA.Plot.XZ_PosErr = int(CheckVar['XZ_PosErr'].get())
        PA.Plot.XZ_Y = int(CheckVar['XZ_Y'].get())

        PA.Plot.XYZ = int(CheckVar['XYZ'].get())
        PA.Plot.XYZ_Time = int(CheckVar['XYZ_Time'].get())
        PA.Plot.XYZ_Z = int(CheckVar['XYZ_Z'].get())
        PA.Plot.XYZ_PathVel = int(CheckVar['XYZ_PathVel'].get())
        PA.Plot.XYZ_PathAcc = int(CheckVar['XYZ_PathAcc'].get())
        PA.Plot.XYZ_PathJerk = int(CheckVar['XYZ_PathJerk'].get())

        PA.Plot.CircleErr_XY = int(CheckVar['CircleErr_XY'].get())
        PA.Plot.CircleErr_YZ = int(CheckVar['CircleErr_YZ'].get())
        PA.Plot.CircleErr_XZ = int(CheckVar['CircleErr_XZ'].get())

        PA.GuiText = ScrolledText['输出消息']
        PA.PlotData()

        UserCodeEnable = int(CheckVar['用户代码'].get())
        UserCode = ScrolledText['用户代码'].get('1.0', 'end')
        if UserCodeEnable:
            try:
                Data                = PA.Data
                Var                 = PA.Data.Var
                Plot                = PA.Plot
                Plot1D              = PA.Plot1D
                Plot2D              = PA.Plot2D
                Plot3D              = PA.Plot3D
                PlotCircleError     = PA.PlotCircleError
                DataInfo            = PA.DataInfo
                OutputMessageToGUI  = PA.OutputMessageToGUI
                exec(UserCode)
            except Exception as e:
                print('\033[1;34m\nUerCode: \033[1;31mError: %s\033[0m' % str(e))
                PA.OutputMessageToGUI('\n\nUserCode Error: %s' % str(e))
            
        PA.DataInfo()

    #################################### 文件路径 ####################################
    x = 0.05
    y = 0.05
    LabelFrame['文件路径'] = ttk.LabelFrame(window, text='文件路径')
    LabelFrame['文件路径'].place(relx=x - 0.03, rely=y - 0.03, relheight=0.093, relwidth=0.95)

    Entry['文件路径'] = ttk.Entry(window, font=('Microsoft YaHei', 10))
    Entry['文件路径'].delete(0, tk.END)
    Entry['文件路径'].insert('insert', PA.DataFileName)
    Entry['文件路径'].place(relx=x, rely=y, relheight=0.05, relwidth=0.7)
    Button['选择文件'] = ttk.Button(window, text="选择文件", command=open_file)
    Button['选择文件'].place(relx=x + 0.8, rely=y, relheight=0.05, relwidth=0.1)

    #################################### 采样参数 ####################################
    x = 0.05
    y = 0.15
    LabelFrame['采样参数'] = ttk.LabelFrame(window, text='采样参数')
    LabelFrame['采样参数'].place(relx=x - 0.03, rely=y - 0.03, relheight=0.165, relwidth=0.95)
    
    x = 0
    y = 0
    xBias = 0.875
    yBias = 0.01
    Button['加载文件'] = ttk.Button(LabelFrame['采样参数'], text="加载文件", command=load_file)
    Button['加载文件'].place(relx=x+xBias, rely=y+yBias, relheight=0.88, relwidth=0.105)
    
    # --------------------------------- 采样参数 1 -----------------------------------#
    x = 0
    y = 0
    xBias = 0.01
    yBias = 0.01
    Label['采样时间'] = ttk.Label(LabelFrame['采样参数'], text='采样时间(s)：', anchor='w', font=('Microsoft YaHei', 9))
    Label['采样时间'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.1)
    xBias += 0.09
    Entry['Ts'] = ttk.Entry(LabelFrame['采样参数'], font=('Microsoft YaHei', 9))
    Entry['Ts'].delete(0, tk.END)
    Entry['Ts'].insert('insert', PA.Ts)
    Entry['Ts'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.06)
    
    x = 0.182
    y = 0
    xBias = 0.01
    yBias = 0.01
    Label['NC行号范围'] = ttk.Label(LabelFrame['采样参数'], text='NC行号范围：', anchor='w', font=('Microsoft YaHei', 9))
    Label['NC行号范围'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.1)
    xBias += 0.1
    Entry['BlockRange_0'] = ttk.Entry(LabelFrame['采样参数'], font=('Microsoft YaHei', 9))
    Entry['BlockRange_0'].delete(0, tk.END)
    if PA.BlockRange[0]:
        Entry['BlockRange_0'].insert('insert', PA.BlockRange[0])
    else:
        Entry['BlockRange_0'].insert('insert', '无')
    Entry['BlockRange_0'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.09)
    xBias += 0.095
    Label['NC行号范围波浪线'] = ttk.Label(LabelFrame['采样参数'], text='~', anchor='w', font=('Microsoft YaHei', 9))
    Label['NC行号范围波浪线'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.1)
    xBias += 0.02
    Entry['BlockRange_1'] = ttk.Entry(LabelFrame['采样参数'], font=('Microsoft YaHei', 9))
    Entry['BlockRange_1'].delete(0, tk.END)
    if PA.BlockRange[1]:
        Entry['BlockRange_1'].insert('insert', PA.BlockRange[1])
    else:
        Entry['BlockRange_1'].insert('insert', '无')
    Entry['BlockRange_1'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.09)
        
    x = 0.52
    y = 0
    xBias = 0.01
    yBias = 0.01
    Label['时间范围'] = ttk.Label(LabelFrame['采样参数'], text='时间范围(s)：', anchor='w', font=('Microsoft YaHei', 9))
    Label['时间范围'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.1)
    xBias += 0.1
    Entry['TimeRange_0'] = ttk.Entry(LabelFrame['采样参数'], font=('Microsoft YaHei', 9))
    Entry['TimeRange_0'].delete(0, tk.END)
    if PA.TimeRange[0]:
        Entry['TimeRange_0'].insert('insert', PA.TimeRange[0])
    else:
        Entry['TimeRange_0'].insert('insert', '无')
    Entry['TimeRange_0'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.09)
    xBias += 0.095
    Label['时间范围波浪线'] = ttk.Label(LabelFrame['采样参数'], text='~', anchor='w', font=('Microsoft YaHei', 9))
    Label['时间范围波浪线'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.1)
    xBias += 0.02
    Entry['TimeRange_1'] = ttk.Entry(LabelFrame['采样参数'], font=('Microsoft YaHei', 9))
    Entry['TimeRange_1'].delete(0, tk.END)
    if PA.TimeRange[1]:
        Entry['TimeRange_1'].insert('insert', PA.TimeRange[1])
    else:
        Entry['TimeRange_1'].insert('insert', '无')
    Entry['TimeRange_1'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.09)

    # --------------------------------- 采样参数 2 -----------------------------------#
    xStep = 0.176
    x = 0
    y = 0
    xBias = 0.01
    yBias = 0.5
    Label['X轴轴号'] = ttk.Label(LabelFrame['采样参数'], text='X轴轴号：', anchor='w', font=('Microsoft YaHei', 9))
    Label['X轴轴号'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.1)
    StringVar['X轴轴号'] = tk.StringVar()
    if int(PA.AxisID_X) >= 1 and int(PA.AxisID_X) <= 32:
        StringVar['X轴轴号'].set(str(int(PA.AxisID_X)))
    else:
        StringVar['X轴轴号'].set(str('无'))
    values = list(map(str, list(range(1, 33))))
    values.insert(0, '无')
    xBias += 0.07
    Combobox['AxisID_X'] = ttk.Combobox(LabelFrame['采样参数'], textvariable=StringVar['X轴轴号'], values=values, font=('Microsoft YaHei', 9), state='readonly')
    Combobox['AxisID_X'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.05)

    x += xStep
    y = 0
    xBias = 0.01
    yBias = 0.5
    Label['Y轴轴号'] = ttk.Label(LabelFrame['采样参数'], text='Y轴轴号：', anchor='w', font=('Microsoft YaHei', 9))
    Label['Y轴轴号'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.1)
    StringVar['Y轴轴号'] = tk.StringVar()
    if int(PA.AxisID_Y) >= 1 and int(PA.AxisID_Y) <= 32:
        StringVar['Y轴轴号'].set(str(int(PA.AxisID_Y)))
    else:
        StringVar['Y轴轴号'].set(str('无'))
    values = list(map(str, list(range(1, 33))))
    values.insert(0, '无')
    xBias += 0.07
    Combobox['AxisID_Y'] = ttk.Combobox(LabelFrame['采样参数'], textvariable=StringVar['Y轴轴号'], values=values, font=('Microsoft YaHei', 9), state='readonly')
    Combobox['AxisID_Y'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.05)

    x += xStep
    y = 0
    xBias = 0.01
    yBias = 0.5
    Label['Z轴轴号'] = ttk.Label(LabelFrame['采样参数'], text='Z轴轴号：', anchor='w', font=('Microsoft YaHei', 9))
    Label['Z轴轴号'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.1)
    StringVar['Z轴轴号'] = tk.StringVar()
    if int(PA.AxisID_Z) >= 1 and int(PA.AxisID_Z) <= 32:
        StringVar['Z轴轴号'].set(str(int(PA.AxisID_Z)))
    else:
        StringVar['Z轴轴号'].set(str('无'))
    values = list(map(str, list(range(1, 33))))
    values.insert(0, '无')
    xBias += 0.07
    Combobox['AxisID_Z'] = ttk.Combobox(LabelFrame['采样参数'], textvariable=StringVar['Z轴轴号'], values=values, font=('Microsoft YaHei', 9), state='readonly')
    Combobox['AxisID_Z'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.05)

    x += xStep
    y = 0
    xBias = 0.01
    yBias = 0.5
    Label['A轴轴号'] = ttk.Label(LabelFrame['采样参数'], text='A轴轴号：', anchor='w', font=('Microsoft YaHei', 9))
    Label['A轴轴号'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.1)
    StringVar['A轴轴号'] = tk.StringVar()
    if int(PA.AxisID_A) >= 1 and int(PA.AxisID_A) <= 32:
        StringVar['A轴轴号'].set(str(int(PA.AxisID_A)))
    else:
        StringVar['A轴轴号'].set(str('无'))
    values = list(map(str, list(range(1, 33))))
    values.insert(0, '无')
    xBias += 0.07
    Combobox['AxisID_A'] = ttk.Combobox(LabelFrame['采样参数'], textvariable=StringVar['A轴轴号'], values=values, font=('Microsoft YaHei', 9), state='readonly')
    Combobox['AxisID_A'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.05)

    x += xStep
    y = 0
    xBias = 0.01
    yBias = 0.5
    Label['B轴轴号'] = ttk.Label(LabelFrame['采样参数'], text='B轴轴号：', anchor='w', font=('Microsoft YaHei', 9))
    Label['B轴轴号'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.1)
    StringVar['B轴轴号'] = tk.StringVar()
    if int(PA.AxisID_B) >= 1 and int(PA.AxisID_B) <= 32:
        StringVar['B轴轴号'].set(str(int(PA.AxisID_B)))
    else:
        StringVar['B轴轴号'].set(str('无'))
    values = list(map(str, list(range(1, 33))))
    values.insert(0, '无')
    xBias += 0.07
    Combobox['AxisID_B'] = ttk.Combobox(LabelFrame['采样参数'], textvariable=StringVar['B轴轴号'], values=values, font=('Microsoft YaHei', 9), state='readonly')
    Combobox['AxisID_B'].place(relx=x+xBias, rely=y+yBias, relheight=0.4, relwidth=0.05)

    ###################################### 绘图 #####################################
    Notebook['绘图'] = ttk.Notebook(window)
    Frame['绘图选项'] = ttk.Frame(Notebook['绘图'])
    Frame['自定义绘图'] = ttk.Frame(Notebook['绘图'])
    Notebook['绘图'].add(Frame['绘图选项'], text='绘图选项')
    Notebook['绘图'].add(Frame['自定义绘图'], text='自定义绘图')
    Notebook['绘图'].place(relx=0.02, rely=0.29, relheight=0.41, relwidth=0.95)
    
    #################################### 绘图选项 ####################################
    # ---------------------------------- 绘图选项1D ----------------------------------#
    x = 0
    y = 0
    LabelFrame['1D'] = ttk.LabelFrame(Frame['绘图选项'], text='1D')
    LabelFrame['1D'].place(relx=x + 0.01, rely=y + 0, relheight=0.96, relwidth=0.275)

    xBias = 0.02
    yBias = 0.11
    xStep = 0.09
    yStep = 0.1
    Key = 'BlockNo'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'PathVel'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'PathAcc'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'PathJerk'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'Pos_X'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'Vel_X'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'Acc_X'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'Jerk_X'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)

    xBias += xStep
    yBias = 0.11
    Key = 'Pos_Y'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'Vel_Y'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'Acc_Y'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'Jerk_Y'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'Pos_Z'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'Vel_Z'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'Acc_Z'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'Jerk_Z'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)

    xBias += xStep
    yBias = 0.11
    Key = 'Pos_A'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    yBias += yStep
    Key = 'Vel_A'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    yBias += yStep
    Key = 'Acc_A'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    yBias += yStep
    Key = 'Jerk_A'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    yBias += yStep
    Key = 'Pos_B'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    yBias += yStep
    Key = 'Vel_B'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    yBias += yStep
    Key = 'Acc_B'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    yBias += yStep
    Key = 'Jerk_B'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)

    # ---------------------------------- 绘图选项2D ----------------------------------#
    x = 0.296
    y = 0
    LabelFrame['2D'] = ttk.LabelFrame(Frame['绘图选项'], text='2D')
    LabelFrame['2D'].place(relx=x + 0.01, rely=y + 0, relheight=0.96, relwidth=0.385)

    xBias = 0.02
    yBias = 0.11
    xStep = 0.13
    yStep = 0.1
    Key = 'XY'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XY_Time'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XY_BlockNo'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XY_PathVel'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XY_PathAcc'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XY_PathJerk'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XY_PosErr'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XY_Z'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)

    xBias += xStep
    yBias = 0.11
    Key = 'YZ'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'YZ_Time'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'YZ_BlockNo'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'YZ_PathVel'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'YZ_PathAcc'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'YZ_PathJerk'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'YZ_PosErr'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'YZ_X'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)

    xBias += xStep
    yBias = 0.11
    Key = 'XZ'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XZ_Time'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XZ_BlockNo'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XZ_PathVel'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XZ_PathAcc'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XZ_PathJerk'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XZ_PosErr'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XZ_Y'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)

    # ---------------------------------- 绘图选项3D ----------------------------------#
    x = 0.703
    y = 0
    LabelFrame['3D'] = ttk.LabelFrame(Frame['绘图选项'], text='3D')
    LabelFrame['3D'].place(relx=x + 0.01, rely=y + 0, relheight=0.96, relwidth=0.127)

    xBias = 0.02
    yBias = 0.11
    xStep = 0.11
    yStep = 0.1
    Key = 'XYZ'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XYZ_Time'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XYZ_Z'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XYZ_PathVel'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XYZ_PathAcc'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'XYZ_PathJerk'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.115)

    # ---------------------------------- 绘图选项Circle --------------------------------#
    x = 0.852
    y = 0
    LabelFrame['Circle'] = ttk.LabelFrame(Frame['绘图选项'], text='Circle')
    LabelFrame['Circle'].place(relx=x + 0.01, rely=y + 0, relheight=0.96, relwidth=0.127)

    xBias = 0.02
    yBias = 0.11
    xStep = 0.11
    yStep = 0.1
    Key = 'CircleErr_XY'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'CircleErr_YZ'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    yBias += yStep
    Key = 'CircleErr_XZ'
    CheckVar[Key] = tk.IntVar()
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    
    ################################## 自定义绘图 ##################################
    CheckVar['用户代码'] = tk.IntVar()
    CheckVar['用户代码'].set(True)
    CheckButton['用户代码'] = ttk.Checkbutton(Frame['自定义绘图'], text='使用以下代码（Python 3.8）：', variable=CheckVar['用户代码'], onvalue=True, offvalue=False)
    CheckButton['用户代码'].place(relx=0.02, rely=0.02, relheight=0.1, relwidth=0.5)
    ScrolledText['用户代码'] = scrolledtext.ScrolledText(Frame['自定义绘图'], font=('Consolas', 8))
    ScrolledText['用户代码'].place(relx=0.03, rely=0.15, relheight=0.8, relwidth=0.95)

    #################################### 输出消息 ##################################
    x = 0.05
    y = 0.75
    Button['绘制图形'] = ttk.Button(window, text="绘制图形", command=plot_data)
    Button['绘制图形'].place(relx=x + 0.8, rely=y, relheight=0.22, relwidth=0.1)
    LabelFrame['输出消息'] = ttk.LabelFrame(window, text='输出消息')
    LabelFrame['输出消息'].place(relx=x - 0.03, rely=y - 0.04, relheight=0.28, relwidth=0.808)
    ScrolledText['输出消息'] = scrolledtext.ScrolledText(window, font=('Consolas', 8), relief='groove')
    ScrolledText['输出消息'].insert('end', 'PA Data Analyze v%s' % Version)
    ScrolledText['输出消息'].place(relx=x, rely=y, relheight=0.22, relwidth=0.76)

    window.mainloop()

##################################################################################
# -------------------------Example of external file use------------------------- #
##################################################################################
"""
PA = PA_Data_Analyze()

PA.DataFileName = r'D:\汇川\采样数据\20210717_迈盛达\象限痕数据集\F2000D55N620.txt'
PA.Ts = 0.001
PA.BlockRange = [620, 630]
PA.TimeRange = [12.447, 0]
PA.AxisID_X = 7
PA.AxisID_Y = 1
PA.AxisID_Z = 5

PA.LoadData()

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
PA.DataInfo()
#PA.DataInfo(PA.Data.Time, PA.Data.CmdPathVel, infoName=['Time(s)', 'F(mm/min)']) # You can also use it this way
PA.ShowFigure()
"""
