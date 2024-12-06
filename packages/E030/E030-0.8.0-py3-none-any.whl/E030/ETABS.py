import comtypes.client

# Desplazamientos de los Centros de Masas
def StoryDisp(Caso_Carga:str):
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
        ETABSModel.Results.Setup.SetCaseSelectedForOutput(Caso_Carga)
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

# 1 -> Sistema Regular || 2 -> Sistema Irregular
# R -> Factor de Reducción Sísmica según Norma
# 1-> Concreto || 2 -> Acero || 3-> Albañilería || 4 -> Madera || 5 -> Muros de Ductilidad Limitada

# Derivas de Piso
def StoryDrift(Caso_Carga:str, sistema:int, R:float, Material:int):
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
        Altura_Pisos = [] # Altura de todos los pisos

        Name = None
        NumberNames = 0
        MyName = []
        Height = 0

        [NumberNames, MyName, ret] = ETABSModel.Story.GetNameList(NumberNames, MyName)
        
        piso = 0

        # --------------------------------------------------------------------
        # AGRUPACIÓN DE LOS PUNTOS DE LOS CM EN LABELS Y UNIQUE NAMES
        #---------------------------------------------------------------------
        for i in range(0, NumberRecords):
            if TableData[cont] == "Yes":
                CM_Label.append(TableData[cont - 1])
                [Name, ret] = ETABSModel.PointObj.GetNameFromLabel(TableData[cont - 1], MyName[piso], Name)
                [Height, ret] = ETABSModel.Story.GetHeight(MyName[piso], Height)       
                CM_Unique.append(Name)
                Altura_Pisos.append(Height)
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

        Deriva_Elast_X = []
        Deriva_Elast_Y = []
        Deriva_Inelast_X = []
        Deriva_Inelast_Y = []
        Desp_Rel_X = []
        Desp_Rel_Y = []
        Deriva_Limite = []

        factor = 0
        limite = 0

        if sistema == 1:
            factor = 0.75 * R
        else:
            factor = 0.85 * R
        
        if Material == 1:
            limite = 0.007
        elif Material == 2:
            limite = 0.010
        elif Material == 3:
            limite = 0.005
        elif Material == 4:
            limite = 0.010
        elif Material == 5:
            limite = 0.005

        ETABSModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
        ETABSModel.Results.Setup.SetCaseSelectedForOutput(Caso_Carga)
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
            Deriva_Limite.append(limite)

            if len(D_X) > 1:
                Desp_Rel_X.append(D_X[len(D_X)-2] - D_X[len(D_X)-1])
                Desp_Rel_Y.append(D_Y[len(D_Y)-2] - D_Y[len(D_Y)-1])
                Deriva_Elast_X.append((D_X[len(D_X)-2] - D_X[len(D_X)-1]) / Altura_Pisos[i])
                Deriva_Elast_Y.append((D_Y[len(D_Y)-2] - D_Y[len(D_Y)-1]) / Altura_Pisos[i])
                Deriva_Inelast_X.append(factor * (D_X[len(D_X)-2] - D_X[len(D_X)-1]) / Altura_Pisos[i])
                Deriva_Inelast_Y.append(factor * (D_Y[len(D_Y)-2] - D_Y[len(D_Y)-1]) / Altura_Pisos[i])

        Desp_Rel_X.append(D_X[len(D_X)-1])
        Desp_Rel_Y.append(D_Y[len(D_Y)-1])
        Deriva_Elast_X.append(D_X[len(D_X)-1] / Altura_Pisos[len(D_X)-1])
        Deriva_Elast_Y.append(D_Y[len(D_Y)-1] / Altura_Pisos[len(D_X)-1])
        Deriva_Inelast_X.append(factor * D_X[len(D_X)-1] / Altura_Pisos[len(D_X)-1])
        Deriva_Inelast_Y.append(factor * D_Y[len(D_Y)-1] / Altura_Pisos[len(D_X)-1])
        
        ETABSModel.SetPresentUnits_2(forceUnits, lengthUnits, temperatureUnits)
     
        import pandas as pd

        Data_Deriva = {"Punto" : Point_U , "Piso" : Story_Point, "Desp.-X" : D_X, "Desp.-Y" : D_Y, "Desp. Rel.-X" : Desp_Rel_X, "Desp. Rel.-Y" : Desp_Rel_Y,
                     "Der. Elást.-X" : Deriva_Elast_X, "Der. Elást.-Y" : Deriva_Elast_Y, "Der. Inelást.-X" : Deriva_Inelast_X, "Der. Inelást.-Y" : Deriva_Inelast_Y,
                     "Limite" : Deriva_Limite}
        Tabla_Deriva = pd.DataFrame(Data_Deriva)

        return Tabla_Deriva
    
    except:
        pass

