# importing libraries
import pandas as pd # data preparation
from helpers.helpers import check_df,retail_data_prep # dataframe operations
from mlxtend.frequent_patterns import apriori, association_rules # apriori algorithm and association rules



# importing data
df_ = pd.read_excel('datasets/online_retail_II.xlsx')
df = df_.copy()
# dropping na's , reducing outliers
dfa = retail_data_prep(df)

# choosing country as germany
df_gr = dfa[dfa['Country'] == "Germany"]

df_gr.head()

# checking df.
check_df(df_gr)


# dropping postage. it is shown as product but has no monetary value.
df_gr = df_gr[~(df_gr['StockCode']=='POST')]
check_df(df_gr)

# creating arl matrix
matrix = df_gr.groupby(['Invoice', "StockCode"])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)
matrix.iloc[0:5, 0:5]

# sample user ids for suggestions
product_ids = [21987,21577,22747,21700]

# function to get product names with stock code
def get_name(dataframe,stock_code):
    try:
        a = dataframe[dataframe['StockCode'] == stock_code]['Description'].values[0]
        return a
    except IndexError:
        print('product cant found')

for i in product_ids:
    print(get_name(df_gr,i))

# creating support values with apriori
itemsets = apriori(matrix,min_support=0.01,use_colnames=True)
itemsets.head()
itemsets.sort_values('support' , ascending = False).head(7)
get_name(df_gr,22326)

# creating association rules
rules = association_rules(itemsets,metric='support', min_threshold=0.01)
rules.head()
rules.sort_values('support', ascending = False).head(7)
rules.sort_values('lift', ascending = False).head(7)

#sorting the rules
sorted_rules = rules.sort_values('lift', ascending = False)
sorted_rules.head()

# giving advices to specific products.
def give_advice(sorted_rules,product_id,number=1):
    advice_list=[]
    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_id:
                advice_list.append(list(sorted_rules.iloc[i]["consequents"])[0])
    return advice_list[0:number]


for i in users_ids:
    print(f'for product : {get_name(df_gr,i)}, adviced product is =', give_advice(sorted_rules, i))

get_name(df_gr,21988)
get_name(df_gr,21576)
get_name(df_gr,22745)
get_name(df_gr,22353)





