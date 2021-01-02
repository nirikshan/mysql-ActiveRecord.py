# sqlmy

sqlmy is query builder for MY SQL database using python.

## Usage

Example :

```python
from sqlmy.db import db

db = db()

def index(request):
    result = db\
    .select(' p1.name AS ProductName ,  p2.product_name_alias , p4.name AS AssetName , p3.name As CatoName , p6.tax_value , p8.propose_name , p9.company_name , p11.typename')\
    .From('product AS p1')\
    .join('product_line_table as p2', 'p2.product_id = p1.id', 'LEFT')\
    .join('category as p3', 'p3.id = p2.product_category', 'LEFT')\
    .join('product_assets_type as p4', 'p4.id = p1.assete_Id', 'LEFT')\
    .join('Purchase_item_table as p5', 'p5.product_line_ID = p2.id', 'LEFT')\
    .join('tax as p6', 'p6.id = p5.Tax_ID', 'LEFT')\
    .join('depreciation as p7', 'p7.id = p5.depreciation_ID', 'LEFT')\
    .join('product_propose as p8', 'p8.id = p5.product_propose_id', 'LEFT')\
    .join('company_table as p9', 'p9.id = p5.company_id', 'LEFT')\
    .join('store as p10', 'p10.id = p5.store_id', 'LEFT')\
    .join('storeType as p11', 'p11.id = p10.storeType', 'LEFT')\
    .join('purchase_serial_numbers as p12', 'p12.purchase_item_id = p5.product_line_ID', 'LEFT')\
    .get()
    
    print(result)
```

## Examples And It's Output

* select

```python
    result = db.select('p1.id , p3.product_name_alias , p1.purchase_ID ')\
            .From('Purchase_item_table AS p1')\
            .join('purchase as p2', 'p2.id = p1.purchase_ID', 'LEFT')\
            .join('product_line_table as p3', 'p3.id = p1.product_line_ID', 'LEFT')\
            .where({
                'p1.id':'',
            })\
            .order('p1.id' , ' ASC')

    print(result.get())

```

* select_distinct

```python
  
   result = db\
         .select_distinct(' p1.id ,  p1.product_line_ID ,  p3.product_name_alias')\
         .From('Purchase_item_table AS p1')\
         .join('purchase as p2', 'p2.id = p1.purchase_ID', 'LEFT')\
         .join('product_line_table as p3', 'p3.id = p1.product_line_ID', 'LEFT')\
         .limit(1)

```

* insert

```python

    result = db.insert('tb_import' , {
        'name'    :  'Nirikshan Bhusal',
        'phone'   :  99999999,
        'address' :  'Nepal , Kathmandu Anamnager'
    })

```

* update

```python

    result = db.update('tb_import' , {
        'name'    :  'Nirikshan3',
        'phone'   :  555245,
        'address' :  'Anamnager2'
    }).where({
        'name':'nirikshan'
    })

```

* insert_bulk

```python

    result = db.insert_bulk('tb_import' ,[
        {
            'name'    :  'Nirikshan1',
            'phone'   :  444475,
            'address' :  'Anamnager4'
        },
        {
            'name'    :  'Nirikshan2',
            'phone'   :  12222,
            'address' :  'Anamnager3'
        },
        {
            'name'    :  'Nirikshan3',
            'phone'   :  3333656,
            'address' :  'Anamnager2'
        }
    ])

```

* update_bulk

```python

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

```
update data according to id

I am looking for more help...
