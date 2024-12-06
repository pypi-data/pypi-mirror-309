from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import inspect
from sqlalchemy.sql import text
import pandas as pd
from krazy import utility_functions as uf

'''
PostgresSql wrapper functions
For all functions, pass connected engine
'''

def create_connection(username, host, database, password):
    '''
    Create sqlalchemy connection for postgresql
    '''
    url = URL.create(
    drivername="postgresql",
    username=username,
    host=host,
    database=database,
    password=password
)
    return create_engine(url)

def get_schema_names(engine):
    '''
    Takes SQLAlchemy engine and returns schema names as list
    '''
    inspector = inspect(engine)
    return inspector.get_schema_names()

def get_table_names(engine)->dict:
    '''
    Takes SQLAlchemy engine and returns schema wise table names as dictionary
    '''
    inspector = inspect(engine)
    schemas = get_schema_names(engine)
    tables = {}
    for schema in schemas:
        tables[schema] = (inspector.get_table_names(schema=schema))

    return tables

def table_search(table_name: str, engine:create_engine)->list:
    '''
    Searches for given table name in tables on Postgressql Server
    Pass sqlalchemy engine with connection on
    '''

    table_names=get_table_names(engine)
    
    if table_names:
        srch_results = []
        for key in list(table_names.keys()):
            table_names_schema = table_names[key]
            for name in table_names_schema:
                if table_name in name.lower():
                    srch_results.append([key, name])
        return srch_results
    else:
        return None

def get_table_schema(schema:str, table:str, engine:create_engine, df_to_compare=pd.DataFrame())->list[pd.DataFrame, list]:
    '''
    Returns list containing table schema as dataframe and useful columns as list
    '''
    # check if schema and table exists and return schema as dataframe
    tables = get_table_names(engine)
    if table in tables[schema]:
        sql = f'''
        select *
        from information_schema.columns
        where table_schema = '{schema}'
        and table_name = '{table}';
        '''
        df_table_schema = pd.read_sql_query(sql, engine)
        useful_cols = ['table_name', 'column_name', 'udt_name', 'character_maximum_length']

        if df_to_compare.empty:
            pass
        else:
            cols_length = {}
            for col in df_to_compare.columns:
                cols_length[col] = df_to_compare[col].astype(str).str.len().max()
            
            df_table_schema['df_length'] = df_table_schema['column_name'].map(cols_length)
            df_table_schema.loc[df_table_schema['udt_name'].isin(['varchar']), 'Diff'] = df_table_schema.loc[df_table_schema['udt_name'].isin(['varchar']), 'character_maximum_length'] - df_table_schema.loc[df_table_schema['udt_name'].isin(['varchar']), 'df_length']

            useful_cols.append('df_length')
            useful_cols.append('Diff')

        return [df_table_schema, useful_cols]

    else:
        print(f'Table: {table} not found in schema: {schema}')
        return [None, None]

def table_delete(schema, table_name, engine:create_engine)->None:
    '''
    Deletes given tabe on postgresql server
    '''
    
    table_list = table_search(table_name, engine)
    
    cur = engine.connect()
    cur.execute(text(f'Drop table if exists "{schema}".{table_name};'))
    cur.commit()

def create_table(df:pd.DataFrame, schema, table_name, engine:create_engine)->None:
    '''
    Creates table in Postgresql server based on dataframe supplied
    '''

    df_dtypes = uf.dtype_to_df(df)

    df_dtypes['Data type'] = ''
    
    for ind, row in df_dtypes.iterrows():
        if row['Type'] == 'datetime64[ns]':
            df_dtypes.loc[ind, 'Data type'] = 'date'
        elif row['Type'] == 'float64':
            df_dtypes.loc[ind, 'Data type'] = 'float8'
        elif row['Type'] == 'float':
            df_dtypes.loc[ind, 'Data type'] = 'float8'
        elif row['Type'] == 'int':
            df_dtypes.loc[ind, 'Data type'] = 'int8'
        elif row['Type'] == 'int64':
            df_dtypes.loc[ind, 'Data type'] = 'int8'
        elif df[row['Col']].astype(str).str.len().max() <= 90:
            max_len = df[row['Col']].astype(str).str.len().max()
            df_dtypes.loc[ind, 'Data type'] = f'varchar({max_len+10})'
        else:
            df_dtypes.loc[ind, 'Data type'] = 'text'

    col_string = []
    for ind, row in df_dtypes.iterrows():
        col_string.append(f'''"{row['Col']}" {row['Data type']}''')

    col_string = ', '.join(col_string)

    sql = f'Create table "{schema}".{table_name} ({col_string});'
    
    with engine.begin() as conn:
        conn.execute(text(sql))    
    
    # cur = engine.connect()
    # cur.execute(sql)
    # cur.commit()

