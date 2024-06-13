import ctypes
from ctypes import wintypes
def getfont():
    # Define necessary types
    LF_FACESIZE = 32
    LF_FULLFACESIZE = 64

    class LOGFONT(ctypes.Structure):
        _fields_ = [
            ("lfHeight", wintypes.LONG),
            ("lfWidth", wintypes.LONG),
            ("lfEscapement", wintypes.LONG),
            ("lfOrientation", wintypes.LONG),
            ("lfWeight", wintypes.LONG),
            ("lfItalic", wintypes.BYTE),
            ("lfUnderline", wintypes.BYTE),
            ("lfStrikeOut", wintypes.BYTE),
            ("lfCharSet", wintypes.BYTE),
            ("lfOutPrecision", wintypes.BYTE),
            ("lfClipPrecision", wintypes.BYTE),
            ("lfQuality", wintypes.BYTE),
            ("lfPitchAndFamily", wintypes.BYTE),
            ("lfFaceName", wintypes.WCHAR * LF_FACESIZE)
        ]

    # Define callback function
    def EnumFontFamiliesExProc(lpelfe, lpntme, FontType, lParam):
        fonts.append(lpelfe.contents.lfFaceName)
        return 1

    # Define function prototype
    EnumFontFamiliesExProcProto = ctypes.WINFUNCTYPE(
        wintypes.INT, ctypes.POINTER(LOGFONT), ctypes.POINTER(wintypes.LONG), wintypes.DWORD, wintypes.LPARAM
    )
    EnumFontFamiliesExProc = EnumFontFamiliesExProcProto(EnumFontFamiliesExProc)

    # Load gdi32.dll
    gdi32 = ctypes.WinDLL("gdi32")

    # Load user32.dll
    user32 = ctypes.WinDLL("user32")

    # Get device context
    hdc = user32.GetDC(None)

    # Prepare LOGFONT
    lf = LOGFONT()
    lf.lfCharSet = 1  # DEFAULT_CHARSET

    # Prepare list to store font names
    fonts = []

    # Enumerate fonts
    gdi32.EnumFontFamiliesExW(hdc, ctypes.byref(lf), EnumFontFamiliesExProc, 0, 0)

    # Release device context
    user32.ReleaseDC(None, hdc)

    return fonts