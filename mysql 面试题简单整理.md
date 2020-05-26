1. 有一张充值表 `vouch(id, uid, amount, vouch_time, mobile)`，其字段分别是：ID，用户ID，充值金额，充值时间，手机号：

   1. 查询在 2018年2月份内充值总额总数大于10000元的前十名的 uid 及其充值总额：

      ```
      mysql> select uid, sum(amount) as s from vouch where vouch_time like "2018-2%" group by uid having s>=10000 limit 10;
      ```

   2. 导出 excel 文件，数据包含所有玩家的 id，充值金额，充值时间及手机号，注意手机号需隐藏中间四位号码：

      ```
      mysql> select uid,sum(amount), group_concat(vouch_time), group_concat(distinct insert(mobile,4,4,"****")) as mobile from vouch group by uid into outfile "/Desktop/marvelous.csv";
      ```

      * Remark：`into outfile`需要有导出文件权限，否则会报错：

        ```
        ERROR 1290 (HY000): The MySQL server is running with the --secure-file-priv option so it cannot execute this statement
        ```
        
        解决方案：
        
        ```
        (1). 使用命令 mysql --help|grep "my.ini"或者 "my.cnf" 查询 mysql 的默认配置文件顺序.
        (2). 选择第一个 "my.ini" 或者 "my.cnf", sudo vim 这个文件。
        (3). 在 [mysqld] 修改 secure_file_priv=''，至自己被赋予 777 权限的目录。
        (4). 在修改过程中，需保持 mysql 服务端全程关闭。
        (5). 重启服务，修改生效。
        ```
   3. 查询充值总额大于10000元的前十名uid与充值总额，并标明序号（倒排序）：

      ```
      mysql> select a.*, @rank:=@rank + 1 as uid_number from (select uid,sum(amount) as s from vouch group by uid having s >= 10000 order by s desc) as a, (select @rank:=0) as b;
      ```

   4. 简述 mysql 索引优化基本原则。

      ```
      1. 避免使用 select * 或者尽量使用 limit。
      2. 查询的缓存设置。
      3. 将数据类型进行优化。
      4. char 代替 varchar，
      5. 组合索引代替单列索引（因为mysql遍历智能使用一次索引）.
      6. 连表代替子查询。
      7. 重复性高的列不适宜建立索引.
      ```
      
   5. 简述 mysql 无法命中索引的几种情况：

      ```
      1. 所查询的列不是创建索引的列（本质上相当于没有创建索引）。
      2. 对于创建索引的列，使用运算或者内置函数（计算机会将所有值的运算重新计算，本质上相当于没有创建索引）。
      3. 遍历创建索引的列时，此列的重复率过高（因为需要筛选的条件多，所以需要显示大量数据，这与没有创建索引的筛		选效果是几乎相同的）。
      4. 遍历创建索引的列，此列存在一个取值范围，并且这个范围过大（原因同上）。
      5. 存在逻辑运算 and 或者 or：
      	5.1 使用 and 联合的字段只需有一个存在索引，便可以命中索引。
      	5.2 使用 or 联合的字段必须所有字段都存在索引，才可命中索引。(计算机会优先识别存在索引的并且查找最快的			字段，并优先根据这个字段进行查找。)
      6. 联合索引：
      	6.1 对于联合索引中的其中一个字段出现了范围查找（原因同上述范围查找）。
      	6.2 联合索引遵循最左前缀原则，即第一个出现索引的字段必须存在值，否则索引不命中。
      	6.3 遍历联合索引的字段，使用 and 命中，使用 or 不命中（分开索引相当于遍历多个表）。
      	6.4 联合索引查找效率高于单目标索引
      ```

   6. 简述 mysql 存储引擎。

      ```
      1. InnoDB：5.6 及以上默认存储引擎，数据库存储形式为 b+ 树。
      2. Myisam：5.5 及以下默认存储引擎。数据库存储形式为 b+ 树。
      3. Memory：数据库信息保存在内存中，hash 存储：
      ```

      Remark：InnoDB 与 Myisam 的区别：

      |                      | MyISAM                                                       | InnoDB                                                       |
      | -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
      | 存储结构             | 每张表被存放三个文件：1.frm-表格定义，2.MYD-数据文件，3.MYI-索引文件 | 所有的表都保存在同一个(一组)数据文件中(也可能是多个文件，或者是独立的表空间文件)，InnoDB 表的大小只受限于操作系统文件的大小，一般为 2G。 |
      | 存储空间             | MyISAM可被压缩，存储空间较小                                 | InnoDB 的表需要更多的内存和存储，它会在住内存中建立其专用的缓冲池用于高速缓冲数据和索引. |
      | 可移植性，备份，恢复 | 数据以文件形式存储，跨平台移植很方便，并且备份以及恢复可对单独的表进行处理。 | 移植与 MyISAM 一致即拷贝数据文件，备份使用 binlog 或者 mysqldump，但不适用于超过数十G大数据量。 |
      | 事务安全             | 不支持事务，每次查询具有原子性。                             | 支持事务，回滚与崩溃修复能力。具有事务安全型表。             |
      | auto_increment       | 自增字段可以与其他字段建立联合索引                           | 必须包含只有该字段的索引。                                   |
      | select               | MyISAM 更优                                                  |                                                              |
      | Insert               |                                                              | InnoDB 更优                                                  |
      | update               |                                                              | InnoDB 更优                                                  |
      | delete               |                                                              | InnoDB 更优，它是逐行删除，不建立新的表。                    |
      | count without where  | MyISAM 更优，因为 MyISAM 保存了数据的具体行数。              | InnoDB 是动态的逐行统计，效率低                              |
      | count with where     | 效率相同                                                     | 效率相同                                                     |
      | 锁                   | 只支持表锁                                                   | 支持表锁与行锁                                               |
      | 外键                 | 不支持                                                       | 支持                                                         |
      | 全文索引             | 支持                                                         | 不支持，但可以通过 Sphinx 获得全文索引                       |

      

   7. 将所有充值金额达到 10000 元的用户的手机号改为 13422343345。

      ```
      update vouch set mobile = 13422343345 where amount >= 10000;
      ```

