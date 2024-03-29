<h1>Статус {{machine}}</h1>
%include menu
%import calendar
%import datetime
%import usage
%import settings
<h2>Включения компьютера</h2>
%for i in sessions_pc:
{{i}} <br/>
%end
<h2>Пользовательские сессии</h2>
<h3>Открытые</h3>
%for i in sessions_user:
{{i}} <br/>
%end
<h3>Недавние</h3>
%for i in sessions_open:
{{i}} <br/>
%end
<h2>Uptime</h2>
<img src={{settings.PREFIX}}/graph/{{machine}}_uptime/{{period}}>
<h2>Нагрузка на процессор</h2>
<img src={{settings.PREFIX}}/graph/{{machine}}_cpu/{{period}}>
<h2>Количество пользователей</h2>
<img src={{settings.PREFIX}}/graph/{{machine}}_users/{{period}}>
<h2>Свободное место на scratch</h2>
<img src={{settings.PREFIX}}/graph/{{machine}}_scratch/{{period}}>
<h2>Статус ansible</h2>
<img src={{settings.PREFIX}}/graph/{{machine}}_ansible/{{period}}>

%include footer
