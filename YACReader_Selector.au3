; YACReader_Selector.au3
; Este script é chamado pelo YACReader.exe (Python) para exibir a seleção do leitor.

#include <GUIConstantsEx.au3>
#include <ButtonConstants.au3>
#Include <Constants.au3> ; Necessário para $IDCLOSE

; --- Configuração dos Caminhos dos Leitores ---
; O YACReader_ORIG.exe deve estar na mesma pasta deste executável do AutoIt
Global Const $g_sYACReaderPath = @ScriptDir & "\YACReader_ORIG.exe"
; O BDReader.exe no seu caminho de instalação padrão
Global Const $g_sBDReaderPath = "C:\Program Files (x86)\BDReader\BDReader.exe"

; --- Obter o caminho completo do quadrinho dos argumentos ---
; O caminho completo do quadrinho é o primeiro argumento passado para este script
Global $sComicPath = ""
If $CmdLine[0] > 0 Then
    $sComicPath = $CmdLine[1]
EndIf

; --- Verificar se o caminho do quadrinho foi recebido ---
If $sComicPath = "" Then
    MsgBox($MB_ICONERROR + $MB_TOPMOST, "Erro", "Caminho do quadrinho não foi passado para o seletor.")
    Exit
EndIf

; --- Criar a Janela de Seleção ---
Global $g_hGUI = GUICreate("Escolher Leitor", 300, 150, -1, -1) ; Largura, Altura, X, Y (-1 para centralizar)
GUISetFont(10, 400, 0, "Segoe UI") ; Ajusta a fonte

; Label para o título da HQ (opcional, pode ser formatado)
Global $sComicTitle = StringRegExpReplace($sComicPath, '^.*[\\/]([^\\/]+)\.\w+$', '\1') ; Extrai apenas o nome do arquivo
If @error Then $sComicTitle = "Quadrinho" ; Fallback se falhar

GUICtrlCreateLabel("Abrir """ & $sComicTitle & """ com:", 10, 10, 280, 20) ; x, y, largura, altura

; Botões para a seleção
; Adicionado $BS_DEFPUSHBUTTON ao botão YACReader para que ele seja o padrão (ativado com ENTER)
Global $g_idYACReaderBtn = GUICtrlCreateButton("YACReader (Original)", 50, 50, 200, 30, $BS_DEFPUSHBUTTON)
Global $g_idBDReaderBtn = GUICtrlCreateButton("BDReader", 50, 90, 200, 30)

; Força o foco inicial no botão YACReader
GUICtrlSetState($g_idYACReaderBtn, $GUI_FOCUS) 

GUISetState(@SW_SHOW) ; Exibir a janela

; --- Loop de Eventos da GUI ---
While 1
    Switch GUIGetMsg()
        Case $GUI_EVENT_CLOSE ; Se o usuário fechar a janela (X)
            Exit ; Sair do script
        
        Case $g_idYACReaderBtn
            If FileExists($g_sYACReaderPath) Then
                ; Lançando YACReader
                Run('"' & $g_sYACReaderPath & '" "' & $sComicPath & '"', "", @SW_SHOWNORMAL) 
                
                ; *** MODIFICAÇÕES AQUI PARA GARANTIR O FOCO NO YACREADER ***
                ; Espera um curto período para a aplicação começar a inicializar
                Sleep(100) 
                ; Espera pela janela do YACReader se tornar ativa (usando a classe fornecida)
                WinWaitActive("[CLASS:Qt5152QWindowIcon]", "", 10) ; Espera até 10 segundos
                ; Ativa a janela, trazendo-a para o primeiro plano
                WinActivate("[CLASS:Qt5152QWindowIcon]")
                ; Garante que a janela esteja restaurada (não minimizada)
                WinSetState("[CLASS:Qt5152QWindowIcon]", "", @SW_RESTORE)
            Else
                MsgBox($MB_ICONERROR + $MB_TOPMOST, "Erro", "YACReader_ORIG.exe não encontrado em: " & $g_sYACReaderPath)
            EndIf
            Exit ; Sair após a escolha

        Case $g_idBDReaderBtn
            If FileExists($g_sBDReaderPath) Then
                ; Lançando BDReader
                Run('"' & $g_sBDReaderPath & '" "' & $sComicPath & '"', "", @SW_SHOWNORMAL) 
                ; Para o BDReader, as linhas de WinWaitActive/WinActivate não são estritamente necessárias
                ; já que ele já estava abrindo normalmente, mas podem ser adicionadas para consistência futura
            Else
                MsgBox($MB_ICONERROR + $MB_TOPMOST, "Erro", "BDReader.exe não encontrado em: " & $g_sBDReaderPath & @CRLF & @CRLF & "Verifique o caminho ou instale o BDReader.")
            EndIf
            Exit
            
    EndSwitch
WEnd