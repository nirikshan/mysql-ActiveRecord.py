class Sql:
  
  def __init__(self):
    self.tableName = ''
    self.build     = '';

  def select(self , item):
    self.build += "SELECT "+item
    return self


  def select_distinct(self , item):
    self.build += "SELECT DISTINCT "+item
    return self


  def ActualWhere(self , paired , Type = 'AND' , WhereType = ' WHERE '):
    pairs = []
    for item in paired:
      consition = ('=' in item) or ('>' in item) or ('<' in item)
      value     = paired[item]
      pairs.append(item + ( '' if consition else '=') + ( "'"+str(value)+"'" if type(value) == str else str(value) ) )
    syntax = Type.join(pairs)
    self.build = self.build+WhereType+syntax


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


  def insert(self , TableName , Data):
    Keys  = []
    Value = []
    for item in Data:
      Keys.append(item)
      Value.append(Data[item])
    Keys  = '('+self.AllStr(Keys , '`')+')'
    Value = '('+self.AllStr(Value , "'")+')'
    self.build = 'INSERT INTO `{0}` {1}  VALUES {2} '.format(TableName , Keys , Value)
    return self


  def insert_bulk(self , TableName , DataList):
    Keys      = set()
    BulkValue = []
    for item in DataList:
      Value = []
      for key in item:
        Keys.add(key)
        Value.append(item[key])
      Value = '('+self.AllStr(Value , "'")+')'
      BulkValue.append(Value)
    BulkValue = self.AllStr(BulkValue , "");
    Keys      = '('+self.AllStr(Keys , "`")+')'
    self.build = 'INSERT INTO `{0}` {1}  VALUES {2}'.format(TableName , Keys , BulkValue)
    return self
  

  def update(self , TableName , Data):
    Collection = ''
    for item in Data:
      value = Data[item]
      Collection += ('' if Collection == '' else ' , ')+'`'+str(item)+'` = '+( str(value) if type(value) == int else "'"+str(value)+"'" )
    self.build = 'UPDATE `{0}` SET {1}'.format(TableName , Collection)
    return self

  def update_bulk(self , TableName , Collection , UpdateFrom):
    # I will write this tommorrow
    # Like : INSERT INTO `tb_import` (`id`, `name`, `phone`, `address`) VALUES (1 , 'nirikshan3' , 986 , 'anam') ON DUPLICATE KEY UPDATE name=VALUES(name),phone=VALUES(phone)
    # Because This query performs very fast
    return self


  def get(self):
    return self.build


db = Sql()

# SELECT
#     se.NAME
# FROM
#     Transactions AS td
# INNER JOIN Transaction_Detail AS det
# ON
#     td.ID_Transaction = det.ID_Transaction
# INNER JOIN Services AS se
# ON
#     det.ID_Services = se.ID_Services
# WHERE
#     td.ID_Transaction = 'TRA1'

# result = db.select('id').where({
#   'id':1,
#   'purchase_ID':1,
#   'product_line_ID':15
# })
# print(result.get())

# result = db.select('id').where({
#   'id':1,
#   'purchase_ID':1,
#   'product_line_ID':15
# }).From('Purchase_item_table AS p1')

# print(result.get())


# result = db.select('id').From('Purchase_item_table AS p1').where({
#   'id':1,
#   'purchase_ID':1,
#   'product_line_ID':15
# }).order('p1.id' , ' DESC')



# result = db.select('p1.id , p3.product_name_alias , p1.purchase_ID ').From('Purchase_item_table AS p1').join('purchase as p2', 'p2.id = p1.purchase_ID', 'LEFT').join('product_line_table as p3', 'p3.id = p1.product_line_ID', 'LEFT').where({
#   'p1.id':'',
# }).order('p1.id' , ' ASC')

# result = db.insert('tb_import' , {
#   'name'    :  'Nirikshan',
#   'phone'   :  9861280012,
#   'address' :  'Anamnager'
# })

# result = db.insert_bulk('tb_import' ,[
#    {
#     'name'    :  'Nirikshan',
#     'phone'   :  444475,
#     'address' :  'Anamnager4'
#   },
#   {
#     'name'    :  'Nirikshan2',
#     'phone'   :  12222,
#     'address' :  'Anamnager3'
#   },
#   {
#     'name'    :  'Nirikshan3',
#     'phone'   :  3333656,
#     'address' :  'Anamnager2'
#   }
# ])

# result = db.update('tb_import' , {
#     'name'    :  'Nirikshan3',
#     'phone'   :  555245,
#     'address' :  'Anamnager2'
# }).where({
#   'name':'nirikshan'
# })


result = db.update_bulk('tb_import' , [
   {
    'id'     :  1,
    'name'    :  'Nirikshan',
    'phone'   :  7855525,
    'address' :  'Anamnager4'
  },
  {
    'id'      :  2,
    'name'    :  'Nirikshan2',
    'phone'   :  989999,
    'address' :  'Anamnager3'
  },
  {
    'id'      :  3,
    'name'    :  'Nirikshan3',
    'phone'   :  2223,
    'address' :  'Anamnager2'
  }
] , 'id')



# result = db.select_distinct(' p1.id ,  p1.product_line_ID ,  p3.product_name_alias').From('Purchase_item_table AS p1').join('purchase as p2', 'p2.id = p1.purchase_ID', 'LEFT').join('product_line_table as p3', 'p3.id = p1.product_line_ID', 'LEFT').limit(1)

print(result.get())

# INSERT INTO `tb_import` (`id`, `name`, `phone`, `address`) VALUES (1 , 'nirikshan3' , 986 , 'anam') ON DUPLICATE KEY UPDATE name=VALUES(name),phone=VALUES(phone)
