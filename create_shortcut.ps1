
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\tushar.sharma1\Desktop\Screen Assistant.lnk")
$Shortcut.TargetPath = "C:\Users\tushar.sharma1\AppData\Local\Programs\Python\Python313\pythonw.exe"
$Shortcut.Arguments = """c:\Users\tushar.sharma1\Repository\screen-assistant\screen_assistant_gui.py"""
$Shortcut.WorkingDirectory = "c:\Users\tushar.sharma1\Repository\screen-assistant"
$Shortcut.Description = "AI Screen Assistant"
$Shortcut.IconLocation = "shell32.dll,22" 
$Shortcut.Save()
Write-Host "Shortcut created successfully at C:\Users\tushar.sharma1\Desktop\Screen Assistant.lnk"
