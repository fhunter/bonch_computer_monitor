# Do this:

```
sqlite3 database.sqlite3 "update machines set room='a437' where hostname like 'a437%';"
sqlite3 database.sqlite3 "update machines set room='a439' where hostname like 'a439%';"
sqlite3 database.sqlite3 "update machines set room='a441' where hostname like 'a441%';"
sqlite3 database.sqlite3 "update machines set room='a443' where hostname like 'a443%';"
sqlite3 database.sqlite3 "update machines set room='a445' where hostname like 'a445%';"
```

After registering other machines

#TODO
This needs refactoring. BADLY.