2. mysql 高可用：

   ```
   https://www.cnblogs.com/itplay/p/10782678.html
   ```

3. 使用 SQLAlchemy 改写下列 SQL 语句：

   ```
   select a.*, classes.c_name from student as a,classes where classes.id = a.classes_id and (select count(*) from student where a.classes_id = student.classes_id and a.score < student.score) < 1;
   ```

   解答：
   
   ```
from sqlalchemy.engine import create_engine
   from sqlalchemy.orm import sessionmaker
   from sqlalchemy import and_
   from 加强练习.做题或写东西的测试.test40 import Classes, Student
   
   engine = create_engine("mysql+pymysql://root:hongwei123@127.0.0.1:3306/testsqlalchemy")
   select_db = sessionmaker(engine)
   db_session = select_db()
   
   final_list = []
   all_students = db_session.query(Student).all()
   for i in all_students:
       target_count = db_session.query(Student).filter(and_(Student.classes_id == i.classes_id, Student.score > i.score)).count()
       if target_count < 1:
           final_list += db_session.query(Student).join(Classes, Classes.id == Student.classes_id).filter(Student.id == i.id).all()
   
   for i in final_list:
       print(i.s_name)
   ```
   
4. 事务的隔离性：

   ```
   事务的基本要素：
   	1、原子性（Atomicity）：事务开始后事务内的所有操作绑定，不停滞在中间环节。事务执行过程中出错，会回滚（		Rollback）到事务开始前的状态。
   	2、一致性（Consistency）：事务开始前和结束后，数据库的完整性约束没有被破坏。
   		* 例：A向B转账，不可能A扣了钱，B却没收到。
   	3、隔离性（Isolation）：同一时间，只允许一个事务请求同一数据，不同的事务之间彼此没有任何干扰。
   		* 例：比如A正在从一张银行卡中取钱，在A取钱的过程结束前，B不能向这张卡转账
   	4、持久性（Durability）：事务完成后，该事务所对数据库所作的更改将被保存到数据库之中，不能回滚
   	
   数据库并发操作锁引发的问题：
   	1. B 读取了 A 未提交的数据：脏读。
   	2. A 第一次读取的数据与第二次读取的数据不一致，其中 B 在两次查询中介入并修改数据：不可重复读。
   	3. A 第一次读取的数据与第二次读取的数据不一致，其中 B 在两次查询中介入并添加或者删除数据：幻读。
   
   四个隔离级别：
     1. 读未提交：可以读到未提交的内容。查询不加锁。
     2. 读提交：只能读到已经提交的内容。(SQL Server 和 Oracle 的默认隔离级别), 通常不加锁，使用快照读。
       * 快照读：读取的是快照版本，也就是历史版本，select 就是快照读。
     3. 可重复读：针对不可重复读的隔离级别，mysql 的默认隔离级别，同样使用快照读，并且在事务启动时，不允许使		用修改操作。
     4. 串行化：所有事务串行执行，牺牲效率保证数据安全。
   ```

   各个安全级别所能避免的并发问题：

   |          | 脏读  | 不可重复读 | 幻读  |
   | -------- | ----- | ---------- | ----- |
   | 读未提交 | False | False      | False |
   | 读提交   | True  | False      | False |
   | 可重复读 | True  | True       | False |
   | 串行化   | True  | True       | True  |

