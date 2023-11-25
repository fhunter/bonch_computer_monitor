%import settings
<a href="{{settings.PREFIX}}/"><button>Домой</button></a>
%for i in (("d","День"),("w","Неделя"),("m","Месяц"),("y","Год")):
<a href="{{settings.PREFIX}}/{{path}}/{{i[0]}}"><button>
%if period==i[0]:
<b>
%end
{{i[1]}}
%if period==i[0]:
</b>
%end
</font>
</button></a>
