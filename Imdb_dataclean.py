

num_range  = movie_data.shape[0]

for i in range(0,num_range):
    
    temp1  = ""
    temp2  = ""
    temp3  = ""
    temp4  = ""
    temp5  = ""
    temp6  = ""
    temp7  = ""
    temp8  = ""
    temp9  = ""
    temp10 = ""
    
    #Genre Data Cleanning
    if (pd.isnull(data.Genre[i]) == False):
        temp1 = data.Genre[i][2:-2]
        temp1 = (temp1.replace('\\n', '').replace('\\xa0', ''))
        data.Genre[i] = temp1
    
    #Director
    if (pd.isnull(data.Director[i]) == False):
        data.Director[i] = data.Director[i][2:-2]
    
    #Language
    if (pd.isnull(data.Language[i]) == False):
        data.Language[i] = data.Language[i][2:-2]
    
    #Keywords
    if (pd.isnull(data.Keywords[i]) == False):
        temp2 = data.Keywords[i][2:-2]
        temp2 = temp2.split(",")
        temp2 = ([x for x in temp2 if "See All" not in x])
        data.Keywords[i] = temp2
    
    #MPAA
    if (pd.isnull(data.MPAA[i]) == False):
        temp3 = data.MPAA[i][71:]
        temp3 = temp3.replace("\\n","").replace("  See all certifications\\xa0»", "")[:-5]
        data.MPAA[i] = temp3
    
    #budget 
    temp4 = data.Budget[i]
    if (pd.isnull(temp4) == False):
        temp4 = re.findall(r'[0-9]+',temp4)
        temp4 = "".join(temp4)
        data.Budget[i] = temp4
    
    #Revenue
    temp5 = data.revenue[i]
    if (pd.isnull(temp5) == False):
        temp5 = re.findall(r'[0-9]+',temp5)
        temp5 = "".join(temp5)
        data.revenue[i] = temp5   
    
    #Actors
    if (pd.isnull(data.Actors[i]) == False):
        temp6 = data.Actors[i][2:-2].split(",")
        temp6 = ([x for x in temp6 if 'See full cast' not in x])
        data.Actors[i] = temp6

    #Writer
    if (pd.isnull(data.writer[i]) == False):
        data.writer[i] = data.writer[i][2:-2]
    
    #Production Company 
    if (pd.isnull(data.Production_Company[i]) == False):
        temp7 = data.Production_Company[i][1:-1]
        temp7 = temp7.replace("\\nSee more\\xa0»" , "")
        data.Production_Company[i] = temp7
   
    #Tagline
    if (pd.isnull(data.Tagline[i]) == False):
        temp8 = data.Tagline[i]
        temp8 = temp8.replace("\n See more\xa0»", "")
        temp8 = temp8.strip()
        
    #Summary 
    if (pd.isnull(data.Summary[i]) == False):
        temp9 = data.Summary[i]
        temp9 = temp9.replace("See full summary\xa0»","").replace("\n","")
        temp9 = temp9.strip()
	
	#No_of_votes 		
	if (pd.isnull(data.No_of_Votes[i]) == False):
        temp10 = (data.No_of_Votes[i].replace(',', ''))
        data.No_of_Votes[i] = temp10
    