6. 有如下四张表：

   ```
   table1: student(id, s_name)
   table2: classes(id, c_name, teacher_id)
   table3: result(id, student_id, class_id, score)
   table4: teacher(id, t_name)
   ```
   
   1. 写出 mysql 建表语句：
     
      ```
       create table teacher(id int primary key, t_name varchar(15));
         create table student(id int primary key, s_name varchar(15));
         create table classes(id int primary key, c_name varchar(15), teacher_id int, foreign 		 key(teacher_id) references teacher(id) on delete cascade on update cascade);
      create table result(id int primary key, student_id int, class_id int, score int, foreign key(student_id) references student(id) on delete cascade on update cascade, foreign key(class_id) references classes(id) on delete cascade on update cascade);
      ```
   
   2. 查询所有数学成绩好于英语成绩的学生的姓名。
   
      ```
   select a.*, b.English from (select student.id, student.s_name, result.score as math from student,result,classes where student.id = result.student_id and result.class_id = classes.id and classes.c_name = "Math") as a, (select student.id, student.s_name, result.score as English from student,result,classes where student.id = result.student_id and result.class_id = classes.id and classes.c_name = "English") as b where a.id = b.id and a.math > b.English;
      ```
   
   3. 查询所有没有学习过 ‘太白’ 老师的课的学生的姓名。
   
      ```
   select student.s_name from student,result,classes,teacher where student.id = result.student_id and result.class_id = classes.id and classes.teacher_id = teacher.id and teacher.t_name = "太白" and result.score = null;
      ```
   
   4. 查询各门课程的最高分与最低分，并以课程名，课程最高分，课程最低分的顺序显示。
   
      ```
      select m.c_name, m.max, n.min from (select classes.c_name, a.score as max from classes,result as a where classes.id = a.class_id and 1 > (select count(*) from result where a.class_id = result.class_id and result.score > a.score)) as m, (select classes.c_name, b.score as min from classes,result as b where classes.id = b.class_id and 1 > (select count(*) from result where b.class_id = result.class_id and result.score < b.score)) as n where m.c_name = n.c_name;
      ```
   
   5. 使用 sqlalchemy 改写 2。
   
      ```
      from sqlalchemy.engine import create_engine
      from sqlalchemy.orm import sessionmaker
      from sqlalchemy import and_
      from 加强练习.做题或写东西的测试.test54 import Teacher, Classes, Result, Student
      
      engine = create_engine("mysql+pymysql://root:hongwei123@127.0.0.1:3306/test2")
      select_db = sessionmaker(engine)
      db_session = select_db()
      
      students = db_session.query(Student).all()
      classes = db_session.query(Classes).all()
      
      math_score = [db_session.query(Result).filter(and_(Result.student_id == i.id, Result.class_id == j.id, j.c_name == "Math")).all() for i in students for j in classes]
      English_score = [db_session.query(Result).filter(and_(Result.student_id == i.id, Result.class_id == j.id, j.c_name == "English")).all() for i in students for j in classes]
      
      new_math_score = [{"student_id": i[0].student_id, "math_score": i[0].score} for i in math_score if i]
      new_English_score = [{"student_id": i[0].student_id, "English_score": i[0].score} for i in English_score if i]
      
      final_list = [{"student_id": i["student_id"], "math_score": i["math_score"], "English_score": j["English_score"]} for i in new_math_score for j in new_English_score if i["student_id"] == j["student_id"] and i["math_score"] > j["English_score"]]
      
      print(final_list)
      ```
   
   6. 使用 sqlalchemy 改写 3。
   
      ```
      from sqlalchemy.engine import create_engine
      from sqlalchemy.orm import sessionmaker
      from sqlalchemy import and_
      from 加强练习.做题或写东西的测试.test54 import Teacher, Classes, Result, Student
      
      engine = create_engine("mysql+pymysql://root:hongwei123@127.0.0.1:3306/test2")
      select_db = sessionmaker(engine)
      db_session = select_db()
      
      students = db_session.query(Student).filter(and_(Student.id == Result.student_id, Result.class_id == Classes.id, Classes.teacher_id == Teacher.id, Teacher.t_name == "太白", Result.score is None)).all()
      print(students)
      ```
   
   7. 使用 sqlcalcemy 改写 4。
   
      ```
      from sqlalchemy.engine import create_engine
      from sqlalchemy.orm import sessionmaker
   from sqlalchemy import and_
      from 加强练习.做题或写东西的测试.test54 import Teacher, Classes, Result, Student
      
      engine = create_engine("mysql+pymysql://root:hongwei123@127.0.0.1:3306/test2")
      select_db = sessionmaker(engine)
      db_session = select_db()
      
      def get_max_min_score(judge_string):
          results_list = []
          target = 0
          all_results = db_session.query(Result).all()
          for i in all_results:
              if judge_string.upper() == "max".upper():
                  target = db_session.query(Result).filter(and_(Result.class_id == i.class_id, Result.score > i.score))
              elif judge_string.upper() == "min".upper():
                  target = db_session.query(Result).filter(and_(Result.class_id == i.class_id, Result.score < i.score))
              if target.count() < 1:
                  results_list += db_session.query(Result).join(Classes, Result.class_id == Classes.id).filter(
                      Result.id == i.id).all()
          return results_list
      
      
      class_max_score = get_max_min_score("max")
      class_min_score = get_max_min_score("min")
      sort_class_max_score = sorted([i for i in class_max_score], key=lambda x: x.class_id)
      sort_class_min_score = sorted([i for i in class_min_score], key=lambda x: x.class_id)
      middle_list = list(zip(sort_class_max_score, sort_class_min_score))
      middle2_list = [{"class_id": i[0].class_id, "max_score": i[0].score, "min_score": i[1].score} for i in middle_list]
      
      for i in middle2_list:
          class_name = db_session.query(Classes).filter(Classes.id == i["class_id"]).all()[0].c_name
          i.update({"class_name": class_name})
      
      print(middle2_list)
      ```
      
   8. 对 `student` 表，使用 mysql 自定义函数，展示索引分布情况：
   
      ```
      s_name concat
      字段  id_1 or id_0(多个)
      其中， id_1 为对应字段的 id, id_0 为其余字段的 id
      ```
   
      ```
      create function get_string(name varchar(30), target_id integer) returns varchar(20) character set utf8
          begin
              declare c int;
              select id from student where s_name = name into c;
              if c != target_id then
                  return '0';
              else
                  return '1';
              end if;
          end;
      
      
      select student.id,student.s_name, concat(student.id, '_', get_string(a.s_name, student.id)) as concat1 from student, (select * from student) as a;
      
      select A.s_name,group_concat(A.concat1) from (select student.id,student.s_name, concat(student.id, '_', get_string(a.s_name, student.id)) as concat1 from student, (select * from student) as a) as A group by A.id;
      ```

