<h1>Нагрузка на {{machine}}</h1>
%include menu
%import calendar
%import datetime
%import usage
<table border=1 width=75%>
<thead>
<tr >
<th rowspan=2 width=10%>Дата</th>
<th width=90% colspan=288>Занятость</th>
</tr>
<tr>
%for x in xrange(0,24):
<th width=3.75% >{{(x+3)%24}}</th>
%end
</tr>
</thead>
%today = datetime.datetime.today()
%for i in calendar.Calendar().itermonthdates(today.year,today.month):
<tr><td>{{i}}</td>
<td colspan=24><img src="../image/{{ip}}/{{i}}" width=100% ></td>
</tr>
%end
</table>

%include footer
