from influxdb_client import InfluxDBClient

def get_field_value_from_influxdb(database: dict, time_start, time_end, fields: list):
    fields_str = ''
    for i in range(len(fields)):
        if i == 0:
            fields_str += f'r._field == "{fields[i]}"'
        else:
            fields_str += f' or r._field == "{fields[i]}"'

    query = (f'from(bucket: "{database["bucket"]}") '
            f'|> range(start: {time_start}, stop: {time_end}) '
            f'|> filter(fn: (r) => {fields_str}) '
            f'|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")  ')


    with InfluxDBClient(url=database['url'], token=database['token'], org=database['org']) as client:
        tables = client.query_api().query(query)


    data_rows = []
    # 遍历查询结果
    for table in tables:
        for record in table.records:
            # 提取时间戳和每个字段的值
            row = []
            row.append(record.get_time().timestamp())
            for field in fields:
                row.append(record.values.get(field))
            
            data_rows.append(row)

    return data_rows