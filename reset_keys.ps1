
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.SendKeys]::SendWait("^")
[System.Windows.Forms.SendKeys]::SendWait("+")
[System.Windows.Forms.SendKeys]::SendWait("%")
Write-Host "Sent key-up signals for Ctrl, Shift, Alt."
