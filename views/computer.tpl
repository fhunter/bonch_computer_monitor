%include header
%import settings
%import tpl_utils
<h1>Графики для {{machine}}</h1>
%include graph_menu path="computer/" + attr, period=period

<h2>Нагрузка на процессор</h2>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_cpu1/{{period}}><br/>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_cpu2/{{period}}><br/>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_cpu3/{{period}}>
<h2>Количество пользователей</h2>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_users/{{period}}><br/>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_lpu/{{period}}>
<h2>Свободное место на scratch</h2>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_scratch/{{period}}>
<h2>Статус ansible</h2>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_ansible/{{period}}>
<h2>Время работы</h2>
<img src={{settings.PREFIX}}/graph/i/{{machine}}_uptime/{{period}}>


%def myfunc(e):
%return e[1]
%end
<h2> Использование за {{tpl_utils.period_to_days(period)}} дней</h2>
<table border=1 width=50%>
<thead>
<tr>
<th>Пользователь</th><th>минуты</th>
<tr>
</thead>
<!--- FIXME -->
%popularity.sort(key=myfunc,reverse=True)
%for k in popularity:
<tr>
<td>{{k[0]}}</td><td>{{k[1]}}</td>
</tr>
%end
</table>
%include footer
