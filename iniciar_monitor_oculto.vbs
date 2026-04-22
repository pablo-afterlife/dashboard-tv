' ============================================================
' iniciar_monitor_oculto.vbs
'
' Inicia o monitor Excel em segundo plano, completamente
' sem janela e sem ícone na barra de tarefas.
'
' Como usar:
'   Duplo clique neste arquivo  →  monitor inicia oculto
'
' Para iniciar automaticamente com o Windows:
'   1. Pressione Win+R e digite:  shell:startup
'   2. Coloque um atalho deste arquivo .vbs na pasta que abrir
'
' Para encerrar o monitor:
'   Gerenciador de Tarefas → aba Detalhes → encerrar pythonw.exe
' ============================================================

Option Explicit

Dim objShell, objFSO
Dim strScript, strPython
Dim arrPaths, i

strScript = "C:\Users\Consultor\Scripts\dashboard-monitor\monitor_excel.py"

' Locais comuns do Python (pythonw = sem janela)
arrPaths = Array( _
    "C:\Users\Consultor\AppData\Local\Programs\Python\Python312\pythonw.exe", _
    "C:\Users\Consultor\AppData\Local\Programs\Python\Python311\pythonw.exe", _
    "C:\Users\Consultor\AppData\Local\Programs\Python\Python310\pythonw.exe", _
    "C:\Python312\pythonw.exe", _
    "C:\Python311\pythonw.exe", _
    "C:\Python310\pythonw.exe" _
)

Set objFSO   = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("WScript.Shell")

' Verifica se o script existe
If Not objFSO.FileExists(strScript) Then
    MsgBox "Script não encontrado:" & vbCrLf & strScript & vbCrLf & vbCrLf & _
           "Verifique o caminho e tente novamente.", _
           vbCritical, "Monitor Excel - Erro"
    WScript.Quit 1
End If

' Encontra pythonw.exe
strPython = ""
For i = 0 To UBound(arrPaths)
    If objFSO.FileExists(arrPaths(i)) Then
        strPython = arrPaths(i)
        Exit For
    End If
Next

' Fallback: pythonw do PATH do sistema
If strPython = "" Then
    strPython = "pythonw.exe"
End If

' Inicia o monitor oculto (0 = sem janela, False = não aguarda encerramento)
objShell.Run """" & strPython & """ """ & strScript & """", 0, False

' Mensagem silenciosa — nenhum popup, processo apenas sobe em background
WScript.Quit 0
