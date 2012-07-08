#!/usr/bin/perl -w
use strict;
use diagnostics -verbose;
use CGI qw(:standard);
use vars qw($query $cols $rows $first_col_width $other_col_width @row_head
@col_head $check_image $blank_image $row1_height $row_height
@correct_answers);
use subs qw(setup_defaults controls create_table write_code);

## width and height cannot be made (in table) less than some predefined 
## (in browser?) size

# [TODO] radiobutton to chose pics for $check_image
#        attempts count in checkIt()
$blank_image = 'blank.gif';
$check_image = 'check1.gif';

$query = new CGI;
print $query->header;
print $query->start_html;
if (defined ($query->param('rows')))
{
  $rows = $query->param('rows');
  $cols = $query->param('cols');
  $first_col_width = $query->param('width1');
  $other_col_width = $query->param('width2');
  $row1_height  = $query->param('height1');
  $row_height = $query->param('height2');
  foreach (1..$cols)
  {
    $col_head[$_] = $query->param("col_head$_");
  }
  foreach (1..$rows)
  {
    $row_head[$_] = $query->param("row_head$_");
  }
  @correct_answers = split(/,/,$query->param('correct_answers'));
}
else
{
  setup_defaults;
}
if ($query->param('tp_only') ne 'true') {
  controls;
  print $query->hr;
}
create_table;
print "\n";
write_code;
print $query->end_html;
1;

sub controls {
  print $query->startform();
  print $query->em('Columns:');
  print $query->textfield('cols',$cols,5);
  print $query->em('Rows:');
  print $query->textfield('rows',$rows,5);
  print $query->em('First column width:');
  print $query->textfield('width1',$first_col_width,5);
  print $query->em('Other columns width:');
  print $query->textfield('width2',$other_col_width,5),'<BR>';
  print $query->em('First row height:');
  print $query->textfield('height1',$row1_height,5);
  print $query->em('Other rows height:');
  print $query->textfield('height2',$row_height,5),'<BR>';
  print $query->hidden('correct_answers',join(',',@correct_answers));
  foreach (1..$cols)
  {
    print $query->textfield("col_head$_",$col_head[$_],15);
  }
  print '<BR>';
  foreach (1..$rows)
  {
    print $query->textfield("row_head$_",$row_head[$_],15);
  }
  print $query->hidden('tp_only','false');
  print '<BR>';
  print $query->submit();
  print $query->submit(-name=>'Save correct answers',-onClick=>"writeCorrect();");
  print $query->submit(-name=>'TestPage only',-onClick=>"document.forms[0].tp_only.value='true';");
  print $query->endform;
  print 'Correct answers are:',$#correct_answers,' len; =',join(',',@correct_answers),'<BR>';
}

sub create_table {
  my($i,$ii) = ($rows+1,$cols+1);
  print qq/<TABLE BORDER="1" CELLPADDING="1" CELLSPACING="1" ROWS="$i"
COLS="$ii">/;
  print '<TR>';
  print qq/<TD WIDTH="$first_col_width" HEIGHT="$row1_height">/,'</TD>';
  foreach $i (1..$cols)
  {
    print qq(<TD WIDTH="$other_col_width" HEIGHT="$row1_height">$col_head[$i]</TD>);
  }
  print '</TR>';
  foreach $i (1..$rows)
  {
    print '<TR>';
    print qq/<TD WIDTH="$first_col_width" HEIGHT="$row_height">/,$row_head[$i],'</TD>';
    foreach (1..$cols)
    {
      print qq(<TD WIDTH="$other_col_width" HEIGHT="$row_height">);
      $ii = ($i-1)*$cols + $_;
      print "\n";
      print qq(<CENTER><A HREF="javascript:void(0);" onClick="imgClick($ii);">);
      print qq(<IMG SRC="$blank_image" BORDER="0"></CENTER></A>);
      print '</TD>';
    }
    print '</TR>'
  }
  print '</TABLE><BR>';
  print "\n",'<A HREF="javascript:void(0);" onClick="checkIt();">CheckIt</A>';
}

sub write_code {
  my($size) = $rows*$cols;
  my($condition) = 'false';
  my($i);
  if ($#correct_answers >= 0) {
    $condition = 'data[' . $correct_answers[0] . ']';
    for ($i = 1; $i <= $#correct_answers; $i++) {
      $condition = $condition . ' && data[' .  $correct_answers[$i] . ']';
    }
  }
  print <<END;
<SCRIPT LANGUAGE="JavaScript" TYPE="text/javascript">

var data = new Array($size);

// helper only routine
function writeCorrect() {
  var cor_enum = "";
  for( var i=0; i<$size; i++ ) {
    if( data[i] == true )
      cor_enum = cor_enum + i + ",";
    }
  alert(cor_enum);
  document.forms[0].correct_answers.value = cor_enum;
  document.forms[0].Submit();
}

function imgClick( par ) {
  if( data[par-1] == true ) {
    document.images[par-1].src = "$blank_image";
    data[par-1] = false;
  }
  else {
    document.images[par-1].src = "$check_image";
    data[par-1] = true;
  }
}

function checkIt( par ) {
  var rv = 0;
  var tt = false;
  for( var i=0; i<$size; i++ ) {
    if( data[i] == true )
      rv++;
  }
  tt = $condition;
  if( rv == ($#correct_answers+1) && tt ) {
    //document.forms[0].reply.value = "Верно";
   alert("Correct:"+rv);
  }
  else {
    //var t = data[0]+" "+data[3]+" "+data[11]+" "+data[12]+" "+data[24];
    alert("Wrong:");
    //document.forms[0].reply.value = "Неверно";
  }
}

// init
for( var i=0; i<$size; i++) {
  data[i] = false;
}  

var img = new Image();
img.src = "$check_image";
</SCRIPT>
END
}

sub setup_defaults {
  print "setup_defaults works<BR>";
  $cols = 5;
  $rows = 5;
  $first_col_width = 200;
  $other_col_width = 100;
  $row1_height = 20;
  $row_height = 20;
  foreach (1..$cols)
  {
    $col_head[$_] = "head $_";
  }
  foreach (1..$rows)
  {
    $row_head[$_] = "row $_";
  }
}