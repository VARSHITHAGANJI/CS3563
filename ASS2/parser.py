#Function to get all the lines for a research paper i.e get title,index,ids referenced, authors,venue, year
#The function is taken from stakeoverflow
def getlines(f):
  lines = []
  while True:
      try:
        line = next(f)
        if line != '\n':  
           lines.append(line)
        else:
           yield lines
           lines = []
      except StopIteration:  
        if lines:
           yield lines
        break

from pickletools import int4
import pandas as pd #importing pandas library to work with dataframes
#columns of each research paper(at most because few attributes are missing or unknown)
column_names = ['Title','Authors','Year','Venue','Id','id_ref','Abstract']

#function to get the column to which a line belongs to in the abouve column names
def col_name(line):
  #dictionary to encode 2nd charcter of each line
  col_names = {'*' :'Title','@':'Authors','t':'Year','c':'Venue','index':'Id','%':'id_ref','!':'Abstract'}
  if(col_names.get(line[1:6])):#finding if there is a key with 5 characters i.e index
    return col_names.get(line[1:6])
  else:
    return col_names.get(line[1])

#Function to process lines i.e gives a dictionary with keys as column_names and values are
#corresponding strings in the lines
def process(lines):
  strings = lines #7 or less no of lines
  lines_7 = {}
  id_list = []
  for i in range(len(strings)):
    strings[i] = strings[i].rstrip('\n')
    col = col_name(strings[i])#column_name of each line
    
    if(col=='Id'):
      lines_7['Id'] = strings[i][6:]
      
    if(col == 'id_ref'):
      id_list.append(strings[i][2:])

    if(col!='Id' and col!='id_ref'):
      if(strings[i][2:]!=""):
        lines_7[col]=strings[i][2:]
      elif(strings[2:]=='\n'):
        lines_7[col] = 'Unknown'
  if (id_list) :
    lines_7['id_ref'] = ",". join(id_list)
  for col in column_names:
    if col not in lines_7:
      lines_7[col] = 'Unknown'
  
  return lines_7


location = 'source.txt'
rows = []#list of all rows
with open(location, 'r',encoding='utf-8') as f:
    next(f)#skipping the first line which has only the count of research papers

    for lines in getlines(f):
      row = process(lines)#dictionary of each research paper
      
      rows.append(row)

#creating a dataframe
df = pd.DataFrame(columns = column_names)
#appending rows to dataframe
df = df.append(rows,ignore_index=True)

#Get Authors dataframe having columns Author name
authors = set()
for author_str in df["Authors"]:
  a = author_str.split(",")
  for author in a:
    if(author!=''):
      authors.add(author)



df_authors = pd.DataFrame({"author_name":list(authors)})
#Exporting the df_authors to csv file
df_authors.to_csv('authors.csv',index = False)
#Get Venues dataframe having venue/conference_name
venues = set()
for venue in df["Venue"]:
  venues.add(venue)
df_venues = pd.DataFrame({"venue":list(venues)})
#Exporting the df_venues to csv file
df_venues.to_csv('venues.csv',index = False)

def remove_dup(string):
  queue = set()
  list_strings = []
  for item in string:
    if item not in queue:
        queue.add(item)
        list_strings.append(item)
  return list_strings

#Get authors and index of research paper including the index of contribution
author_rows = []
for i in df[["Id", "Authors"]][df["Authors"]!="Unknown"].iloc:
  a = i[0]

  refs = i[1].split(",")
  refs = remove_dup(refs)
  for i in range(len(refs)):
    if (refs[i]!=''):
      author_rows.append([a,refs[i],i+1])

for i in df[["Id", "Authors"]][df["Authors"]=="Unknown"].iloc:
  a = i[0]
  r = i[1]
  author_rows.append([a,r,1])

df_authored_by = pd.DataFrame(author_rows,columns = ['id','author','contribution'])
df_authored_by['id'] = df_authored_by['id'].astype(str).astype(int)
df_authored_by['contribution'] = df_authored_by['contribution'].astype(str).astype(int)
#Exporting as csv file
df_authored_by.to_csv('authored_by.csv',index = False)

#Get citation dataframe where each row contains paper id and corresponding reference id
id_rows = []
for i in df[["Id", "id_ref"]][df["id_ref"]!="Unknown"].iloc:
  a = i[0]
  r = i[1]
  refs = r.split(",")
  for ref in refs:
    id_rows.append([a,ref])
df_ref = pd.DataFrame(id_rows,columns = ['paper_id_1 ',
	'citationpaper_id_2'])
df_ref = df_ref.astype(str).astype(int)
#Exporting citation dataframe to csv
df_ref.to_csv('citation.csv',index = False)

df = df[['Id','Title','Year','Abstract','Venue']]
df['Year'] = df['Year'].astype(str).astype(int)

#Exporting research paper dataframe into csv
df.to_csv('research.csv',index = False)

