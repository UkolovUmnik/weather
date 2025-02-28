import logging

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
            count_elements=len(fields)
            current_element_index=1
            for field in fields:
                command+=field
                if current_element_index<count_elements:
                    command+=","
                current_element_index+=1  
        command+=" FROM "+name_table
        if where!=None:
            command+=" WHERE "
            where_count=1
            for where_field, where_value in where:
                if where_count>=2:
                    command+=" AND "
                if type(where_value) is list:
                    command+=where_field+" IN ("
                    count_elements=len(where_value)
                    current_element_index=1
                    for element in where_value:
                        command+=str("'"+element+"'")
                        if current_element_index<count_elements:
                            command+=','
                        current_element_index+=1
                    command+=")"
                elif type(where_value) is str:
                    command+=where_field+"="+"'"+where_value+"'"
                elif type((where_value)) is int:
                    command+=where_field+"="+"'"+str(where_value)+"'"
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