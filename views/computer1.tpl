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
<th width=3.75% colspan=12>{{x}}</th>
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
	&nbsp;
	%else:
	<td bgcolor=lime>
	&nbsp;
	%end
%else:
<td>
&nbsp;
%end
</td>
%end
</tr>
%end
</table>

%include footer
