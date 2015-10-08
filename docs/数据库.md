
# 数据库

数据库只实现了很简单的一小部分功能。

目前数据库可以在命令行环境下使用。

## 使用方法

在django项目根目录下的python命令行当中：

```
from database import backend, utils
```

即可。

在django其他部分当中使用可能需要一些额外的工作。

## Utils

`setup_test_db()`
    向数据库当中添加一些用于测试的数据。
    
`clean_test_db()`
    将数据库清空。
    
## Backend

接口如同之前所约定的。

`dir(backend)`查看可用的函数即可。