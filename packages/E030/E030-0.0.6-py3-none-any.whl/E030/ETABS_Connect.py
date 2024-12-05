import comtypes.client
import ctypes

def ETABS():
    try:
        ETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
        ETABSModel = ETABSObject.SapModel

        ctypes.windll.user32.MessageBoxW(0, "Connection with ETABS successful", "CEINT-SOFTWARE", 64)
    except:
        pass