def dbase_col_checker_adder(schema:str, table_name:str, df_to_compare:pd.DataFrame, engine, speak=False)->None:

    '''Checks if all columns in df exists in database and adds it not'''

    # check if schema exists
    if schema not in get_schema_names(engine):
        if speak:
            print(f'Schema {schema} does not exist')
        return None
    # check if table exists
    if table_name not in get_table_names(engine)[schema]:
        if speak:
            print(f'Table {table_name} does not exist')
        return None

    # get table schmea
    results = get_table_schema(schema, table_name, engine, df_to_compare)

    # get results
    df_compared = results[0]

    # get columns to add
    df_cols = uf.dtype_to_df(df_to_compare)
    df_col_diff = df_cols.loc[~df_cols['Col'].isin(df_compared['column_name'].tolist())]

    df_postgrest_col_dict = {
        'datetime64[ns]':'date',
        'float64': 'float8',
        'int':'int8',
        'int64':'int8',
        'object':'text'
    }

    if df_col_diff.empty:
        if speak:
            print('No new columns to add in db')
        return None
    else:
        # add columns
        cur = engine.connect()
        for ind, row in df_col_diff.iterrows():
            cur.execute(text(f'''alter table "General".cc_consolidated add column if not exists "{row['Col']}" {df_postgrest_col_dict[str(row['Type'])]} null;'''))
            cur.commit() 
        if speak:
            print(f'New columns added: {df_col_diff['Col']}')

        return df_col_diff['Col'].tolist()


def dbase_writer(df: pd.DataFrame, schema, table, engine:create_engine, append=True)->None:
    '''
    writes data to table. Accepts following arguments for append:
    True = append to existing data
    False = deletes all rows and then insert data into existing table
    delete_table = delete table, recreate table and writes data
    '''
    cur = engine.connect()

    if schema not in get_schema_names(engine):
        print(f'Schema {schema} does not exist')
        return None
    
    tables = get_table_names(engine)

    if append=='delete_table':
        
        # delete table
        table_delete(schema=schema, table_name=table, engine=engine)
        print(f'Table: {table} deleted')

        # create table
        create_table(df, schema, table, engine)
        print(f'Table: {table} re-created')

    elif append==False:
                        
        # delete rows
        cur.execute(text(f'Delete from "{schema}".{table};'))
        print(f'Deleted all data from table: {table}')

    else:
        pass

    # check and add columns
    new_cols = dbase_col_checker_adder(schema, table, df, engine, speak=False)
    if new_cols is not None:
        print(f'New columns added: {new_cols}')

    # write to db
    df.to_sql(table, engine, if_exists='append', index=False, schema=schema)

    print(f'Data written to table {table}')

def build_sql_select(cols:list, table:str, schema:str, follow_through:str=None)->str:
    '''
    builds select sql string based on table name, schema and follow_through given
    '''
    cols = '","'.join(cols)
    if follow_through:
        if cols=='*':
            sql = f'select * from "{schema}".{table} {follow_through};'
        else:
            sql = f'select "{cols}" from "{schema}".{table} {follow_through};'
    else:
        if cols=='*':
            sql = f'select * from "{schema}".{table};'
        else:
            sql = f'select "{cols}" from "{schema}".{table};'

    return sql