# Definición del Sismo Estático
def SeismoUserCoef(NameLoad:str, DirLoad:tuple, Ecc:float, RangeStory:tuple, C:float, k:float):
    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel
        
        # Definición de Patrón de Carga Sísmica Estática
        ETABSModel.LoadPatterns.Add(NameLoad, 5)

        NumFatalErrors = 0 ; NumErrorMsgs = 0 ; NumWarnMsgs = 0 ; NumInfoMsgs = 0
        ImportLog = None        # Información del resultado de la Importación de Datos a la Tabla
        TableVersion = 1
        FieldsKeysIncluded = [] # Contiene las Cabeceras de la Tabla
        NumberRecords = 0       # Número de Filas que tiene la Tabla
        TableData = []          # Contenido de la Tabla
        GroupName = None

        [TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.GetTableForEditingArray("Load Pattern Definitions - Auto Seismic - User Coefficient", GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
        
        FieldsKeysIncluded = ["Name", "IsAuto", "XDir", "XDirPlusE", "XDirMinusE", "YDir", "YDirPlusE", "YDirMinusE", 
                      "EccRatio", "TopStory", "BotStory", "OverStory", "OverDiaph", "OverEcc", "C", "K"]
        
        if len(TableData) > 1:
            Table_Old = []
            for j in range(0, len(TableData)):
                Table_Old.append(TableData[j])
            New_Data = ["Sismo-Y E030", "No", "No", "No", "No", "Yes", "Yes", "Yes", "0.05", "Story4", "Base", None, None, None, "0.1675", "1.235"]
            TableData = Table_Old + New_Data
        else:
            TableData = [NameLoad, "No", DirLoad[0], DirLoad[1], DirLoad[2], DirLoad[3], DirLoad[4], DirLoad[5], str(Ecc), RangeStory[0], RangeStory[1], None, None, None, str(C), str(k)]

        NumberRecords = int(len(TableData) / len(FieldsKeysIncluded))
        [FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.SetTableForEditingArray("Load Pattern Definitions - Auto Seismic - User Coefficient", TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
        [NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog, ret] = ETABSModel.DatabaseTables.ApplyEditedTables(True, NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog)

        return print("Carga Sismica \"" + NameLoad + "\" creada con éxito")

    except:
        return print("La Carga \"" + NameLoad + "\" no pude crearse")

# Arreglo personalizado de listas de barras
def BarCustom(NameBars:tuple, Diameter:tuple, Area:tuple):
        try:
            ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
            ETABSModel = ETABSObject.SapModel

            NumFatalErrors = 0 ; NumErrorMsgs = 0 ; NumWarnMsgs = 0 ; NumInfoMsgs = 0
            ImportLog = None        # Información del resultado de la Importación de Datos a la Tabla
            TableVersion = 1
            FieldsKeysIncluded = [] # Contiene las Cabeceras de la Tabla
            NumberRecords = 0       # Número de Filas que tiene la Tabla
            TableData = []          # Contenido de la Tabla
            GroupName = None

            [TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.GetTableForEditingArray("Reinforcing Bar Sizes", GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)

            FieldsKeysIncluded = ["Name", "Diameter", "Area", "GUID"] # Cabeceras de la Tabla

            TableData = []

            for i in range(0, len(NameBars)):
                TableData.append(str(NameBars[i]), str(Diameter[i]), str(Area[i]), "GDSAGDSAFDASFAGEE")

            NumberRecords = int(len(TableData) / len(FieldsKeysIncluded))
            [FieldsKeysIncluded, NumberRecords, TableData, ret] = ETABSModel.DatabaseTables.SetTableForEditingArray("Reinforcing Bar Sizes", TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
            [NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog, ret] = ETABSModel.DatabaseTables.ApplyEditedTables(True, NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog)

            import ctypes
            return ctypes.windll.user32.MessageBoxW(0, ImportLog, "CEINT-SOFTWARE", 64)
        
        except:
            pass
    