import comtypes.client

def StoryDisp(LoadCaseU):
    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        TableVersion = 0
        FieldsKeysIncluded = []     # Cabeceras de la Tabla / Table Headers
        NumberRecords = 0           # Número de Filas de la Tabla / Number Rows of Table
        TableData = []              # Array que contiene toda la información de la Tabla / Array containing all information of Table
        FieldKeyList = []
        GroupName = None

        [FieldKeyList, TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.GetTableForDisplayArray("Point Bays", FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)

        cont = 1

        CM_Label = [] # labels o Etiquetas de los Puntos de los Centros de Masas
        CM_Unique = [] # Nombres Unicos de los puntos en los Centros de Masas

        Name = None
        NumberNames = 0
        MyName = []

        [NumberNames, MyName, ret] = ETABSModel.Story.GetNameList(NumberNames, MyName)

        piso = 0

        # --------------------------------------------------------------------
        # AGRUPACIÓN DE LOS PUNTOS DE LOS CM EN LABELS Y UNIQUE NAMES
        #---------------------------------------------------------------------
        for i in range(0, NumberRecords):
            if TableData[cont] == "Yes":
                CM_Label.append(TableData[cont - 1])
                [Name, ret] = ETABSModel.PointObj.GetNameFromLabel(TableData[cont - 1], MyName[piso], Name)        
                CM_Unique.append(Name)        
                piso += 1
            cont += len(FieldsKeysIncluded)

        
        forceUnits = 0 ; lengthUnits = 0 ; temperatureUnits = 0
        [forceUnits, lengthUnits, temperatureUnits, ret] = ETABSModel.GetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)
        ETABSModel.SetPresentUnits_2(6, 6, 2) # Unidades Tonf, m, C

        Obj = []
        Elm = []
        U1 = [] ; U2 = [] ; U3 = [] ; R1 = [] ; R2 = [] ; R3 = []
        NumberResults = 0
        LoadCase = []
        StepType = []
        StepNum = []

        Desp_Ux = []
        Desp_Uy = []

        Point_U = []
        D_X = []
        D_Y = []
        Story_Point = []

        ETABSModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        ETABSModel.Results.Setup.SetCaseSelectedForOutput(LoadCaseU)
        for i in range(0, len(CM_Unique)):
            [NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3, ret] = ETABSModel.Results.JointDispl(CM_Unique[i], 0, NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3)
            Desp_Ux = [] ; Desp_Uy = []
            for j in range(0, len(U1)):
                Desp_Ux.append(U1[j])
                Desp_Uy.append(U2[j])
            D_X.append(max(Desp_Ux))
            D_Y.append(max(Desp_Uy))
            Point_U.append(CM_Unique[i])
            Story_Point.append(MyName[i])

        ETABSModel.SetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)

        import pandas as pd

        Data_Desp = {"Punto" : Point_U , "Piso" : Story_Point, "Desp.-X" : D_X, "Desp.-Y" : D_Y}
        Tabla_Desp = pd.DataFrame(Data_Desp)

        return Tabla_Desp
    
    except:
        pass