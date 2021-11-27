<h1>Статус {{machine}}</h1>
%include menu
%import calendar
%import datetime
%import usage
%import settings
<h2>Uptime</h2>
<img src={{settings.PREFIX}}/graph/{{machine}}_uptime>
<h2>Нагрузка на процессор</h2>
<img src={{settings.PREFIX}}/graph/{{machine}}_cpu>
<h2>Количество пользователей</h2>
<img src={{settings.PREFIX}}/graph/{{machine}}_users>
<h2>Свободное место на scratch</h2>
<img src={{settings.PREFIX}}/graph/{{machine}}_scratch>
<h2>Статус ansible</h2>
<img src={{settings.PREFIX}}/graph/{{machine}}_ansible>

%include footer
