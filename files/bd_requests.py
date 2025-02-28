import logging

# def get_data_from_bd(cursor: object, name_table: str, fields:list[str]=None, where_field:str=None, where_values:list=None, group_by:str=None):
#     try:
#         if cursor is None:
#             logging.warning("function get_data_from_bd()")
#             logging.warning("cursor is None")
#             return None           
#         if name_table is None or name_table=="":
#             logging.warning("function get_data_from_bd()")
#             logging.warning("name_table is empty or None")
#             return None
#         command="SELECT "
#         if fields is None:
#             command+=" * "
#         else:
#             for field in fields:
#                 command+=field
#         command+=" FROM "+name_table
#         if where_field!=None:
#             command+=" WHERE "+where_field+" IN ("
#             for value in where_values:
#                 command+=value+","
#             command+=")"
#         if group_by!=None:
#             command+=" GROUP BY "+group_by            
#         cursor.execute(command.format(name_table=name_table))
#         result = cursor.fetchall()
#     except Exception as e:
#         logging.warning("function get_data_from_bd()")
#         logging.warning(e)
#         return None
#     return result  

def get_data_from_bd(cursor: object, name_table: str, fields:list[str]=None, where:list[tuple]=None, group_by:str=None):
    try:
        if cursor is None:
            logging.warning("function get_data_from_bd()")
            logging.warning("cursor is None")
            return None           
        if name_table is None or name_table=="":
            logging.warning("function get_data_from_bd()")
            logging.warning("name_table is empty or None")
            return None
        command="SELECT "
        if fields is None:
            command+=" * "
        else:
            count_fields=len(fields)
            current_field_index=1
            for field in fields:
                command+=field
                if current_field_index<count_fields:
                    command+=","
                current_field_index+=1  
        command+=" FROM "+name_table
        if where!=None:
            command+=" WHERE "
            where_count=1
            for where_field, where_value in where:
                if where_count>=2:
                    command+=" AND "
                if where_value is list:
                    command+=where_field+" IN ("+where_value+")"
                elif where_value is str:
                    command+=where_field+"="+where_value
                where_count+=1
        if group_by!=None:
            command+=" GROUP BY "+group_by      
           
        # cursor.execute(command.format(name_table=name_table))
        cursor.execute(command)
        result = cursor.fetchall()
    except Exception as e:
        logging.warning("function get_data_from_bd()")
        logging.warning(e)
        logging.warning("request in bd: "+command)
        return None
    return result  