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
                SetPathVel                      Unit: mm/min
                CmdPathVel                      Unit: mm/min
                ActPathVel                      Unit: mm/min
                SetPathAcc                      Unit: m/s^2
                CmdPathAcc                      Unit: m/s^2
                ActPathAcc                      Unit: m/s^2
                SetPathJerk                     Unit: m/s^3
                CmdPathJerk                     Unit: m/s^3
                ActPathJerk                     Unit: m/s^3
                SetPos_X                        Unit: mm
                CmdPos_X                        Unit: mm
                ActPos_X                        Unit: mm
                SetVel_X                        Unit: mm/min
                CmdVel_X                        Unit: mm/min
                ActVel_X                        Unit: mm/min
                SetAcc_X                        Unit: m/s^2
                CmdAcc_X                        Unit: m/s^2
                ActAcc_X                        Unit: m/s^2
                SetJerk_X                       Unit: m/s^3
                CmdJerk_X                       Unit: m/s^3
                ActJerk_X                       Unit: m/s^3
"""

Version = '1.7.2'
################################ Version History ##################################
# ---------------------------------Version 1.7.2--------------------------------- #
# Date: 2021/9/27
# Author: yangxiaosheng
# Update: fix bug in saving user code that inclucing space
# ---------------------------------Version 1.7.1--------------------------------- #
# Date: 2021/9/27
# Author: yangxiaosheng
# Update: provide more options for drawing 1D and 2D figure
# ---------------------------------Version 1.7.0--------------------------------- #
# Date: 2021/9/24
# Author: yangxiaosheng
# Update: save GUI config parameters to ini file for parameters loading when starting
# ---------------------------------Version 1.6.4--------------------------------- #
# Date: 2021/9/22
# Author: yangxiaosheng
# Update: fix the bug in drawing figure
# ---------------------------------Version 1.6.3--------------------------------- #
# Date: 2021/9/13
# Author: yangxiaosheng
# Update: add color in activing check button
# ---------------------------------Version 1.6.2--------------------------------- #
# Date: 2021/9/13
# Author: yangxiaosheng
# Update: fix some bug in loading data
# ---------------------------------Version 1.6.1--------------------------------- #
# Date: 2021/9/12
# Author: yangxiaosheng
# Update: add error message in GUI
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
        
class PA_Data_Analyze:
    def __init__(self):
        self.initParam()
    
    def initParam(self):
        ##################################################################################
        # ----------------------------------User Define--------------------------------- #
        ##################################################################################
        self.Precision_um           = 1; # 1 internal incremental = Precision_um * 1um
        self.Ts                     = 0.001  # sample time, unit: s
        self.DataFileName           = r'C:\PACnc\CNCVariableTrace.txt'
        self.TimeRange              = [0, 0] # select the sample data in Time range of [minTime, maxTime] (unit: s) ([0, 0] means select all Time)
        self.BlockRange             = [0, 0] # select the sample data in NC Block range of [minBlockNo, maxBlockNo] ([0, 0] means select all NC Block)
        self.Plot                   = self.PlotFlag_Class()
        self.AxisID_X               = 0  # 0 means no axis,1 means the first axis
        self.AxisID_Y               = 0  # 0 means no axis,1 means the first axis
        self.AxisID_Z               = 0  # 0 means no axis,1 means the first axis
        self.AxisID_A               = 0  # 0 means no axis,1 means the first axis
        self.AxisID_B               = 0  # 0 means no axis,1 means the first axis

        ##################################################################################
        # -------------------------------Internal Param--------------------------------- #
        ##################################################################################
        self.FigNum                 = 0
        self.GuiText                = None
        self.DataInfoExist          = False
        self.Data                   = self.Data_Class()
        self.ShareAxis              = self.ShareAxis_Class()
        self.reSplit                = re.compile("[\t\n ,]")
        self.reMatch                = re.compile("[-+0-9Ee\\.]*")
        self.DataName_SetPos        = 'SSetPos[%d]'
        self.DataName_CmdPos        = 'CommandedMachinePosCorr[%d]'
        self.DataName_ActPos        = 'SActMachinePos[%d]'
        self.DataName_SetPathVel    = 'PathVelocity[0]'
        self.DataName_CmdPathVel    = 'CommandedPathVelocity[0]'
        self.DataName_BlockNo       = 'BlockNoActive[0]'

    class Data_Class:
        Length          = 0
        Var             = dict()
        Time            = []
        BlockNo         = []
        SetPathVel      = []
        CmdPathVel      = []
        ActPathVel      = []
        SetPathAcc      = []
        CmdPathAcc      = []
        ActPathAcc      = []
        SetPathJerk     = []
        CmdPathJerk     = []
        ActPathJerk     = []
        SetPos_X        = []
        CmdPos_X        = []
        ActPos_X        = []
        SetVel_X        = []
        CmdVel_X        = []
        ActVel_X        = []
        SetAcc_X        = []
        CmdAcc_X        = []
        ActAcc_X        = []
        SetJerk_X       = []
        CmdJerk_X       = []
        ActJerk_X       = []
        SetPos_Y        = []
        CmdPos_Y        = []
        ActPos_Y        = []
        SetVel_Y        = []
        CmdVel_Y        = []
        ActVel_Y        = []
        SetAcc_Y        = []
        CmdAcc_Y        = []
        ActAcc_Y        = []
        SetJerk_Y       = []
        CmdJerk_Y       = []
        ActJerk_Y       = []
        SetPos_Z        = []
        CmdPos_Z        = []
        ActPos_Z        = []
        SetVel_Z        = []
        CmdVel_Z        = []
        ActVel_Z        = []
        SetAcc_Z        = []
        CmdAcc_Z        = []
        ActAcc_Z        = []
        SetJerk_Z       = []
        CmdJerk_Z       = []
        ActJerk_Z       = []
        SetPos_A        = []
        CmdPos_A        = []
        ActPos_A        = []
        SetVel_A        = []
        CmdVel_A        = []
        ActVel_A        = []
        SetAcc_A        = []
        CmdAcc_A        = []
        ActAcc_A        = []
        SetJerk_A       = []
        CmdJerk_A       = []
        ActJerk_A       = []
        SetPos_B        = []
        CmdPos_B        = []
        ActPos_B        = []
        SetVel_B        = []
        CmdVel_B        = []
        ActVel_B        = []
        SetAcc_B        = []
        CmdAcc_B        = []
        ActAcc_B        = []
        SetJerk_B       = []
        CmdJerk_B       = []
        ActJerk_B       = []
        PosErr          = []

    class ShareAxis_Class:
        Time            = None
        XY              = None
        YZ              = None
        XZ              = None

    class PlotFlag_Class:
        paramName = [
            'BlockNo', 
            'PathVel', 'PathAcc', 'PathJerk',
            'Pos_X', 'Vel_X', 'Acc_X', 'Jerk_X',
            'Pos_Y', 'Vel_Y', 'Acc_Y', 'Jerk_Y',
            'Pos_Z', 'Vel_Z', 'Acc_Z', 'Jerk_Z',
            'Pos_A', 'Vel_A', 'Acc_A', 'Jerk_A',
            'Pos_B', 'Vel_B', 'Acc_B', 'Jerk_B',
            'XY', 'XY_Time', 'XY_BlockNo', 'XY_PathVel', 'XY_PathAcc', 'XY_PathJerk', 'XY_PosErr', 'XY_Z',
            'YZ', 'YZ_Time', 'YZ_BlockNo', 'YZ_PathVel', 'YZ_PathAcc', 'YZ_PathJerk', 'YZ_PosErr', 'YZ_X',
            'XZ', 'XZ_Time', 'XZ_BlockNo', 'XZ_PathVel', 'XZ_PathAcc', 'XZ_PathJerk', 'XZ_PosErr', 'XZ_Y',
            'XYZ', 'XYZ_Time', 'XYZ_Z', 'XYZ_PathVel', 'XYZ_PathAcc', 'XYZ_PathJerk', 
            'CircleErr_XY', 'CircleErr_YZ', 'CircleErr_XZ',
            'Plot1D_ShowActPathVel', 'Plot1D_ShowActPathAcc', 'Plot1D_ShowActPathJerk',
            'Plot1D_ShowActAxisVel', 'Plot1D_ShowActAxisAcc', 'Plot1D_ShowActAxisJerk',
            'Plot2D_PathVelType', 'Plot2D_PathAccType', 'Plot2D_PathJerkType',
            'Plot2D_AbsPathVel', 'Plot2D_AbsPathAcc', 'Plot2D_AbsPathJerk',
            'Plot2D_EqualScale'
            ]
        def __init__(self):
            for name in self.paramName:
                setattr(self, name, False)
            self.Plot1D_ShowActPathVel  = True
            self.Plot1D_ShowActPathAcc  = False
            self.Plot1D_ShowActPathJerk = False
            self.Plot1D_ShowActAxisVel  = True
            self.Plot1D_ShowActAxisAcc  = True
            self.Plot1D_ShowActAxisJerk = False
            self.Plot2D_PathVelType     = 'Cmd' # 'Set' or 'Cmd' or 'Act'
            self.Plot2D_PathAccType     = 'Cmd'
            self.Plot2D_PathJerkType    = 'Cmd'
            self.Plot2D_AbsPathVel      = False
            self.Plot2D_AbsPathAcc      = True
            self.Plot2D_AbsPathJerk     = True
            self.Plot2D_EqualScale      = False

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
        self.ShareAxis.Time = None
        self.ShareAxis.XY   = None
        self.ShareAxis.YZ   = None
        self.ShareAxis.XZ   = None
        self.DataInfoExist  = False
            
        # ---------------------------------Plot 1D---------------------------------- #
        # BlockNo
        if self.Plot.BlockNo == True:
            try:
                block = self.Data.BlockNo
                self.Plot1D(block, dataName='BlockNo', shareAxis='time', title='BlockNo', newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError BlockNo: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error BlockNo: %s' % str(e))

        # PathVel
        if self.Plot.PathVel == True:
            try:
                self.Plot1D(self.Data.SetPathVel, axisName_1='Vel (mm/min)', dataName='SetPathVel', shareAxis='time', title='PathVel', newFigure=True)
                self.Plot1D(self.Data.CmdPathVel, axisName_1='Vel (mm/min)', dataName='CmdPathVel', shareAxis='time', title='PathVel', newFigure=False)
                if self.Plot.Plot1D_ShowActPathVel == True and self.Data.ActPathVel.__len__() != 0:
                    self.Plot1D(self.Data.ActPathVel, axisName_1='Vel (mm/min)', dataName='ActPathVel', shareAxis='time', title='PathVel', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError PathVel: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error PathVel: %s' % str(e))

        # PathAcc
        if self.Plot.PathAcc == True:
            try:
                self.Plot1D(self.Data.SetPathAcc, axisName_1='Acc (m/s^2)', dataName='SetPathAcc', shareAxis='time', title='PathAcc', newFigure=True)
                self.Plot1D(self.Data.CmdPathAcc, axisName_1='Acc (m/s^2)', dataName='CmdPathAcc', shareAxis='time', title='PathAcc', newFigure=False)
                if self.Plot.Plot1D_ShowActPathAcc == True and self.Data.ActPathAcc.__len__() != 0:
                    self.Plot1D(self.Data.ActPathAcc, axisName_1='Acc (m/s^2)', dataName='ActPathAcc', shareAxis='time', title='PathAcc', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError PathAcc: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error PathAcc: %s' % str(e))

        # PathJerk
        if self.Plot.PathJerk == True:
            try:
                self.Plot1D(self.Data.SetPathJerk, axisName_1='Jerk (m/s^3)', dataName='SetPathJerk', shareAxis='time', title='PathJerk', newFigure=True)
                self.Plot1D(self.Data.CmdPathJerk, axisName_1='Jerk (m/s^3)', dataName='CmdPathJerk', shareAxis='time', title='PathJerk', newFigure=False)
                if self.Plot.Plot1D_ShowActPathJerk == True and self.Data.ActPathJerk.__len__() != 0:
                    self.Plot1D(self.Data.ActPathJerk, axisName_1='Jerk (m/s^3)', dataName='ActPathJerk', shareAxis='time', title='PathJerk', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError PathJerk: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error PathJerk: %s' % str(e))

        # X
        # Pos_X
        if self.Plot.Pos_X == True:
            try:
                self.Plot1D(self.Data.SetPos_X, axisName_1='Pos (mm)', dataName='SetPos_X', shareAxis='time', title='Pos_X', newFigure=True)
                self.Plot1D(self.Data.CmdPos_X, axisName_1='Pos (mm)', dataName='CmdPos_X', shareAxis='time', title='Pos_X', newFigure=False)
                self.Plot1D(self.Data.ActPos_X, axisName_1='Pos (mm)', dataName='ActPos_X', shareAxis='time', title='Pos_X', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Pos_X: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Pos_X: %s' % str(e))
        # Vel_X
        if self.Plot.Vel_X == True:
            try:
                self.Plot1D(self.Data.SetVel_X, axisName_1='Vel (mm/min)', dataName='SetVel_X', shareAxis='time', title='Vel_X', newFigure=True)
                self.Plot1D(self.Data.CmdVel_X, axisName_1='Vel (mm/min)', dataName='CmdVel_X', shareAxis='time', title='Vel_X', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisVel == True:
                    self.Plot1D(self.Data.ActVel_X, axisName_1='Vel (mm/min)', dataName='ActVel_X', shareAxis='time', title='Vel_X', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Vel_X: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Vel_X: %s' % str(e))
        # Acc_X
        if self.Plot.Acc_X == True:
            try:
                self.Plot1D(self.Data.SetAcc_X, axisName_1='Acc (m/s^2)', dataName='SetAcc_X', shareAxis='time', title='Acc_X', newFigure=True)
                self.Plot1D(self.Data.CmdAcc_X, axisName_1='Acc (m/s^2)', dataName='CmdAcc_X', shareAxis='time', title='Acc_X', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisAcc == True:
                    self.Plot1D(self.Data.ActAcc_X, axisName_1='Acc (m/s^2)', dataName='ActAcc_X', shareAxis='time', title='Acc_X', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Acc_X: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Acc_X: %s' % str(e))
        # Jerk_X
        if self.Plot.Jerk_X == True:
            try:
                self.Plot1D(self.Data.SetJerk_X, axisName_1='Jerk (m/s^3)', dataName='SetJerk_X', shareAxis='time', title='Jerk_X', newFigure=True)
                self.Plot1D(self.Data.CmdJerk_X, axisName_1='Jerk (m/s^3)', dataName='CmdJerk_X', shareAxis='time', title='Jerk_X', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisJerk == True:
                    self.Plot1D(self.Data.ActJerk_X, axisName_1='Jerk (m/s^3)', dataName='ActJerk_X', shareAxis='time', title='Jerk_X', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Jerk_X: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Jerk_X: %s' % str(e))

        # Y
        # Pos_Y
        if self.Plot.Pos_Y == True:
            try:
                self.Plot1D(self.Data.SetPos_Y, axisName_1='Pos (mm)', dataName='SetPos_Y', shareAxis='time', title='Pos_Y', newFigure=True)
                self.Plot1D(self.Data.CmdPos_Y, axisName_1='Pos (mm)', dataName='CmdPos_Y', shareAxis='time', title='Pos_Y', newFigure=False)
                self.Plot1D(self.Data.ActPos_Y, axisName_1='Pos (mm)', dataName='ActPos_Y', shareAxis='time', title='Pos_Y', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Pos_Y: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Pos_Y: %s' % str(e))
        # Vel_Y
        if self.Plot.Vel_Y == True:
            try:
                self.Plot1D(self.Data.SetVel_Y, axisName_1='Vel (mm/min)', dataName='SetVel_Y', shareAxis='time', title='Vel_Y', newFigure=True)
                self.Plot1D(self.Data.CmdVel_Y, axisName_1='Vel (mm/min)', dataName='CmdVel_Y', shareAxis='time', title='Vel_Y', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisVel == True:
                    self.Plot1D(self.Data.ActVel_Y, axisName_1='Vel (mm/min)', dataName='ActVel_Y', shareAxis='time', title='Vel_Y', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Vel_Y: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Vel_Y: %s' % str(e))
        # Acc_Y
        if self.Plot.Acc_Y == True:
            try:
                self.Plot1D(self.Data.SetAcc_Y, axisName_1='Acc (m/s^2)', dataName='SetAcc_Y', shareAxis='time', title='Acc_Y', newFigure=True)
                self.Plot1D(self.Data.CmdAcc_Y, axisName_1='Acc (m/s^2)', dataName='CmdAcc_Y', shareAxis='time', title='Acc_Y', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisAcc == True:
                    self.Plot1D(self.Data.ActAcc_Y, axisName_1='Acc (m/s^2)', dataName='ActAcc_Y', shareAxis='time', title='Acc_Y', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Acc_Y: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Acc_Y: %s' % str(e))
        # Jerk_Y
        if self.Plot.Jerk_Y == True:
            try:
                self.Plot1D(self.Data.SetJerk_Y, axisName_1='Jerk (m/s^3)', dataName='SetJerk_Y', shareAxis='time', title='Jerk_Y', newFigure=True)
                self.Plot1D(self.Data.CmdJerk_Y, axisName_1='Jerk (m/s^3)', dataName='CmdJerk_Y', shareAxis='time', title='Jerk_Y', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisJerk == True:
                    self.Plot1D(self.Data.ActJerk_Y, axisName_1='Jerk (m/s^3)', dataName='ActJerk_Y', shareAxis='time', title='Jerk_Y', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Jerk_Y: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Jerk_Y: %s' % str(e))

        # Z
        #Pos_Z
        if self.Plot.Pos_Z == True:
            try:
                self.Plot1D(self.Data.SetPos_Z, axisName_1='Pos (mm)', dataName='SetPos_Z', shareAxis='time', title='Pos_Z', newFigure=True)
                self.Plot1D(self.Data.CmdPos_Z, axisName_1='Pos (mm)', dataName='CmdPos_Z', shareAxis='time', title='Pos_Z', newFigure=False)
                self.Plot1D(self.Data.ActPos_Z, axisName_1='Pos (mm)', dataName='ActPos_Z', shareAxis='time', title='Pos_Z', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Pos_Z: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Pos_Z: %s' % str(e))
        #Vel_Z
        if self.Plot.Vel_Z == True:
            try:
                self.Plot1D(self.Data.SetVel_Z, axisName_1='Vel (mm/min)', dataName='SetVel_Z', shareAxis='time', title='Vel_Z', newFigure=True)
                self.Plot1D(self.Data.CmdVel_Z, axisName_1='Vel (mm/min)', dataName='CmdVel_Z', shareAxis='time', title='Vel_Z', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisVel == True:
                    self.Plot1D(self.Data.ActVel_Z, axisName_1='Vel (mm/min)', dataName='ActVel_Z', shareAxis='time', title='Vel_Z', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Vel_Z: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Vel_Z: %s' % str(e))
        #Acc_Z
        if self.Plot.Acc_Z == True:
            try:
                self.Plot1D(self.Data.SetAcc_Z, axisName_1='Acc (m/s^2)', dataName='SetAcc_Z', shareAxis='time', title='Acc_Z', newFigure=True)
                self.Plot1D(self.Data.CmdAcc_Z, axisName_1='Acc (m/s^2)', dataName='CmdAcc_Z', shareAxis='time', title='Acc_Z', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisAcc == True:
                    self.Plot1D(self.Data.ActAcc_Z, axisName_1='Acc (m/s^2)', dataName='ActAcc_Z', shareAxis='time', title='Acc_Z', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Acc_Z: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Acc_Z: %s' % str(e))
        # Jerk_Z
        if self.Plot.Jerk_Z == True:
            try:
                self.Plot1D(self.Data.SetJerk_Z, axisName_1='Jerk (m/s^3)', dataName='SetJerk_Z', shareAxis='time', title='Jerk_Z', newFigure=True)
                self.Plot1D(self.Data.CmdJerk_Z, axisName_1='Jerk (m/s^3)', dataName='CmdJerk_Z', shareAxis='time', title='Jerk_Z', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisJerk == True:
                    self.Plot1D(self.Data.ActJerk_Z, axisName_1='Jerk (m/s^3)', dataName='ActJerk_Z', shareAxis='time', title='Jerk_Z', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Jerk_Z: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Jerk_Z: %s' % str(e))

        # A
        #Pos_A
        if self.Plot.Pos_A == True:
            try:
                self.Plot1D(self.Data.SetPos_A, axisName_1='Pos (mm)', dataName='SetPos_A', shareAxis='time', title='Pos_A', newFigure=True)
                self.Plot1D(self.Data.CmdPos_A, axisName_1='Pos (mm)', dataName='CmdPos_A', shareAxis='time', title='Pos_A', newFigure=False)
                self.Plot1D(self.Data.ActPos_A, axisName_1='Pos (mm)', dataName='ActPos_A', shareAxis='time', title='Pos_A', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Pos_A: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Pos_A: %s' % str(e))
        #Vel_A
        if self.Plot.Vel_A == True:
            try:
                self.Plot1D(self.Data.SetVel_A, axisName_1='Vel (mm/min)', dataName='SetVel_A', shareAxis='time', title='Vel_A', newFigure=True)
                self.Plot1D(self.Data.CmdVel_A, axisName_1='Vel (mm/min)', dataName='CmdVel_A', shareAxis='time', title='Vel_A', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisVel == True:
                    self.Plot1D(self.Data.ActVel_A, axisName_1='Vel (mm/min)', dataName='ActVel_A', shareAxis='time', title='Vel_A', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Vel_A: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Vel_A: %s' % str(e))
        #Acc_A
        if self.Plot.Acc_A == True:
            try:
                self.Plot1D(self.Data.SetAcc_A, axisName_1='Acc (m/s^2)', dataName='SetAcc_A', shareAxis='time', title='Acc_A', newFigure=True)
                self.Plot1D(self.Data.CmdAcc_A, axisName_1='Acc (m/s^2)', dataName='CmdAcc_A', shareAxis='time', title='Acc_A', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisAcc == True:
                    self.Plot1D(self.Data.ActAcc_A, axisName_1='Acc (m/s^2)', dataName='ActAcc_A', shareAxis='time', title='Acc_A', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Acc_A: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Acc_A: %s' % str(e))
        # Jerk_A
        if self.Plot.Jerk_A == True:
            try:
                self.Plot1D(self.Data.SetJerk_A, axisName_1='Jerk (m/s^3)', dataName='SetJerk_A', shareAxis='time', title='Jerk_A', newFigure=True)
                self.Plot1D(self.Data.CmdJerk_A, axisName_1='Jerk (m/s^3)', dataName='CmdJerk_A', shareAxis='time', title='Jerk_A', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisJerk == True:
                    self.Plot1D(self.Data.ActJerk_A, axisName_1='Jerk (m/s^3)', dataName='ActJerk_A', shareAxis='time', title='Jerk_A', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Jerk_A: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Jerk_A: %s' % str(e))

        # B
        #Pos_B
        if self.Plot.Pos_B == True:
            try:
                self.Plot1D(self.Data.SetPos_B, axisName_1='Pos (mm)', dataName='SetPos_B', shareAxis='time', title='Pos_B', newFigure=True)
                self.Plot1D(self.Data.CmdPos_B, axisName_1='Pos (mm)', dataName='CmdPos_B', shareAxis='time', title='Pos_B', newFigure=False)
                self.Plot1D(self.Data.ActPos_B, axisName_1='Pos (mm)', dataName='ActPos_B', shareAxis='time', title='Pos_B', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Pos_B: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Pos_B: %s' % str(e))
        #Vel_B
        if self.Plot.Vel_B == True:
            try:
                self.Plot1D(self.Data.SetVel_B, axisName_1='Vel (mm/min)', dataName='SetVel_B', shareAxis='time', title='Vel_B', newFigure=True)
                self.Plot1D(self.Data.CmdVel_B, axisName_1='Vel (mm/min)', dataName='CmdVel_B', shareAxis='time', title='Vel_B', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisVel == True:
                    self.Plot1D(self.Data.ActVel_B, axisName_1='Vel (mm/min)', dataName='ActVel_B', shareAxis='time', title='Vel_B', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Vel_B: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Vel_B: %s' % str(e))
        #Acc_B
        if self.Plot.Acc_B == True:
            try:
                self.Plot1D(self.Data.SetAcc_B, axisName_1='Acc (m/s^2)', dataName='SetAcc_B', shareAxis='time', title='Acc_B', newFigure=True)
                self.Plot1D(self.Data.CmdAcc_B, axisName_1='Acc (m/s^2)', dataName='CmdAcc_B', shareAxis='time', title='Acc_B', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisAcc == True:
                    self.Plot1D(self.Data.ActAcc_B, axisName_1='Acc (m/s^2)', dataName='ActAcc_B', shareAxis='time', title='Acc_B', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Acc_B: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Acc_B: %s' % str(e))
        # Jerk_B
        if self.Plot.Jerk_B == True:
            try:
                self.Plot1D(self.Data.SetJerk_B, axisName_1='Jerk (m/s^3)', dataName='SetJerk_B', shareAxis='time', title='Jerk_B', newFigure=True)
                self.Plot1D(self.Data.CmdJerk_B, axisName_1='Jerk (m/s^3)', dataName='CmdJerk_B', shareAxis='time', title='Jerk_B', newFigure=False)
                if self.Plot.Plot1D_ShowActAxisJerk == True:
                    self.Plot1D(self.Data.ActJerk_B, axisName_1='Jerk (m/s^3)', dataName='ActJerk_B', shareAxis='time', title='Jerk_B', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError Jerk_B: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error Jerk_B: %s' % str(e))

        # ---------------------------------Plot 2D---------------------------------- #
        equalScale = True if self.Plot.Plot2D_EqualScale == True else False
        # XY
        if self.Plot.XY == True:
            try:
                self.Plot2D(self.Data.SetPos_X, self.Data.SetPos_Y, axisName_1='X (mm)', axisName_2='Y (mm)', dataName='SetPos', shareAxis='xy', title='XY', equalScale=equalScale, newFigure=True)
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, axisName_1='X (mm)', axisName_2='Y (mm)', dataName='CmdPos', shareAxis='xy', title='XY', equalScale=equalScale, newFigure=False)
                self.Plot2D(self.Data.ActPos_X, self.Data.ActPos_Y, axisName_1='X (mm)', axisName_2='Y (mm)', dataName='ActPos', shareAxis='xy', title='XY', equalScale=equalScale, newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XY: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XY: %s' % str(e))
        # XY with BlockNo
        if self.Plot.XY_BlockNo == True:
            try:
                color = self.Data.BlockNo
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='BlockNo', shareAxis='xy', title='XY_BlockNo', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError BlockNo: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error BlockNo: %s' % str(e))
        # XY with Time
        if self.Plot.XY_Time == True:
            try:
                color = self.Data.Time
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='Time (s)', shareAxis='xy', title='XY_Time', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_Time: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XY_Time: %s' % str(e))
        #XY with PathVel
        if self.Plot.XY_PathVel == True:
            try:
                if self.Plot.Plot2D_PathVelType == 'Set':
                    color = self.Data.SetPathVel
                    name = 'SetPathVel'
                elif self.Plot.Plot2D_PathVelType == 'Cmd':
                    color = self.Data.CmdPathVel
                    name = 'CmdPathVel'
                elif self.Plot.Plot2D_PathVelType == 'Act':
                    color = self.Data.ActPathVel
                    name = 'ActPathVel'
                else:
                    color = self.Data.CmdPathVel
                    name = 'CmdPathVel'
                if self.Plot.Plot2D_AbsPathVel == True:
                    color = np.abs(color)
                    colorName = 'Abs(%s) (mm/min)' % name
                else:
                    colorName = '%s (mm/min)' % name
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName=colorName, shareAxis='xy', title='XY_PathVel', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_PathVel: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XY_PathVel: %s' % str(e))
        #XY with PathAcc
        if self.Plot.XY_PathAcc == True:
            try:
                if self.Plot.Plot2D_PathAccType == 'Set':
                    color = self.Data.SetPathAcc
                    name = 'SetPathAcc'
                elif self.Plot.Plot2D_PathAccType == 'Cmd':
                    color = self.Data.CmdPathAcc
                    name = 'CmdPathAcc'
                elif self.Plot.Plot2D_PathAccType == 'Act':
                    color = self.Data.ActPathAcc
                    name = 'ActPathAcc'
                else:
                    color = self.Data.CmdPathAcc
                    name = 'CmdPathAcc'
                if self.Plot.Plot2D_AbsPathAcc == True:
                    color = np.abs(color)
                    colorName = 'Abs(%s) ((m/s^2)' % name
                else:
                    colorName = '%s ((m/s^2)' % name
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName=colorName, shareAxis='xy', title='XY_PathAcc', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_PathAcc: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XY_PathAcc: %s' % str(e))
        #XY with PathJerk
        if self.Plot.XY_PathJerk == True:
            try:
                if self.Plot.Plot2D_PathJerkType == 'Set':
                    color = self.Data.SetPathJerk
                    name = 'SetPathJerk'
                elif self.Plot.Plot2D_PathJerkType == 'Cmd':
                    color = self.Data.CmdPathJerk
                    name = 'CmdPathJerk'
                elif self.Plot.Plot2D_PathJerkType == 'Act':
                    color = self.Data.ActPathJerk
                    name = 'ActPathJerk'
                else:
                    color = self.Data.CmdPathJerk
                    name = 'CmdPathJerk'
                if self.Plot.Plot2D_AbsPathJerk == True:
                    color = np.abs(color)
                    colorName = 'Abs(%s) ((m/s^3)' % name
                else:
                    colorName = '%s ((m/s^3)' % name
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName=colorName, shareAxis='xy', title='XY_PathJerk', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_PathJerk: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XY_PathJerk: %s' % str(e))
        #XY with PosErr
        if self.Plot.XY_PosErr == True:
            try:
                if self.Data.PosErr.__len__() != 0:
                    color = self.Data.PosErr
                    self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='PosErr (mm)', shareAxis='xy', title='XY_PosErr', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_PosErr: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XY_PosErr: %s' % str(e))
        #XY with Z
        if self.Plot.XY_Z == True:
            try:
                color = self.Data.CmdPos_Z
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Y, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', colorName='Z (mm)', shareAxis='xy', title='XY_Z', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XY_Z: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XY_Z: %s' % str(e))
        
        # YZ
        if self.Plot.YZ == True:
            try:
                self.Plot2D(self.Data.SetPos_Y, self.Data.SetPos_Z, axisName_1='Y (mm)', axisName_2='Z (mm)', dataName='SetPos', shareAxis='yz', title='YZ', equalScale=equalScale, newFigure=True)
                self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, axisName_1='Y (mm)', axisName_2='Z (mm)', dataName='CmdPos', shareAxis='yz', title='YZ', equalScale=equalScale, newFigure=False)
                self.Plot2D(self.Data.ActPos_Y, self.Data.ActPos_Z, axisName_1='Y (mm)', axisName_2='Z (mm)', dataName='ActPos', shareAxis='yz', title='YZ', equalScale=equalScale, newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error YZ: %s' % str(e))
        # YZ with BlockNo
        if self.Plot.YZ_BlockNo == True:
            try:
                color = self.Data.BlockNo
                self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='BlockNo', shareAxis='yz', title='YZ_BlockNo', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_BlockNo: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error YZ_BlockNo: %s' % str(e))
        # YZ with Time
        if self.Plot.YZ_Time == True:
            try:
                color = self.Data.Time
                self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='Time (s)', shareAxis='yz', title='YZ_Time', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_Time: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error YZ_Time: %s' % str(e))
        #YZ with PathVel
        if self.Plot.YZ_PathVel == True:
            try:
                if self.Plot.Plot2D_PathVelType == 'Set':
                    color = self.Data.SetPathVel
                    name = 'SetPathVel'
                elif self.Plot.Plot2D_PathVelType == 'Cmd':
                    color = self.Data.CmdPathVel
                    name = 'CmdPathVel'
                elif self.Plot.Plot2D_PathVelType == 'Act':
                    color = self.Data.ActPathVel
                    name = 'ActPathVel'
                else:
                    color = self.Data.CmdPathVel
                if self.Plot.Plot2D_AbsPathVel == True:
                    color = np.abs(color)
                    colorName = 'Abs(%s) (mm/min)' % name
                else:
                    colorName = '%s (mm/min)' % name
                    name = 'CmdPathVel'
                self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName=colorName, shareAxis='yz', title='YZ_PathVel', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_PathVel: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error YZ_PathVel: %s' % str(e))
        #YZ with PathAcc
        if self.Plot.YZ_PathAcc == True:
            try:
                if self.Plot.Plot2D_PathAccType == 'Set':
                    color = self.Data.SetPathAcc
                    name = 'SetPathAcc'
                elif self.Plot.Plot2D_PathAccType == 'Cmd':
                    color = self.Data.CmdPathAcc
                    name = 'CmdPathAcc'
                elif self.Plot.Plot2D_PathAccType == 'Act':
                    color = self.Data.ActPathAcc
                    name = 'ActPathAcc'
                else:
                    color = self.Data.CmdPathAcc
                    name = 'CmdPathAcc'
                if self.Plot.Plot2D_AbsPathAcc == True:
                    color = np.abs(color)
                    colorName = 'Abs(%s) ((m/s^2)' % name
                else:
                    colorName = '%s ((m/s^2)' % name
                self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName=colorName, shareAxis='yz', title='YZ_PathAcc', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_PathAcc: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error YZ_PathAcc: %s' % str(e))
        #YZ with PathJerk
        if self.Plot.YZ_PathJerk == True:
            try:
                if self.Plot.Plot2D_PathJerkType == 'Set':
                    color = self.Data.SetPathJerk
                    name = 'SetPathJerk'
                elif self.Plot.Plot2D_PathJerkType == 'Cmd':
                    color = self.Data.CmdPathJerk
                    name = 'CmdPathJerk'
                elif self.Plot.Plot2D_PathJerkType == 'Act':
                    color = self.Data.ActPathJerk
                    name = 'ActPathJerk'
                else:
                    color = self.Data.CmdPathJerk
                    name = 'CmdPathJerk'
                if self.Plot.Plot2D_AbsPathJerk == True:
                    color = np.abs(color)
                    colorName = 'Abs(%s) ((m/s^3)' % name
                else:
                    colorName = '%s ((m/s^3)' % name
                self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName=colorName, shareAxis='yz', title='YZ_PathJerk', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_PathJerk: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error YZ_PathJerk: %s' % str(e))
        #YZ with PosErr
        if self.Plot.YZ_PosErr == True:
            try:
                if self.Data.PosErr.__len__() != 0:
                    color = self.Data.PosErr
                    self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='PosErr (mm)', shareAxis='yz', title='YZ_PosErr', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_PosErr: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error YZ_PosErr: %s' % str(e))
        #YZ with X
        if self.Plot.YZ_X == True:
            try:
                color = self.Data.CmdPos_X
                self.Plot2D(self.Data.CmdPos_Y, self.Data.CmdPos_Z, color=color, axisName_1='Y (mm)', axisName_2='Z (mm)', colorName='X (mm)', shareAxis='yz', title='YZ_X', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError YZ_X: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error YZ_X: %s' % str(e))

        # XZ
        if self.Plot.XZ == True:
            try:
                self.Plot2D(self.Data.SetPos_X, self.Data.SetPos_Z, axisName_1='X (mm)', axisName_2='Z (mm)', dataName='SetPos', shareAxis='xz', title='XZ', equalScale=equalScale, newFigure=True)
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, axisName_1='X (mm)', axisName_2='Z (mm)', dataName='CmdPos', shareAxis='xz', title='XZ', equalScale=equalScale, newFigure=False)
                self.Plot2D(self.Data.ActPos_X, self.Data.ActPos_Z, axisName_1='X (mm)', axisName_2='Z (mm)', dataName='ActPos', shareAxis='xz', title='XZ', equalScale=equalScale, newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XZ: %s' % str(e))
        # XZ with BlockNo
        if self.Plot.XZ_BlockNo == True:
            try:
                color = self.Data.BlockNo
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='BlockNo', shareAxis='xz', title='XZ_BlockNo', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_BlockNo: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XZ_BlockNo: %s' % str(e))
        # XZ with Time
        if self.Plot.XZ_Time == True:
            try:
                color = self.Data.Time
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='Time (s)', shareAxis='xz', title='XZ_Time', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_Time: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XZ_Time: %s' % str(e))
        #XZ with PathVel
        if self.Plot.XZ_PathVel == True:
            try:
                if self.Plot.Plot2D_PathVelType == 'Set':
                    color = self.Data.SetPathVel
                    name = 'SetPathVel'
                elif self.Plot.Plot2D_PathVelType == 'Cmd':
                    color = self.Data.CmdPathVel
                    name = 'CmdPathVel'
                elif self.Plot.Plot2D_PathVelType == 'Act':
                    color = self.Data.ActPathVel
                    name = 'ActPathVel'
                else:
                    color = self.Data.CmdPathVel
                    name = 'CmdPathVel'
                if self.Plot.Plot2D_AbsPathVel == True:
                    color = np.abs(color)
                    colorName = 'Abs(%s) (mm/min)' % name
                else:
                    colorName = '%s (mm/min)' % name
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName=colorName, shareAxis='xz', title='XZ_PathVel', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_PathVel: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XZ_PathVel: %s' % str(e))
        #XZ with PathAcc
        if self.Plot.XZ_PathAcc == True:
            try:
                if self.Plot.Plot2D_PathAccType == 'Set':
                    color = self.Data.SetPathAcc
                    name = 'SetPathAcc'
                elif self.Plot.Plot2D_PathAccType == 'Cmd':
                    color = self.Data.CmdPathAcc
                    name = 'CmdPathAcc'
                elif self.Plot.Plot2D_PathAccType == 'Act':
                    color = self.Data.ActPathAcc
                    name = 'ActPathAcc'
                else:
                    color = self.Data.CmdPathAcc
                    name = 'CmdPathAcc'
                if self.Plot.Plot2D_AbsPathAcc == True:
                    color = np.abs(color)
                    colorName = 'Abs(%s) ((m/s^2)' % name
                else:
                    colorName = '%s ((m/s^2)' % name
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName=colorName, shareAxis='xz', title='XZ_PathAcc', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_PathAcc: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XZ_PathAcc: %s' % str(e))
        #XZ with PathJerk
        if self.Plot.XZ_PathJerk == True:
            try:
                if self.Plot.Plot2D_PathJerkType == 'Set':
                    color = self.Data.SetPathJerk
                    name = 'SetPathJerk'
                elif self.Plot.Plot2D_PathJerkType == 'Cmd':
                    color = self.Data.CmdPathJerk
                    name = 'CmdPathJerk'
                elif self.Plot.Plot2D_PathJerkType == 'Act':
                    color = self.Data.ActPathJerk
                    name = 'ActPathJerk'
                else:
                    color = self.Data.CmdPathJerk
                    name = 'CmdPathJerk'
                if self.Plot.Plot2D_AbsPathJerk == True:
                    color = np.abs(color)
                    colorName = 'Abs(%s) ((m/s^3)' % name
                else:
                    colorName = '%s ((m/s^3)' % name
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName=colorName, shareAxis='xz', title='XZ_PathJerk', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_PathJerk: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XZ_PathJerk: %s' % str(e))
        #XZ with PosErr
        if self.Plot.XZ_PosErr == True:
            try:
                if self.Data.PosErr.__len__() != 0:
                    color = self.Data.PosErr
                    self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='PosErr (mm)', shareAxis='xz', title='XZ_PosErr', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_PosErr: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XZ_PosErr: %s' % str(e))
        #XZ with Y
        if self.Plot.XZ_Y == True:
            try:
                color = self.Data.CmdPos_Y
                self.Plot2D(self.Data.CmdPos_X, self.Data.CmdPos_Z, color=color, axisName_1='X (mm)', axisName_2='Z (mm)', colorName='Y (mm)', shareAxis='xz', title='XZ_Y', equalScale=equalScale, newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XZ_Y: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XZ_Y: %s' % str(e))

        # ---------------------------------Plot 3D---------------------------------- #
        #XYZ
        if self.Plot.XYZ == True:
            try:
                self.Plot3D(self.Data.SetPos_X, self.Data.SetPos_Y, self.Data.SetPos_Z, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', dataName='SetPos', title='XYZ', newFigure=True)
                self.Plot3D(self.Data.CmdPos_X, self.Data.CmdPos_Y, self.Data.CmdPos_Z, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', dataName='CmdPos', title='XYZ', newFigure=False)
                self.Plot3D(self.Data.ActPos_X, self.Data.ActPos_Y, self.Data.ActPos_Z, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', dataName='ActPos', title='XYZ', newFigure=False)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XYZ: %s' % str(e))

        #XYZ with Time
        if self.Plot.XYZ_Time == True:
            try:
                color = self.Data.Time
                self.Plot3D(self.Data.ActPos_X, self.Data.ActPos_Y, self.Data.ActPos_Z, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='Time (s)', title='XYZ_Time', newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_Time: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XYZ_Time: %s' % str(e))

        #XYZ with Z
        if self.Plot.XYZ_Z == True:
            try:
                color = self.Data.ActPos_Z
                self.Plot3D(self.Data.ActPos_X, self.Data.ActPos_Y, self.Data.ActPos_Z, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='Z (mm)', title='XYZ_Z', newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_Z: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XYZ_Z: %s' % str(e))

        #XYZ with CmdPathVel
        if self.Plot.XYZ_PathVel == True:
            try:
                color = self.Data.CmdPathVel
                self.Plot3D(self.Data.ActPos_X, self.Data.ActPos_Y, self.Data.ActPos_Z, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='CmdPathVel (mm/min)', title='XYZ_PathVel', newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_PathVel: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XYZ_PathVel: %s' % str(e))

        #XYZ with CmdPathAcc
        if self.Plot.XYZ_PathAcc == True:
            try:
                color = self.Data.CmdPathAcc
                self.Plot3D(self.Data.ActPos_X, self.Data.ActPos_Y, self.Data.ActPos_Z, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='CmdPathAcc (m/s^2)', title='XYZ_PathAcc', newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_PathAcc: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XYZ_PathAcc: %s' % str(e))

        #XYZ with CmdPathJerk
        if self.Plot.XYZ_PathJerk == True:
            try:
                color = self.Data.CmdPathJerk
                self.Plot3D(self.Data.ActPos_X, self.Data.ActPos_Y, self.Data.ActPos_Z, color=color, axisName_1='X (mm)', axisName_2='Y (mm)', axisName_3='Z (mm)', colorName='CmdPathJerk (m/s^3)', title='XYZ_PathJerk', newFigure=True)
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError XYZ_PathJerk: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error XYZ_PathJerk: %s' % str(e))

        # ----------------------------Plot Circle Error----------------------------- #
        # circular error of XY
        if self.Plot.CircleErr_XY == True:
            try:
                Center1 = (max(self.Data.SetPos_X) + min(self.Data.SetPos_X)) / 2
                Center2 = (max(self.Data.SetPos_Y) + min(self.Data.SetPos_Y)) / 2
                R_MaxErr = 0.05
                R = (max(self.Data.SetPos_X) - min(self.Data.SetPos_X)) / 2
                self.PlotCircleError(R, R_MaxErr, Center1, Center2, self.Data.CmdPos_X, self.Data.CmdPos_Y, self.Data.ActPos_X, self.Data.ActPos_Y, F=None, title='CircleErr_XY')
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError CircleErr_XY: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error CircleErr_XY: %s' % str(e))

        # circular error of YZ
        if self.Plot.CircleErr_YZ == True:
            try:
                Center1 = (max(self.Data.SetPos_Y) + min(self.Data.SetPos_Y)) / 2
                Center2 = (max(self.Data.SetPos_Z) + min(self.Data.SetPos_Z)) / 2
                R_MaxErr = 0.05
                R = (max(self.Data.SetPos_Y) - min(self.Data.SetPos_Y)) / 2
                self.PlotCircleError(R, R_MaxErr, Center1, Center2, self.Data.CmdPos_Y, self.Data.CmdPos_Z, self.Data.ActPos_Y, self.Data.ActPos_Z, F=None, title='CircleErr_YZ')
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError CircleErr_YZ: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error CircleErr_YZ: %s' % str(e))

        # circular error of XZ
        if self.Plot.CircleErr_XZ == True:
            try:
                Center1 = (max(self.Data.SetPos_X) + min(self.Data.SetPos_X)) / 2
                Center2 = (max(self.Data.SetPos_Z) + min(self.Data.SetPos_Z)) / 2
                R_MaxErr = 0.05
                R = (max(self.Data.SetPos_X) - min(self.Data.SetPos_X)) / 2
                self.PlotCircleError(R, R_MaxErr, Center1, Center2, self.Data.CmdPos_X, self.Data.CmdPos_Z, self.Data.ActPos_X, self.Data.ActPos_Z, F=None, title='CircleErr_XZ')
            except Exception as e:
                print('\033[1;34m\nPlotData: \033[1;31mError CircleErr_XZ: %s\033[0m' % str(e))
                self.OutputMessageToGUI('\nPlotData: Error CircleErr_XZ: %s' % str(e))

        
        # ---------------------------------end---------------------------------- #
        return None

    ##################################################################################
    # ----------------------------------Plot 1D Data-------------------------------- #
    ##################################################################################
    def Plot1D(self, x, axisName_1=None, dataName=None, shareAxis=None, newFigure=True, mark='.-', tLimit=None, xLimit=None, title=''):
        plt.rcParams['font.family'] = 'Microsoft YaHei'
        plt.rcParams.update({'figure.max_open_warning': 0})
        x = np.array(x)
        if newFigure:
            self.FigNum += 1
            print('')
            self.OutputMessageToGUI('\n')
        sys.stdout.write("\033[1;34m\rPlotData: \033[0mDrawing Figure %2d  %s\033[0m" % (self.FigNum, title))
        self.OutputMessageToGUI('PlotData: Drawing Figure %2d  %s' % (self.FigNum, title), overwrite=True)
        fig = plt.figure(self.FigNum)
        if newFigure:
            fig.clf()
        if shareAxis == 'Time' or shareAxis == 'time':
            shareAx = self.ShareAxis.Time
        else:
            shareAx = None
        if fig.get_axes() == []:
            ax = fig.add_subplot(1, 1, 1, sharex=shareAx)
        else:
            ax = fig.get_axes()[0]
        ax.plot(self.Data.Time, x, mark, label=dataName, alpha=0.7)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel(axisName_1)
        if dataName != None:
            ax.legend(loc="upper right")
        if title != '':
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
        sys.stdout.write("\033[1;34m\rPlotData: \033[1;32mDone    \033[0mFigure %2d  %s       \033[0m" % (self.FigNum, title))
        self.OutputMessageToGUI('PlotData: Done    Figure %2d  %s       ' % (self.FigNum, title), overwrite=True)
        plt.ioff()
        if shareAxis == 'Time' or shareAxis == 'time':
            self.ShareAxis.Time = ax
        return ax

    ##################################################################################
    # ----------------------------------Plot 2D Data-------------------------------- #
    ##################################################################################
    def Plot2D(self, x, y, color=None, axisName_1=None, axisName_2=None, colorName=None, dataName=None, shareAxis=None, newFigure=True, mark='.-', xLimit=None, yLimit=None, title='', equalScale=False):
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
        sys.stdout.write("\033[1;34m\rPlotData: \033[0mDrawing Figure %2d  %s\033[0m" % (self.FigNum, title))
        self.OutputMessageToGUI('PlotData: Drawing Figure %2d  %s' % (self.FigNum, title), overwrite=True)
        fig = plt.figure(self.FigNum)
        if newFigure:
            fig.clf()
        if equalScale == True:
            shareAx = None # do not use shareAxis when equalScale
        elif shareAxis == 'XY' or shareAxis == 'xy':
            shareAx = self.ShareAxis.XY
        elif shareAxis == 'YZ' or shareAxis == 'yz':
            shareAx = self.ShareAxis.YZ
        elif shareAxis == 'XZ' or shareAxis == 'xz':
            shareAx = self.ShareAxis.XZ
        else:
            shareAx = None
        if fig.get_axes() == []:
            ax = fig.add_subplot(1, 1, 1, sharex=shareAx, sharey=shareAx)
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
        if title != '':
            ax.set_title(title)
        else:
            ax.set_title('2D')
        if xLimit != None:
            plt.xlim(xLimit)
        if yLimit != None:
            plt.ylim(yLimit)
        ax.grid('on')
        if equalScale == True:
            plt.axis('equal')
        plt.ion()
        plt.draw()
        plt.pause(0.001)
        sys.stdout.write("\033[1;34m\rPlotData: \033[1;32mDone    \033[0mFigure %2d  %s       \033[0m" % (self.FigNum, title))
        self.OutputMessageToGUI('PlotData: Done    Figure %2d  %s       ' % (self.FigNum, title), overwrite=True)
        plt.ioff()
        if shareAxis == 'XY' or shareAxis == 'xy':
            self.ShareAxis.XY = ax
        elif shareAxis == 'YZ' or shareAxis == 'yz':
            self.ShareAxis.YZ = ax
        elif shareAxis == 'XZ' or shareAxis == 'xz':
            self.ShareAxis.XZ = ax
        return ax

    ##################################################################################
    # ----------------------------------Plot 3D Data-------------------------------- #
    ##################################################################################
    def Plot3D(self, x, y, z, color=None, axisName_1=None, axisName_2=None, axisName_3=None, colorName=None, dataName=None, newFigure=True, mark='-', xLimit=None, yLimit=None, zLimit=None, title=''):
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
        sys.stdout.write("\033[1;34m\rPlotData: \033[0mDrawing Figure %2d  %s\033[0m" % (self.FigNum, title))
        self.OutputMessageToGUI('PlotData: Drawing Figure %2d  %s' % (self.FigNum, title), overwrite=True)
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
        if title != '':
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
        sys.stdout.write("\033[1;34m\rPlotData: \033[1;32mDone    \033[0mFigure %2d  %s       \033[0m" % (self.FigNum, title))
        self.OutputMessageToGUI('PlotData: Done    Figure %2d  %s       ' % (self.FigNum, title), overwrite=True)
        plt.ioff()
        return None

    ##################################################################################
    # -------------------------------Plot Circle Error------------------------------ #
    ##################################################################################
    def PlotCircleError(self, R, R_MaxErr, Center1, Center2, CmdPos1_mm, CmdPos2_mm, ActPos1_mm, ActPos2_mm, F=None, title=''):
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
        
        self.PlotPolar(Thtea, Radius, title=title, dataName=dataName, newFigure=True)
        plt.yticks(np.array(range(int((R_Display - R_MaxErr) * 1000), int((R_Display + R_MaxErr) * 1000), int(R_DisplayStep * 1000))) / 1000, np.array(range(int(-R_MaxErr * 1000), int(R_MaxErr * 1000), int(R_DisplayStep * 1000))))
        
        return None

    ##################################################################################
    # --------------------------------Plot Polar Data------------------------------- #
    ##################################################################################
    def PlotPolar(self, Theta, Radius, dataName=None, mark='-', newFigure=True, title=''):
        plt.rcParams['font.family'] = 'Microsoft YaHei'
        plt.rcParams.update({'figure.max_open_warning': 0})
        #len = min(Theta.__len__(), Radius.__len__())
        #Theta = np.array(Theta[:len])
        #Radius = np.array(Radius[:len])
        if newFigure:
            self.FigNum += 1
            print('')
            self.OutputMessageToGUI('\n')
        sys.stdout.write("\033[1;34m\rPlotData: \033[0mDrawing Figure %2d  %s\033[0m" % (self.FigNum, title))
        self.OutputMessageToGUI('PlotData: Drawing Figure %2d  %s' % (self.FigNum, title), overwrite=True)
        fig = plt.figure(self.FigNum)
        if newFigure:
            fig.clf()
            #fig.add_subplot(111, projection='polar')
        plt.polar(Theta, Radius, mark, alpha=0.5)
        if title != '':
            plt.title(title)
        if dataName != None:
            plt.legend(dataName, loc="upper right")
        plt.grid('on')
        plt.ion()
        plt.draw()
        plt.pause(0.001)
        sys.stdout.write("\033[1;34m\rPlotData: \033[1;32mDone    \033[0mFigure %2d  %s       \033[0m" % (self.FigNum, title))
        self.OutputMessageToGUI('PlotData: Done    Figure %2d  %s       ' % (self.FigNum, title), overwrite=True)
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

    def diff(self, x):
        y = np.array(x)
        y = np.diff(y)
        y = np.append(y, y[-1])
        return y
    ##################################################################################
    # -----------------------------Split Data from Str------------------------------ #
    ##################################################################################
    def SplitDataStr(self, str):
        # elementList = re.split("[\t\n ,]", str)
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
        except Exception as e:
            print('\033[1;34m\nLoadData: \033[1;31mError(CodeLine %d) in loading DataFile: %s\033[0m' % (sys._getframe().f_lineno, str(e)))
            self.OutputMessageToGUI('\nLoadData: Error (CodeLine %d) in loading DataFile: %s\n' % (sys._getframe().f_lineno, str(e)))
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
                            maxTime = max(maxTime, float(Time))
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
        #Ts (Sample time)
        self.Data.Ts = self.Ts
        
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
            print('\033[1;34m\n\nDataInfo: \033[1;31mError: can not import mpldatacursor\033[0m')
            self.OutputMessageToGUI('\n\nDataInfo: Error: can not import mpldatacursor \n')
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
            mpldatacursor.datacursor(artists, display='multiple', draggable=True, formatter=lambda **param: self.InfoText[param['ind'][0]]+'\nValue: (%g, %g)' % (param['x'], param['y']))
            self.DataInfoExist = True
            #print('\033[1;34m\n\nDataInfo: \033[1;32mDone\033[0m')
            #self.OutputMessageToGUI('\n\nDataInfo: Done \n')
        except Exception as e:
            print('\033[1;34m\n\nDataInfo: \033[1;31mError: %s\033[0m' % str(e))
            self.OutputMessageToGUI('\n\nDataInfo: Error: %s\n' % str(e))
        return None

##################################################################################
# -------------------------------------GUI-------------------------------------- #
##################################################################################
if __name__ == '__main__':

    # init paramters of PA
    PA = PA_Data_Analyze()
    PA.AxisID_X = 1
    PA.AxisID_Y = 2
    PA.AxisID_Z = 3
    
    # for UserCode in GUI
    data                = PA.Data
    var                 = PA.Data.Var
    plot1               = PA.Plot1D
    plot2               = PA.Plot2D
    plot3               = PA.Plot3D
    plotCircleError     = PA.PlotCircleError
    info                = PA.DataInfo
    out                 = PA.OutputMessageToGUI
    diff                = PA.diff
    sqrt                = np.sqrt
    sin                 = np.sin
    cos                 = np.cos
    tan                 = np.tan
    arccos              = np.arccos
    arcsin              = np.arcsin
    arctan              = np.arctan
    arctan2             = np.arctan2
    exp                 = np.exp

    TextBox             = dict()
    Button              = dict()
    Entry               = dict()
    Label               = dict()
    StringVar           = dict()
    Combobox            = dict()
    ScrolledText        = dict()
    LabelFrame          = dict()
    CheckButton         = dict()
    CheckVar            = dict()
    Notebook            = dict()
    Frame               = dict()
    
    #init parameters of GUI
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import scrolledtext
    class GUI_Param():
        def __init__(self):
            self.WindowSize = '1000x615'
            self.WindowPosition = ''
            self.lastTime = time.time()
            self.EnableUserCode = True
            self.UserCode = ''
            
        def getWindowSize(self, event):
            if str(event.widget) != '.':
                return None
            #print(event.widget, event.width, event.height, event.x, event.y)
            self.currentTime = time.time()
            #if (self.currentTime - self.lastTime) > 0.2 and event.width > 1 and event.height > 1:
            if event.width > 1 and event.height > 1:
                self.WindowSize = '%dx%d' % (event.width, event.height)
                self.WindowPosition = '+%d+%d' % (event.x, event.y)
            #self.lastTime = time.time()
    
    GUI = GUI_Param()
    
    # init config used in GUI
    import configparser
    import os
    class Config():
        def __init__(self):
            self.fileName = os.path.splitext(os.path.basename(__file__))[0] + '.ini'
            print(self.fileName)
            self.conf = configparser.ConfigParser()
            self.conf.read(self.fileName)
            
        def read(self):
            def get_param(section, key, defaultValue):
                try:
                    return self.conf.get(section, key)
                except:
                    try:
                        self.conf.set(section, key, str(defaultValue))
                    except:
                        self.conf.add_section(section)
                        self.conf.set(section, key, str(defaultValue))
                    return defaultValue
                
            GUI.WindowSize      = str(get_param('WINDOW', 'WindowSize', str(GUI.WindowSize)))
            GUI.WindowPosition  = str(get_param('WINDOW', 'WindowPosition', str(GUI.WindowPosition)))
            GUI.EnableUserCode  = bool(get_param('WINDOW', 'EnableUserCode', str(bool(GUI.EnableUserCode))) == 'True')
            GUI.UserCode        = str(get_param('WINDOW', 'UserCode', str(GUI.UserCode)))
            try:
                GUI.UserCode    = str(bytearray(bytes.fromhex(GUI.UserCode)), 'utf-8')
            except:
                GUI.UserCode    = ''
            
            PA.DataFileName     = str(get_param('LOAD', 'DataFileName', str(PA.DataFileName)))
            PA.Ts               = float(get_param('LOAD', 'Ts', str(PA.Ts)))
            PA.BlockRange[0]    = int(float(get_param('LOAD', 'BlockRange[0]', str(PA.BlockRange[0]))))
            PA.BlockRange[1]    = int(float(get_param('LOAD', 'BlockRange[1]', str(PA.BlockRange[1]))))
            PA.TimeRange[0]     = float(get_param('LOAD', 'TimeRange[0]', str(PA.TimeRange[0])))
            PA.TimeRange[1]     = float(get_param('LOAD', 'TimeRange[1]', str(PA.TimeRange[1])))
            PA.AxisID_X         = int(float(get_param('LOAD', 'AxisID_X', str(PA.AxisID_X))))
            PA.AxisID_Y         = int(float(get_param('LOAD', 'AxisID_Y', str(PA.AxisID_Y))))
            PA.AxisID_Z         = int(float(get_param('LOAD', 'AxisID_Z', str(PA.AxisID_Z))))
            PA.AxisID_A         = int(float(get_param('LOAD', 'AxisID_A', str(PA.AxisID_A))))
            PA.AxisID_B         = int(float(get_param('LOAD', 'AxisID_B', str(PA.AxisID_B))))
            
            for name in PA.Plot.paramName:
                value = getattr(PA.Plot, name)
                value = value if type(value) == str else str(bool(value))
                value = get_param('PLOT', name, value)
                if value == 'True' or value == 'true':
                    value = True
                elif value == 'False' or value == 'false':
                    value = False
                setattr(PA.Plot, name, value)
            
        def save(self):
            with open(self.fileName, 'w') as f:
                def write_param(section, key, defaultValue):
                    try:
                        self.conf.set(section, key, str(defaultValue))
                    except:
                        self.conf.add_section(section)
                        self.conf.set(section, key, str(defaultValue))

                if GUI.WindowSize != '1x1':
                    write_param('WINDOW', 'WindowSize', str(GUI.WindowSize))
                    write_param('WINDOW', 'WindowPosition', str(GUI.WindowPosition))
                write_param('WINDOW', 'EnableUserCode', str(bool(GUI.EnableUserCode)))
                write_param('WINDOW', 'UserCode', str(GUI.UserCode).encode('utf-8').hex())
                    
                write_param('LOAD', 'DataFileName', str(PA.DataFileName))
                write_param('LOAD', 'BlockRange[0]', str(PA.BlockRange[0]))
                write_param('LOAD', 'BlockRange[1]', str(PA.BlockRange[1]))
                write_param('LOAD', 'TimeRange[0]', str(PA.TimeRange[0]))
                write_param('LOAD', 'TimeRange[1]', str(PA.TimeRange[1]))
                write_param('LOAD', 'AxisID_X', str(PA.AxisID_X))
                write_param('LOAD', 'AxisID_Y', str(PA.AxisID_Y))
                write_param('LOAD', 'AxisID_Z', str(PA.AxisID_Z))
                write_param('LOAD', 'AxisID_A', str(PA.AxisID_A))
                write_param('LOAD', 'AxisID_B', str(PA.AxisID_B))
                
                for name in PA.Plot.paramName:
                    value = getattr(PA.Plot, name)
                    value = value if type(value) == str else str(bool(value))
                    write_param('PLOT', name, value)

                self.conf.write(f)
        
    config = Config()
    config.read()

    #init window
    window = tk.Tk()
    window.title('PA Data Analyze v%s' % Version)
    window.geometry(GUI.WindowSize + GUI.WindowPosition)
    window.bind('<Configure>', GUI.getWindowSize)
    #Pop up window
    window.iconify()
    window.update()
    window.deiconify()

    def OpenFile():
        filename = filedialog.askopenfilename(title='打开文件', filetypes=[('txt', '*.txt')])
        if type(filename)==str and filename != '':
            Entry['文件路径'].delete(0, tk.END)
            Entry['文件路径'].insert('insert', filename)

    err = -1
    def LoadParamSync():
        PA.DataFileName = Entry['文件路径'].get()
        try:
            PA.Ts = float(Entry['Ts'].get())
        except Exception as e:
            PA.OutputMessageToGUI('\n\nLoadData: Error Ts: %s' % str(e))
            return err
        
        try:
            PA.BlockRange[0] = int(Entry['BlockRange_0'].get()) if Entry['BlockRange_0'].get() != '无' and Entry['BlockRange_0'].get() != '' else 0
            PA.BlockRange[1] = int(Entry['BlockRange_1'].get()) if Entry['BlockRange_1'].get() != '无' and Entry['BlockRange_1'].get() != '' else 0
        except Exception as e:
            PA.OutputMessageToGUI('\n\nLoadData: Error BlockRange: %s' % str(e))
            return err
        
        try:
            PA.TimeRange[0] = float(Entry['TimeRange_0'].get()) if Entry['TimeRange_0'].get() != '无' and Entry['TimeRange_0'].get() != '' else 0
            PA.TimeRange[1] = float(Entry['TimeRange_1'].get()) if Entry['TimeRange_1'].get() != '无' and Entry['TimeRange_1'].get() != '' else 0
        except Exception as e:
            PA.OutputMessageToGUI('\n\nLoadData: Error TimeRange: %s' % str(e))
            return err
        
        PA.AxisID_X = int(Combobox['AxisID_X'].get()) if Combobox['AxisID_X'].get() != '无' else 0
        PA.AxisID_Y = int(Combobox['AxisID_Y'].get()) if Combobox['AxisID_Y'].get() != '无' else 0
        PA.AxisID_Z = int(Combobox['AxisID_Z'].get()) if Combobox['AxisID_Z'].get() != '无' else 0
        PA.AxisID_A = int(Combobox['AxisID_A'].get()) if Combobox['AxisID_A'].get() != '无' else 0
        PA.AxisID_B = int(Combobox['AxisID_B'].get()) if Combobox['AxisID_B'].get() != '无' else 0
        return None
        
    def load_file():
        PA.GuiText = ScrolledText['输出消息']
        if LoadParamSync() == err:
            return None
        if PA.AxisID_X == 0 and PA.AxisID_Y == 0 and PA.AxisID_Z == 0 and PA.AxisID_A == 0:
            return None
        config.save()
        PA.LoadData()
        
    def PlotParamSync():
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
        
        PA.Plot.Plot1D_ShowActPathVel = int(CheckVar['Plot1D_ShowActPathVel'].get())
        PA.Plot.Plot1D_ShowActPathAcc = int(CheckVar['Plot1D_ShowActPathAcc'].get())
        PA.Plot.Plot1D_ShowActPathJerk = int(CheckVar['Plot1D_ShowActPathJerk'].get())
        PA.Plot.Plot1D_ShowActAxisVel = int(CheckVar['Plot1D_ShowActAxisVel'].get())
        PA.Plot.Plot1D_ShowActAxisAcc = int(CheckVar['Plot1D_ShowActAxisAcc'].get())
        PA.Plot.Plot1D_ShowActAxisJerk = int(CheckVar['Plot1D_ShowActAxisJerk'].get())
        
        PA.Plot.Plot2D_PathVelType = Combobox['Plot2D_PathVelType'].get()
        PA.Plot.Plot2D_PathAccType = Combobox['Plot2D_PathAccType'].get()
        PA.Plot.Plot2D_PathJerkType = Combobox['Plot2D_PathJerkType'].get()
        PA.Plot.Plot2D_AbsPathVel = int(CheckVar['Plot2D_AbsPathVel'].get())
        PA.Plot.Plot2D_AbsPathAcc = int(CheckVar['Plot2D_AbsPathAcc'].get())
        PA.Plot.Plot2D_AbsPathJerk = int(CheckVar['Plot2D_AbsPathJerk'].get())
        PA.Plot.Plot2D_EqualScale = int(CheckVar['Plot2D_EqualScale'].get())
        
        GUI.EnableUserCode = int(CheckVar['用户代码'].get())
        GUI.UserCode = ScrolledText['用户代码'].get('1.0', 'end')
        return None

    def plot_data():
        PA.GuiText = ScrolledText['输出消息']
        if PlotParamSync() == err:
            return None
        config.save()
        PA.PlotData()

        if GUI.EnableUserCode and PA.Data.Length != 0:
            try:
                exec(GUI.UserCode)
            except Exception as e:
                print('\033[1;34m\nUerCode: \033[1;31mError: %s\033[0m' % str(e))
                PA.OutputMessageToGUI('\n\nUserCode Error: %s' % str(e))
        
        PA.DataInfo()
        if PA.FigNum == 0:
            print('\033[1;34m\nPlotData: \033[1;31mNo Figure\033[0m')
            PA.OutputMessageToGUI('\nPlotData: No Figure')
    
    #################################### 文件路径 ####################################
    x = 0.05
    y = 0.05
    LabelFrame['文件路径'] = ttk.LabelFrame(window, text='文件路径')
    LabelFrame['文件路径'].place(relx=x - 0.03, rely=y - 0.03, relheight=0.093, relwidth=0.95)

    Entry['文件路径'] = ttk.Entry(window, font=('Microsoft YaHei', 10))
    Entry['文件路径'].delete(0, tk.END)
    Entry['文件路径'].insert('insert', PA.DataFileName)
    Entry['文件路径'].place(relx=x, rely=y, relheight=0.05, relwidth=0.7)
    Button['选择文件'] = ttk.Button(window, text="选择文件", command=OpenFile)
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
    Notebook['绘图'].place(relx=0.02, rely=0.29, relheight=0.41, relwidth=0.95)
    
    #################################### 绘图选项 ####################################
    Frame['绘图选项'] = ttk.Frame(Notebook['绘图'])
    Notebook['绘图'].add(Frame['绘图选项'], text='绘图选项')
    
    s = ttk.Style()                                                                
    s.configure('Blue.TCheckbutton', foreground='blue')                            
    s.configure('Black.TCheckbutton', foreground='black')
    def ChangeCheckButtonColor(Key):
        CheckButton[Key].configure(style='Blue.TCheckbutton') if CheckVar[Key].get() == True else CheckButton[Key].configure(style='Black.TCheckbutton')
    
    # ---------------------------------- 绘图选项1D ----------------------------------#
    x = 0
    y = 0
    LabelFrame['一维绘图选项'] = ttk.LabelFrame(Frame['绘图选项'], text='一维绘图选项')
    LabelFrame['一维绘图选项'].place(relx=x + 0.01, rely=y + 0, relheight=0.96, relwidth=0.275)

    xBias = 0.02
    yBias = 0.11
    xStep = 0.09
    yStep = 0.1
    Key = 'BlockNo'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('BlockNo'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'PathVel'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('PathVel'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'PathAcc'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('PathAcc'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'PathJerk'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('PathJerk'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Pos_X'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Pos_X'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Vel_X'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Vel_X'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Acc_X'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Acc_X'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Jerk_X'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Jerk_X'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)

    xBias += xStep
    yBias = 0.11
    Key = 'Pos_Y'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Pos_Y'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Vel_Y'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Vel_Y'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Acc_Y'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Acc_Y'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Jerk_Y'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Jerk_Y'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Pos_Z'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Pos_Z'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Vel_Z'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Vel_Z'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Acc_Z'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Acc_Z'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Jerk_Z'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Jerk_Z'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)

    xBias += xStep
    yBias = 0.11
    Key = 'Pos_A'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Pos_A'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Vel_A'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Vel_A'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Acc_A'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Acc_A'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Jerk_A'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Jerk_A'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Pos_B'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Pos_B'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Vel_B'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Vel_B'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Acc_B'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Acc_B'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Jerk_B'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('Jerk_B'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.08)
    ChangeCheckButtonColor(Key)

    # ---------------------------------- 绘图选项2D ----------------------------------#
    x = 0.296
    y = 0
    LabelFrame['二维绘图选项'] = ttk.LabelFrame(Frame['绘图选项'], text='二维绘图选项')
    LabelFrame['二维绘图选项'].place(relx=x + 0.01, rely=y + 0, relheight=0.96, relwidth=0.385)

    xBias = 0.02
    yBias = 0.11
    xStep = 0.13
    yStep = 0.1
    Key = 'XY'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XY'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XY_Time'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XY_Time'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XY_BlockNo'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XY_BlockNo'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XY_PathVel'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XY_PathVel'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XY_PathAcc'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XY_PathAcc'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XY_PathJerk'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XY_PathJerk'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XY_PosErr'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XY_PosErr'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XY_Z'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XY_Z'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)

    xBias += xStep
    yBias = 0.11
    Key = 'YZ'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('YZ'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'YZ_Time'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('YZ_Time'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'YZ_BlockNo'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('YZ_BlockNo'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'YZ_PathVel'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('YZ_PathVel'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'YZ_PathAcc'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('YZ_PathAcc'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'YZ_PathJerk'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('YZ_PathJerk'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'YZ_PosErr'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('YZ_PosErr'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'YZ_X'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('YZ_X'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)

    xBias += xStep
    yBias = 0.11
    Key = 'XZ'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XZ'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XZ_Time'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XZ_Time'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XZ_BlockNo'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XZ_BlockNo'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XZ_PathVel'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XZ_PathVel'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XZ_PathAcc'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XZ_PathAcc'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XZ_PathJerk'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XZ_PathJerk'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XZ_PosErr'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XZ_PosErr'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XZ_Y'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XZ_Y'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)

    # ---------------------------------- 绘图选项3D ----------------------------------#
    x = 0.703
    y = 0
    LabelFrame['三维绘图选项'] = ttk.LabelFrame(Frame['绘图选项'], text='三维绘图选项')
    LabelFrame['三维绘图选项'].place(relx=x + 0.01, rely=y + 0, relheight=0.96, relwidth=0.127)

    xBias = 0.02
    yBias = 0.11
    xStep = 0.11
    yStep = 0.1
    Key = 'XYZ'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XYZ'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XYZ_Time'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XYZ_Time'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XYZ_Z'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XYZ_Z'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XYZ_PathVel'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XYZ_PathVel'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XYZ_PathAcc'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XYZ_PathAcc'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'XYZ_PathJerk'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('XYZ_PathJerk'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.115)
    ChangeCheckButtonColor(Key)

    # ---------------------------------- 绘图选项Circle --------------------------------#
    x = 0.852
    y = 0
    LabelFrame['循圆误差选项'] = ttk.LabelFrame(Frame['绘图选项'], text='循圆误差选项')
    LabelFrame['循圆误差选项'].place(relx=x + 0.01, rely=y + 0, relheight=0.96, relwidth=0.127)

    xBias = 0.02
    yBias = 0.11
    xStep = 0.11
    yStep = 0.1
    Key = 'CircleErr_XY'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('CircleErr_XY'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'CircleErr_YZ'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('CircleErr_YZ'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'CircleErr_XZ'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图选项'], command=lambda: ChangeCheckButtonColor('CircleErr_XZ'), text=Key, variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=0.1, relwidth=0.11)
    ChangeCheckButtonColor(Key)
    
    ################################## 绘图细节 ##################################
    Frame['绘图细节'] = ttk.Frame(Notebook['绘图'])
    Notebook['绘图'].add(Frame['绘图细节'], text='绘图细节')
    
    x = 0
    y = 0
    LabelFrame['一维绘图细节'] = ttk.LabelFrame(Frame['绘图细节'], text='一维绘图细节')
    LabelFrame['一维绘图细节'].place(relx=x + 0.01, rely=y + 0, relheight=0.96, relwidth=0.2)
    xBias = 0.02
    yBias = 0.11
    xStep = 0.11
    yStep = 0.11
    relheight = 0.1
    relwidth = 0.18
    
    Key = 'Plot1D_ShowActPathVel'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图细节'], command=lambda: ChangeCheckButtonColor('Plot1D_ShowActPathVel'), text='显示实际合成速度', variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=relheight, relwidth=relwidth)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Plot1D_ShowActPathAcc'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图细节'], command=lambda: ChangeCheckButtonColor('Plot1D_ShowActPathAcc'), text='显示实际合成加速度', variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=relheight, relwidth=relwidth)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Plot1D_ShowActPathJerk'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图细节'], command=lambda: ChangeCheckButtonColor('Plot1D_ShowActPathJerk'), text='显示实际合成加加速度', variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=relheight, relwidth=relwidth)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Plot1D_ShowActAxisVel'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图细节'], command=lambda: ChangeCheckButtonColor('Plot1D_ShowActAxisVel'), text='显示实际各轴速度', variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=relheight, relwidth=relwidth)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Plot1D_ShowActAxisAcc'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图细节'], command=lambda: ChangeCheckButtonColor('Plot1D_ShowActAxisAcc'), text='显示实际各轴加速度', variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=relheight, relwidth=relwidth)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Plot1D_ShowActAxisJerk'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图细节'], command=lambda: ChangeCheckButtonColor('Plot1D_ShowActAxisJerk'), text='显示实际各轴加加速度', variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=relheight, relwidth=relwidth)
    ChangeCheckButtonColor(Key)
    
    x = 0.22
    y = 0
    LabelFrame['二维绘图细节'] = ttk.LabelFrame(Frame['绘图细节'], text='二维绘图细节')
    LabelFrame['二维绘图细节'].place(relx=x + 0.01, rely=y + 0, relheight=0.96, relwidth=0.2)
    xBias = 0.02
    yBias = 0.11
    xStep = 0.11
    yStep = 0.11
    relheight = 0.1
    relwidth = 0.18
    
    Key = 'Plot2D_EqualScale'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图细节'], command=lambda: ChangeCheckButtonColor('Plot2D_EqualScale'), text='等比例刻度缩放', variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=relheight, relwidth=relwidth)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Plot2D_PathVelType'
    Label[Key] = ttk.Label(Frame['绘图细节'], text='PathVel来源', anchor='w', font=('Microsoft YaHei', 9))
    Label[Key].place(relx=x+xBias, rely=y+yBias, relheight=relheight, relwidth=relwidth*3/5)
    StringVar[Key] = tk.StringVar()
    StringVar[Key].set(str(getattr(PA.Plot, Key)))
    values = ['Set', 'Cmd', 'Act']
    Combobox[Key] = ttk.Combobox(Frame['绘图细节'], textvariable=StringVar[Key], values=values, font=('Microsoft YaHei', 9), state='readonly')
    Combobox[Key].place(relx=x+xBias+relwidth*3/5, rely=y+yBias, relheight=relheight, relwidth=relwidth*2/5)
    yBias += yStep
    Key = 'Plot2D_PathAccType'
    Label[Key] = ttk.Label(Frame['绘图细节'], text='PathAcc来源', anchor='w', font=('Microsoft YaHei', 9))
    Label[Key].place(relx=x+xBias, rely=y+yBias, relheight=relheight, relwidth=relwidth*3/5)
    StringVar[Key] = tk.StringVar()
    StringVar[Key].set(str(getattr(PA.Plot, Key)))
    values = ['Set', 'Cmd', 'Act']
    Combobox[Key] = ttk.Combobox(Frame['绘图细节'], textvariable=StringVar[Key], values=values, font=('Microsoft YaHei', 9), state='readonly')
    Combobox[Key].place(relx=x+xBias+relwidth*3/5, rely=y+yBias, relheight=relheight, relwidth=relwidth*2/5)
    yBias += yStep
    Key = 'Plot2D_PathJerkType'
    Label[Key] = ttk.Label(Frame['绘图细节'], text='PathJerk来源', anchor='w', font=('Microsoft YaHei', 9))
    Label[Key].place(relx=x+xBias, rely=y+yBias, relheight=relheight, relwidth=relwidth*3/5)
    StringVar[Key] = tk.StringVar()
    StringVar[Key].set(str(getattr(PA.Plot, Key)))
    values = ['Set', 'Cmd', 'Act']
    Combobox[Key] = ttk.Combobox(Frame['绘图细节'], textvariable=StringVar[Key], values=values, font=('Microsoft YaHei', 9), state='readonly')
    Combobox[Key].place(relx=x+xBias+relwidth*3/5, rely=y+yBias, relheight=relheight, relwidth=relwidth*2/5)
    yBias += yStep
    Key = 'Plot2D_AbsPathVel'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图细节'], command=lambda: ChangeCheckButtonColor('Plot2D_AbsPathVel'), text='PathVel取绝对值', variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=relheight, relwidth=relwidth)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Plot2D_AbsPathAcc'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图细节'], command=lambda: ChangeCheckButtonColor('Plot2D_AbsPathAcc'), text='PathAcc取绝对值', variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=relheight, relwidth=relwidth)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    Key = 'Plot2D_AbsPathJerk'
    CheckVar[Key] = tk.IntVar(); CheckVar[Key].set(getattr(PA.Plot, Key))
    CheckButton[Key] = ttk.Checkbutton(Frame['绘图细节'], command=lambda: ChangeCheckButtonColor('Plot2D_AbsPathJerk'), text='PathJerk取绝对值', variable=CheckVar[Key], onvalue=True, offvalue=False)
    CheckButton[Key].place(relx=x + xBias, rely=y + yBias, relheight=relheight, relwidth=relwidth)
    ChangeCheckButtonColor(Key)
    yBias += yStep
    
    
    ################################## 自定义绘图 ##################################
    Frame['自定义绘图'] = ttk.Frame(Notebook['绘图'])
    Notebook['绘图'].add(Frame['自定义绘图'], text='自定义绘图')
    
    CheckVar['用户代码'] = tk.IntVar(); CheckVar['用户代码'].set(GUI.EnableUserCode)
    CheckButton['用户代码'] = ttk.Checkbutton(Frame['自定义绘图'], text='使用以下代码（Python 3.8）：', variable=CheckVar['用户代码'], onvalue=True, offvalue=False)
    CheckButton['用户代码'].place(relx=0.02, rely=0.02, relheight=0.1, relwidth=0.5)
    ScrolledText['用户代码'] = scrolledtext.ScrolledText(Frame['自定义绘图'], font=('Consolas', 8))
    ScrolledText['用户代码'].insert('end', '%s' % GUI.UserCode)
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
    config.save()

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
