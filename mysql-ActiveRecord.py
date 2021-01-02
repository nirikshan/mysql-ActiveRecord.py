class db:
  
  def __init__(self , devtype = 'prod' ):
    self.cursor        = connection.cursor()
    self.devtype       = devtype
    self.tableName     = ''
    self.build         = ''
    self.inputSet      =  ()
    self.inputSetBulk  =  []
  
  
  def FlushBuild(self):
      self.build        = ''
      self.inputSetBulk = []
      self.inputSet     = ()
  
      
  def select(self , item = '*'):
    self.build += "SELECT "+item
    return self

  def select_distinct(self , item):
    self.build += "SELECT DISTINCT "+item
    return self


  def ActualWhere(self , paired , Type = 'AND' , WhereType = ' WHERE '):
    pairs = []
    for item in paired:
      condition = ('=' in item) or ('>' in item) or ('<' in item)
      value     = paired[item]
      Inputes   = ( "'"+str(value)+"'" if type(value) == str else str(value) ) 
      self.inputSet = self.inputSet + (Inputes ,)
      pairs.append(item + ( '' if condition else '=') + '%s' )
    syntax = Type.join(pairs)
    self.build = self.build + WhereType + syntax


  def where(self , paired):
    self.ActualWhere(paired , ' AND ')
    return self


  def or_where(self , paired):
    HasWhere = 'WHERE' in self.build
    self.ActualWhere(paired , ' OR ' , (' AND ' if HasWhere else ' WHERE '))
    return self


  def From(self , tableName = ''):
    if 'AS' in tableName or 'as' in tableName:
      self.tableName = tableName
    else:
      self.tableName = '`'+tableName+'`'
    self.build += " from "+self.tableName
    return self


  def order(self , feild , orderType):
    HasOrderBy = 'ORDER BY' in self.build 
    self.build += (' , ' if HasOrderBy else ' ORDER BY ' )+feild+' '+orderType
    return self


  def join(self , JoinTable , Conditions , JoinType = 'LEFT'):
    Join = ' '+JoinType+' JOIN '+JoinTable+' ON '+Conditions
    self.build += Join
    return self


  def limit(self , start = '' , end = None):
    self.build += " LIMIT "+str(start)+ (" , "+str(end) if end != None else " ") 
    return self


  def AllStr(self , value , quoType):
    return ','.join( (str(v) if type(v) == int else ""+quoType+""+str(v)+""+quoType+"" ) for v in value)


  def insert(self , TableName , Data , out="result"):
    Keys  = []
    Value = []
    for item in Data:
      Keys.append(item)
      Value.append('%s')
      # self.inputSet.append(Data[item])
      self.inputSet = self.inputSet + (Data[item] ,)
    Keys  = '('+self.AllStr(Keys , '`')+')'
    Value = '('+self.AllStr(Value , " ")+')'
    self.build = 'INSERT INTO `{0}` {1}  VALUES {2} '.format(TableName , Keys , Value)
    if out == "query":
      Build    = self.build
      InputSet = self.inputSet
      self.FlushBuild()
      return [ Build , InputSet ]
    return self.exe(self.build , self.inputSet , 'answer')


  def insert_bulk(self , TableName , DataList , out="result"):
    Keys        = []
    BulkValue   = []
    InputPlaces = []
    for item in DataList:
      Value = ()
      for key in item:
        if not key in Keys:
          Keys.append(key)
          InputPlaces.append(' %s ')
        Value = Value + (item[key] ,)
      self.inputSetBulk.append(Value)
    Keys        = '('+self.AllStr(Keys , "`")+')'
    InputPlaces = '('+self.AllStr(InputPlaces , "")+')'
    self.build = 'INSERT INTO `{0}` {1}  VALUES {2}'.format(TableName , Keys , InputPlaces)
    
    if out == "query":
      Build    = self.build
      InputSet = self.inputSetBulk
      self.FlushBuild()
      return [ Build , InputSet ]
    return self.exe(self.build , self.inputSetBulk , 'answer' , True)


  def update(self , TableName , Data , out="result"):
    Collection = ''
    UpdateValue = ()
    for item in Data:
      value = Data[item]
      UpdateValue = UpdateValue + (value , )
      Collection += ('' if Collection == '' else ' , ')+' `'+str(item)+'` = %s'
    self.inputSet = UpdateValue + self.inputSet
    self.build = ('UPDATE `{0}` SET {1}'.format(TableName , Collection)) + self.build
    if out == "query":
      Build    = self.build
      InputSet = self.inputSet
      self.FlushBuild()
      return [ Build , InputSet ]
    return self.exe(self.build , self.inputSet , 'answer')
    
  def getBulkUpdateEnd(self , Keys , UpdateFrom):
    dataSet = ''
    for item in Keys:
      if not item == UpdateFrom:
        dataSet = ('`{0}` = VALUES({1})'.format(item , item))+ ( '' if not dataSet else ' , ' ) + dataSet
    return(' ON DUPLICATE KEY UPDATE {0} '.format(dataSet))
    
    
    
  def update_bulk(self , TableName , Collection , UpdateFrom = None , out = "result"):
    if not UpdateFrom :
      return False
    Keys        = []
    BulkValue   = []
    InputPlaces = []
    for item in Collection:
      Value = ()
      for key in item:
        if not key in Keys:
          Keys.append(key)
          InputPlaces.append(' %s ')
        Value = Value + (item[key] ,)
      self.inputSetBulk.append(Value)
    UpdateLayer = self.getBulkUpdateEnd(Keys  , UpdateFrom)
    Keys        = '('+self.AllStr(Keys , "`")+')'
    InputPlaces = '('+self.AllStr(InputPlaces , "")+')'
    self.build = 'INSERT INTO `{0}` {1}  VALUES {2} {3}'.format(TableName , Keys , InputPlaces , UpdateLayer)
    if out == "query":
      Build    = self.build
      InputSet = self.inputSetBulk
      self.FlushBuild()
      return [ Build , InputSet ]
    return self.exe(self.build , self.inputSetBulk , 'answer' , True)



  def get(self , out='result'):
    CurrentBuild = self.build
    CurrentInSet = self.inputSet
    self.FlushBuild()
    if out == 'query':
      return [ CurrentBuild , CurrentInSet]
    return self.exe(CurrentBuild , CurrentInSet)
  
  
  
  def exe(self ,CurrentBuild ,  CurrentInSet , get="data" , many = False):
    self.FlushBuild()
    cursor = self.cursor
    if self.devtype == 'dev':
      if many:
        ans = cursor.executemany(CurrentBuild , CurrentInSet)
      else:
        ans = cursor.execute(CurrentBuild , CurrentInSet)
    else:
      try:
        if many:
          ans = cursor.executemany(CurrentBuild , CurrentInSet)
        else:
          ans = cursor.execute(CurrentBuild , CurrentInSet)
      except:
        ans = False
    if get == 'data':
      return cursor.fetchall()
    return ans    
