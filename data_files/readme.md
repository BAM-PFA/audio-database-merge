# Data files

In this directory are data files that represent the descriptive data at various stages in cleaning, as well as database exports and SQL statements used to test and export data from MySQL.

There are two raw data exports, one from Piction and one from FileMaker. There are also cleaned up CSV versions of both of these files, with data split into multiple columns as needed. There is also an OpenRefine project file that includes the edits I used to clean up data further after combining the data sources, and the CSV export from OpenRefine that is the source for the MySQL database. 

`exportTables.sql` includes a set of statements you can use to export each table to a separate CSV. In my case I needed it for import into FileMaker. Cool tip: you can copy and paste the whole deal including commented lines into the MySQL CLI! Note that you will probably need to modify (or create) `~/.my.cnf` to allow MySQL to write to a file. In my case that file looks like: 

```
[mysqld]
secure_file_priv               = '/Users/michael/'
```

You should be able to generate our MySQL db using `audio_db_dump.sql`.