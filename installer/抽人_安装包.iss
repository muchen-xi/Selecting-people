; 抽人 课堂随机点名 - 安装包脚本
#define MyAppName "抽人"
#define MyAppVersion "1.0.0"
#define MyAppExeName "点我.exe"
#define MyAppAssocName "抽人"

[Setup]
AppId={{985F46F5-9B0C-4083-B1FB-23FAE8CF2945}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=MuHongda
DefaultDirName={localappdata}\Programs\抽人
DefaultGroupName=抽人
PrivilegesRequired=lowest
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\点我.exe
UninstallDisplayName={#MyAppName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
OutputDir=.
OutputBaseFilename=抽人_安装包_v1.0.0
SetupIconFile=..\app.ico
ArchitecturesInstallIn64BitMode=x64compatible
ArchitecturesAllowed=x64compatible
MinVersion=10.0

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "附加任务："; Flags: unchecked

[Files]
Source: "..\dist\点我\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\抽人"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\卸载抽人"; Filename: "{uninstallexe}"
Name: "{autodesktop}\抽人"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "立即运行抽人"; Flags: nowait postinstall skipifsilent
