# influxDB SDK
#### 主要功能
1、函数`get_new_set_data`查询最新的测点数据或查询某个时刻的测点数据

    Args:
        database (str): 数据库名。必填参数
        tableName (str): 表名。必填参数
        queryTime (str, optional): 查询时刻。默认值为None，表示查询最新时间。
            格式要求：'YYYY-MM-DD HH:mm:ss'。
        pointList (list[str]): 一个或多个点号。必填参数，表示查询所有点。
        influxDB (InfluxDBClient): 数据库连接对象。必填参数，表示使用默认连接。

    Returns:
        Any: 查询结果，具体类型取决于查询内容和返回的数据结构。

    说明：
        本函数可同时满足以下四个场景要求：
        1. 获取一个点的最新值。
        2. 获取一个点在特定时刻的值。
        3. 获取多个点的最新值。
        4. 获取多个点在特定时刻的值。
2、函数`get_new_data_map`查询最新的测点数据或查询某个时刻的测点数据，返回字典

    Args:
            database (str): 数据库名。
            tableName (str): 表名。
            queryTime (str, optional): 查询时刻。默认为None，表示查询最新时间。格式应为'YYYY-MM-DDTHH:MM:SSZ'。
            pointList (List[str], optional): 一个或多个点号。默认为None，表示查询所有点。
            influxDB (object, optional): 数据库连接对象。默认为None，表示使用默认连接。

    Returns:
        Dict: 字典，包含查询结果的键值对。
3、函数`get_his_set_data_by_complete`查询历史时间段一个或多个测点数据（进行数据补齐）
    
    可同时满足下面4个场景要求：
    1、获取一个[点]的[开始，结束]段的历史数据;
    2、获取一个[点]的[开始，结束]段的[间隔秒]的历史数据;
    3、获取多个[点...] 的[开始，结束] 段的历史数据;
    4、获取多个[点...] 的[开始，结束] 段的[间隔秒] 的历史数据;

    Args:
        database (str): 数据库名，必填参数
        tableName (str): 表名，必填参数
        startTime (str): 开始时间，必填参数，表示使用当前时间。
        endTime (str): 结束时间，必填参数，表示使用当前时间。
        pointList (list of str): 一个或多个点号列表，必填参数，表示查询所有点。
        interval (int, optional): 时间间隔（单位秒），默认为None，表示不使用间隔查询。
        influxDB (InfluxDBClient): InfluxDB连接对象，必填参数，表示使用默认连接。

    Returns:
        dict: 包含查询结果的字典，具体结构根据实际应用情况确定。
4、函数`get_his_set_data`查询历史一个或多个测点数据（不进行数据补齐）

    Args:
        database (str): 数据库名，必填参数
        tableName (str): 表名，必填参数
        startTime (str): 开始时间，必填参数(格式要求："2023-12-27 13:42:00")
        endTime (str): 结束时间，必填参数(格式要求："2023-12-27 13:42:00")
        pointList (List[str]): 一个或多个点号，必填参数
        influxDB (InfluxDBClient): 数据库连接，必填参数

    Returns:
        str: 查询结果
5、函数`write_history_data_to_csv`将历史时间段一个或多个测点数据写入到CSV文件中（进行数据补齐）
    
    可同时满足下面4个场景要求：
    1、获取一个点的[开始，结束]段的历史数据;
    2、获取一个点的[开始，结束]段的[间隔秒]的历史数据;
    3、获取多个点...的[开始，结束]段的历史数据;
    4、获取多个点...的[开始，结束]段的[间隔秒]的历史数据;

    Args:
        database (str): 数据库名，必填参数
        tableName (str): 表名，必填参数 (在InfluxDB中通常是measurement名)
        startTime (str): 开始时间，必填参数(格式要求："YYYY-MM-DD HH:mm:ss")
        endTime (str): 结束时间，必填参数(格式要求："YYYY-MM-DD HH:mm:ss")
        pointList (List[str]): 一个或多个点号（测点标识），必填参数
        interval (int): 时间间隔（单位秒），必填参数
        batchSize (int): 当点位过多时，分批处理数量，选填参数，默认100
        influxDB (InfluxDBClient): InfluxDB客户端连接，必填参数
        filePath (str): 文件路径，必填参数，例如："D:\\temp\\202401.csv" 或 "/opt/202401.csv"