6. 其余的一些常问的东西：

   1. mysql如何做分页？：

      ```
      mysql数据库做分页用limit关键字，它后面跟两个参数startIndex和pageSize
      ```

   2. 

   ```
   
   2、mysql引擎有哪些，各自的特点是什么？
   innodb和myisam两个引擎，两者区别是
   innodb支持事物，myisam不支持
   innodb支持外键，myisam不支持
   innodb不支持全文索引，myisam支持全文索引
   innodb提供提交、回滚、崩溃恢复能力的事物的安全能力，实现并发控制
   myisam提供较高的插入和查询记录的效率，主要用于插入和查询
   
   3、数据库怎么建立索引
   1
   create index account_index on `table name `(`字段名`(length)
   4、一张表多个字段，怎么创建组合索引
   1
   create index account_index on `table name `(`字段名`，'字段名')
   5、如何应对数据的高并发，大量的数据计算
   1.创建索引
   2.数据库读写分离，两个数据库，一个作为写，一个作为读
   3. 外键去掉
   4.django中orm表性能相关的
   select_related：一对多使用，查询主动做连表
   prefetch_related：多对多或者一对多的时候使用，不做连表，做多次查询
   
   6、数据库内连表、左连表、右连表
   内连接是根据某个条件连接两个表共有的数据
   左连接是根据某个条件以及左边的表连接数据，右边的表没有数据的话则为null
   右连接是根据某个条件以及右边的表连接数据，左边的表没有数据的话则为null
   
   7、视图和表的区别
   视图是已经编译好的sql语句，是基于sql语句的结果集的可视化的表，而表不是
   视图是窗口，表示内容
   视图没有实际的物理记录，而表有
   视图的建立和删除只影响视图本身，不影响对应的表
   
   8、关系型数据库的特点
   数据集中控制
   数据独立性高
   数据共享性好
   数据冗余度小
   数据结构化
   统一的数据保护能力
   
   9、mysql数据库都有哪些索引
   普通索引：普通索引仅有一个功能：加速查找
   唯一索引：唯一索引两个功能：加速查找和唯一约束（可含null）
   外键索引：外键索引两个功能：加速查找和唯一约束（不可为null）
   联合索引：联合索引是将n个列组合成一个索引，应用场景：同时使用n列来进行查询
   
   10、存储过程
   存储过程不允许执行return语句，但是可以通过out参数返回多个值，存储过程一般是作为一个独立的部分来执行，存储过程是一个预编译的SQL语句。
   
   11、sql优化：
   select句中避免使用 '*'
   减少访问数据库的次数
   删除重复记录
   用where子句替代having子句
   减少对表的查询
   explain
   
   12、char和vachar区别：
   char是固定长度，存储需要空间12个字节，处理速度比vachar快，费内存空间
   vachar是不固定长度，需要存储空间13个字节，节约存储空间
   
   13、Mechached与redis
   mechached：只支持字符串，不能持久化，数据仅存在内存中，宕机或重启数据将全部失效
   不能进行分布式扩展，文件无法异步法。
   优点：mechached进程运行之后，会预申请一块较大的内存空间，自己进行管理。
   redis：支持服务器端的数据类型，redis与memcached相比来说，拥有更多的数据结构和并发支持更丰富的数据操作，可持久化。
   五大类型数据：string、hash、list、set和有序集合，redis是单进程单线程的。
   缺点：数据库的容量受到物理内存的限制。
   
   14、sql注入
   sql注入是比较常见的攻击方式之一，针对编程员编程的疏忽，通过sql语句，实现账号无法登陆，甚至篡改数据库。
   防止：凡涉及到执行sql中有变量时，切记不要用拼接字符串的方法
   
   15、什么是触发器
   触发器是一种特殊的存储过程，主要是通过事件来触发而被执行的，他可以强化约束，来维护数据库的完整性和一致性，可以跟踪数据内的操作从而不允许未经许可的 更新和变化，可以联级运算。
   只有表支持触发器，视图不支持触发器
   
   16、游标是什么？
   是对查询出来的结果集作为一个单元来有效的处理，游标可以定在该单元中的特定行，从结果集的当前行检索一行或多行，可以对结果集当前行做修改，
   一般不使用游标，但是需要逐条处理数据的时候，游标显得十分重要
   
   17、 数据库支持多有标准的SQL数据类型，重要分为三类
   数值类型（tinyint，int，bigint，浮点数，bit）
   字符串类型（char和vachar，enum，text，set）
   日期类型（date，datetime，timestamp）
   
   18、mysql慢查询
   慢查询对于跟踪有问题的查询很有用，可以分析出当前程序里哪些sql语句比较耗费资源
   慢查询定义：
   指mysql记录所有执行超过long_query_time参数设定的时间值的sql语句，慢查询日志就是记录这些sql的日志。
   mysql在windows系统中的配置文件一般是my.ini找到mysqld
   log-slow-queries = F:\MySQL\log\mysqlslowquery.log 为慢查询日志存放的位置，一般要有可写权限
   long_query_time = 2 2表示查询超过两秒才记录
   
   19、memcached命中率
   命中：可以直接通过缓存获取到需要的数据
   不命中：无法直接通过缓存获取到想要的数据，需要再次查询数据库或者执行其他的操作，原因可能是由于缓存中根本不存在，或者缓存已经过期
   缓存的命中率越高则表示使用缓存的收益越高，应额用的性能越好，抗病发能力越强
   运行state命令可以查看memcached服务的状态信息，其中cmd—get表示总的get次数，get—hits表示命中次数，命中率=get—hits / cmd—get
   
   20、Oracle和MySQL该如何选择，为什么？
   他们都有各自的优点和缺点。考虑到时间因素，我倾向于MySQL
   选择MySQL而不选Oracle的原因
   MySQL开源
   MySQL轻便快捷
   MySQL对命令行和图形界面的支持都很好
   MySQL支持通过Query Browser进行管理
   
   21、什么情况下适合建立索引？
   1.为经常出现在关键字order by、group by、distinct后面的字段，建立索引
   2.在union等集合操作的结果集字段上，建立索引，其建立索引的目的同上
   3.为经常用作查询选择的字段，建立索引
   4.在经常用作表连接的属性上，建立索引
   
   22、数据库底层是用什么结构实现的，你大致画一下：
   底层用B+数实现，结构图参考：
   http://blog.csdn.net/cjfeii/article/details/10858721
   http://blog.csdn.net/tonyxf121/article/details/8393545
   
   23、sql语句应该考虑哪些安全性？
   1.防止sql注入，对特殊字符进行转义，过滤或者使用预编译的sql语句绑定变量
   2.最小权限原则，特别是不要用root账户，为不同的类型的动作或者组建使用不同的账户
   3.当sql运行出错时，不要把数据库返回的错误信息全部显示给用户，以防止泄漏服务器和数据库相关信息
   
   24、数据库事物有哪几种？
   隔离性、持续性、一致性、原子性
   
   25、MySQ数据表在什么情况下容易损坏？
   服务器突然断电导致数据文件损坏
   强制关机，没有先关闭mysq服务器等
   
   26、drop，delete与truncate的区别
   drop直接删除表
   truncate删除表中数据，再插入时自增长id又从1开始
   delete删除表中数据，可以加where子句
   
   27、数据库范式
   1.第一范式：就是无重复的列
   2.第二范式：就是非主属性非部分依赖于主关键字
   3.第三范式：就是属性不依赖于其他非主属性（消除冗余）
   
   28、MySQL锁类型
   根据锁的类型分：可以分为共享锁、排他锁、意向共享锁和意向排他锁
   根据锁的粒度分：可以分为行锁、表锁
   对于mysql而言，事务机制更多是靠底层的存储引擎来实现的，因此，mysql层面只有表锁，
   而支持事物的innodb存储引起则实现了行锁（在行相应的索引记录上的锁）
   说明：对于更新操作（读不上锁），只有走索引才可能上行锁
   MVCC（多版本并发控制）并发控制机制下，任何操作都不会阻塞读取操作，
   读取操作也不会阻塞任何操作，只因为读不上锁
   共享锁：由读表操作加上的锁，加锁后其他用户只能获取该表或行的共享锁，不能获取排他锁，
   也就是说只能读不能写
   排他锁：由写表操作加上的锁，加锁后其他用户不能获取该表或该行的任何锁，典型mysql事物中的更新操作
   意向共享锁（IS）：事物打算给数据行加行共享锁，事物在给一个数据行加共享锁前必须先取得该表的IS锁
   意向排他锁（IX）：事物打算给数据行加行排他锁，事物在给一个数据行家排他锁前必须先取得该表的IX锁
   29、如何解决MYSQL数据库中文乱码问题？
   1.在数据库安装的时候指定字符集
   2.如果在按完了以后可以更改配置文件
   3.建立数据库时候：指定字符集类型
   4.建表的时候也指定字符集
   
   30、数据库应用系统设计
   1.规划
   2.需求分析
   3.概念模型设计
   4.逻辑设计
   5.物理设计
   6. 程序编制及调试
   7.运行及维护
   ps：数据库常见面试问题总结
   https://yq.aliyun.com/wenji/
   ```

   