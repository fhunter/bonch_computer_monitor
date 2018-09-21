<h1>Нагрузка на {{machine}}</h1>
%include menu
%import calendar
%import datetime
%import usage
<table border=0 width=75%>
<thead>
<tr >
<th rowspan=2 width=10%>Дата</th>
<th width=90% colspan=288>Занятость</th>
</tr>
<tr>
%for x in xrange(0,24):
<th width=3.75% colspan=12>{{(x+3)%24}}</th>
%end
</tr>
</thead>
%today = datetime.datetime.today()
%for i in calendar.Calendar().itermonthdates(today.year,today.month):
<tr><td>{{i}}</td>
%users, uptime = usage.getdetailedusage(i, ip)
%for j in xrange(0,288):
%if j in uptime:
	%if j in users:
	<td bgcolor=green>
	%else:
	<td bgcolor=lime>
	%end
%else:
<td>
%end
</td>
%end
</tr>
%end
</table>

%include footer
