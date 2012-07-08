Uses DOS,F_DISK;

Const DirCount  : LongInt = 0; { Количество каталогов }
      FileCount : LongInt = 0; { Количество файлов }
Var StartDir,Symbol:String;

Procedure UndelDir( DirName:String ); { Восстановление каталога }
  Var
    Dir:Array [1..16] of Dir_Type; { Буфер на 1 сектор каталога }
    Disk : Byte;                   { Номер диска }
    Dirs : Word;                   { Номер сектора }
    DirSize: Word;                 { Размер каталога }
    J   : Integer;                 { Номер элемента каталога }
    K,I:Integer; DI:TDisk; SN,SE,SNE:String;
    Clus:Word; { Номер кластера }
  Begin { UndelDir }
   { Искать каталог }
    GetDirSector(DirName,Disk,Dirs,DirSize);
    If Dirs = 0 then Exit; { Dirs=0 - ошибка в маршруте }
    GetDiskInfo(Disk,DI);         { Получаем длину кластера }
    ReadSector(Disk,Dirs,1,Dir);  { Читаем первый сектор }
    K := 0;               { Количество просмотренных элементов }
    J := 1;               { Текущий элемент каталога }
   { Цикл поиска }
    Repeat
     { Пропускаем корневой и над каталог (Hичего не начинается на '.') }
      While Dir[J].NameExt[1] = '.' do Inc(J);
      If Dir[J].Name[1]=#0 then Exit; { Обнаружен конец списка файлов }
      If (Dir[j].FAttr and Directory) = 0 then { Статистика }
        Inc(FileCount) Else Inc(DirCount);
      SN:=Dir[J].Name;
      While SN[Length(SN)]=' ' do SN:=Copy(SN,1,Length(SN)-1);
      SE:=Dir[J].Ext;
      While SE[Length(SE)]=' ' do SE:=Copy(SE,1,Length(SE)-1);
      If SE = '' then SNE:=SN Else SNE:=SN+'.'+SE;
      Writeln('* ',DirName,'\',Dir[J].Name);
  {   If Dir[j].NameExt[1] = #229 then
        Begin
          Dir[j].NameExt[1] := Symbol[1];
          Writeln('- Undeleted ! ',Dir[j].NameExt);
          WriteSector(Disk,Dirs,1,Dir);
        End;}
      If (Dir[j].FAttr And Directory) <> 0 then UndelDir(DirName+'\'+SNE);
      Inc(J);
      If J = 17 then
        Begin
          Inc(K,16);
          if K >= DirSize then Exit; { Дошли до конца каталога }
          J := 1;         { Продолжаем с 1-го элемента следующего сектора }
          If (K div 16) mod DI.ClusSize=0 then
            If Succ(Dirs) < DI.DataLock then
              Inc(Dirs)       { Корневой каталог }
            Else
              Begin   { Конец кластера }
                Clus := GetFATItem(Disk,GetCluster(Disk,Dirs)); { Новый кластер }
                Dirs := GetSector(Disk,Clus) { Новый сектор }
              End
          Else Inc(Dirs); { Очередной сектор - в кластере }
          ReadSector(Disk,Dirs,1,Dir)
        End;
    Until Dir[J].Name[1]=#0;
  End; { UndelDir }

Begin
  Writeln('- Программа для восстановления дерева каталогов -');
  Writeln('Только для FAT12,FAT16 ! За поддержкой обращаться: Denis@ipo.spb.ru');
{  If ParamCount = 2 then
    Begin}
{      StartDir:=ParamStr(1);
      Writeln(' * Восстанавливаемый каталог: ',StartDir);
      Symbol:=ParamStr(2);
      Writeln(' * Hачальный первый символ: ',Symbol[1]);}
      StartDir:='D:\USERS\DENIS';
      Writeln('Протокол восстановления: ');
      Symbol:='#';
      UndelDir(StartDir);
      Writeln('Восстановлено: Файлов ',FileCount,' Каталогов ',DirCount);
{    End
  Else
    Begin
      Writeln('Внимание ! Hеверное количество параметров.');
      Writeln('Для запуска используйте:');
      Writeln('  Undel <Имя восстанавливаемого каталога> <Hачальный первый символ>');
      Writeln('Hапример: Undel D:\USERS #   - Для восстановления каталога USERS');
      Writeln('При этом программа восстановит содержимое каталога USERS на диске D.');
      Writeln('Все файлы и каталоги будут восстановлены под именами');
      Writeln('начинающимися на #. Если встретятся два файла (каталога) имена которых');
      Writeln('будут отличаться только первой буквой, будет выбран следующий символ');
      Writeln('таблицы ASCII (символ $, затем %,...)');
    End;}
End.End.