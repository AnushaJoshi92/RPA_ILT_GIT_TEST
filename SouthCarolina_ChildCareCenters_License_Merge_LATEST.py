import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# df1= pd.read_csv(r"C:\Users\Administrator\Desktop\Endeavour_SouthCarolina_WebScraping\Endeavour_SouthCarolina_WebScraping\Results\SouthCarolina_ChildCareCenters.csv")
# df2= pd.read_csv(r"C:\Users\Administrator\Desktop\Endeavour_SouthCarolina_WebScraping\Endeavour_SouthCarolina_WebScraping\Results\SouthCarolina_LicenseDetails.csv")

df1= pd.read_csv(r"C:\Users\anusha_chandrakanth\OneDrive - Merilytics\Desktop\Endeavour_WebScraping\Endevor\Endeavour_SouthCarolina_WebScraping\SouthCarolina_ChildCareCenters.csv")
df2= pd.read_csv(r"C:\Users\anusha_chandrakanth\OneDrive - Merilytics\Desktop\Endeavour_WebScraping\Endevor\Endeavour_SouthCarolina_WebScraping\SouthCarolina_LicenseDetails.csv")


df1= df1.rename(columns={'License Info':'License Number'})
# Remove leading whitespace 
df1['Provider Name'] = df1['Provider Name'].str.lstrip()
# Remove trailing whitespace 
df1['Provider Name'] = df1['Provider Name'].str.rstrip()
# Remove leading whitespace 
df2['Provider Name'] = df2['Provider Name'].str.lstrip()
# Remove trailing whitespace
df2['Provider Name'] = df2['Provider Name'].str.rstrip()

# Remove leading whitespace 
df1['License Number'] = df1['License Number'].str.lstrip()
# Remove trailing whitespace 
df1['License Number'] = df1['License Number'].str.rstrip()

# Remove leading whitespace 
df2['License Number'] = df2['License Number'].str.lstrip()
# Remove trailing whitespace 
df2['License Number'] = df2['License Number'].str.rstrip()

df2= df2.rename(columns={'License Number':'License Number'})

final_df=pd.DataFrame()
final_df= pd.merge(df1,df2,on=['Provider Name','License Number'],how='left')
final_df.drop(columns=['Unnamed: 16'],inplace=True)

final_df_v2= final_df.copy()

for index, row in final_df.iterrows():
    current_string = row['Provider Name']
    for other_index, other_row in final_df.iterrows():
        if index != other_index:  # Avoid comparing the string with itself
            similarity_score = fuzz.ratio(current_string, other_row['Provider Name'])
            if similarity_score >= 90:
                final_df.at[index, 'similar_to'] = other_row['Provider Name']
                final_df.at[index, 'similarity_score'] = similarity_score 
                # Replace the current string with the similar one
                final_df.at[index, 'Provider Name'] = other_row['Provider Name']

final_df=final_df.rename(columns={'Provider Name':'Provider Name2'})
final_df_v2= pd.concat([final_df_v2,final_df['Provider Name2']],axis=1)

final_df_v2.to_excel("SouthCarolina_ChildCareCenters_Final.xlsx")
# final_df_v2.to_excel(r"C:\Users\anusha_chandrakanth\OneDrive - Merilytics\Desktop\Endeavour_WebScraping\Endevor\Endeavour_SouthCarolina_WebScraping\SouthCarolina_LicenseDetails_20240315.xlsx")
