{ It's WORK !!!! }
Uses F_Disk;

Var CurDir:String;
    Disk:Byte;
    Dirs,DirSize:Word;
{    A:Array[1..2000] of Char;}
    Dir  :array [1..16] of Dir_Type;   {Сектор каталога}
    I:Byte;
Begin
  Disk_Error:=False;
  GetDir(0,CurDir);
  Writeln('CurDir = ',CurDir);
  GetDirSector('D:\USERS\DENIS',Disk,Dirs,DirSize);
  Writeln('Disk = ',Disk);
  Writeln('Dirs = ',Dirs);
  Writeln('DirSize = ',DirSize);
  ReadSector(Disk,Dirs,1,Dir);
  Writeln(Disk_Error);
  Writeln(Disk_Status);
  For I:=1 to 16 do
    Writeln(Dir[I].Name);
End.