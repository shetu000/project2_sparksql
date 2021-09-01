import pyspark
from pyspark.sql import SparkSession 
from pyspark.sql.types import StructType,StructField,StringType,IntegerType
spark=SparkSession.builder.master("local[1]").appName('Spark Application').getOrCreate()
schema=StructType([StructField("ID",IntegerType(),True), 
    StructField("Name",StringType(),True), 
    StructField("sex",StringType(),True), 
    StructField("Age", IntegerType(), True), 
    StructField("Height", IntegerType(), True),
    StructField("weight",IntegerType(),True), 
    StructField("Team", StringType(), True), 
    StructField("NOC", StringType(), True),
    StructField("Games",StringType(),True), 
    StructField("Year", IntegerType(), True), 
    StructField("Session", StringType(), True),
    StructField("City",StringType(),True), 
    StructField("Sport", StringType(), True), 
    StructField("Event", StringType(), True),
    StructField("Medal", StringType(), True)
    ])

df=spark.read.format("csv").option("header", True).schema(schema).load("athlete_events.csv")
#df.printSchema()

noc_schema = StructType() \
    .add("NOC",StringType(),True) \
    .add("region",StringType(),True) \
    .add("notes",StringType(),True) 
    



df_noc= spark.read.format("csv") \
      .option("header", True) \
      .schema(noc_schema) \
      .load("noc_regions.csv")
df_noc.printSchema()
df_noc.createOrReplaceTempView("noc")

#df.show(10,truncate=False)
df.createOrReplaceTempView("athlete")

# #1) Write a Query to Count Female participants in year 2004 from India?

# query="SELECT COUNT(*)  FROM athlete where Year='2004' and Sex='F' and NOC in ('IND')"
# #-------------------------------------------------------------------------------------------

#2)Wriye a query to fetch top 10 youngest athletes to ever compete in the Games?

query="SELECT name, age, city,Sport FROM athlete \
     where Age is not null \
         Group By Name, age,City,sport ORDER BY age"
##--------------------------------------------------------------------------------------------
# #3) Write a Query to display the Name and year when women get started to enter into olympics?

# query="SELECT Name,Year FROM athlete \
#     WHERE Sex='F'\
#         ORDER BY Year Asc \
#             LIMIT 1"
##----------------------------------------------------------------------------------
# #4) Write a query to Count the number of male and female participants in each sport from 1896 to 2006

# query="SELECT s as Sport,Female_Count, Male_Count from \
#     (SELECT Sport as s, Count(Name)as Female_Count FROM athlete WHERE Sex='F' GROUP BY Sport) \
#         join \
#             (SELECT Sport as p, Count(Name)as Male_Count FROM athlete WHERE Sex='M' GROUP BY Sport) \
#                 on s=p"
##------------------------------------------------------------------------------------------------------
# #5) Write a query to Count the no of Females Participants from each country in every year

# query="SELECT Year,NOC as Country, Count(*) as Total_Female_Count \
#     FROM athlete WHERE Sex='F' \
#         GROUP BY NOC,Year order by Year"
##------------------------------------------------------------------------------------------------
# #6.Write a Query to fetch how many Indian took participated in every year?

# query="SELECT Year,Count(*) as Total_indian_Participants \
#     FROM athlete \
#         WHERE NOC='IND' \
#             GROUP BY Year \
#                 ORDER BY Year Asc" 
##-------------------------------------------------------------------------------------------------
# #8)write a query to display all unique Sports in olympics

# query="select distinct sport from athlete"
##-------------------------------------------------------------------------------------------------
# #9) how many gold medals indian won till 2016
                   
# query="select year,count(medal) as Gold from athlete \
        # where team='India' and medal='Gold' group by year order by year"
# #---------------------------------------------------------------------------------------------------
# #10) count the number of participants in each sport(sport,no_of_participants)

# query=query="select s as sport,F,M from (select sport as s,year,count(sex) as F from athlete where sex='F' and year='2016' group by sport,year) p \
# full join \
# (select sport as sp,year,count(sex) as M from athlete where sex='M' and year='2016' group by sport,year) on s=sp" 
# #------------------------------------------------------------------------------------------------------------------------------------------------------------------
# #11) dispaly details of indian players,who won gold,silver,bronze

# query="select ROW_NUMBER() OVER(order by Total desc,Gold desc,Silver desc,Bronze desc) AS Rank,Name,Sex,Total as Total_Medals,IFNULL(Gold,0) as Gold,IFNULL(Silver,0) as Silver,IFNULL(Bronze,0) as Bronze,Sport,Team as Country \
#         from \
#         (((select Sport,Sex,Name,Team,ID as fid,count(Medal) as Total from athlete where Medal='Gold'or Medal='Silver' or Medal='Bronze' group by ID,Name,Sport,Sex,Team) a0 \
#         left join \
#         (select ID,count(Medal) as Gold from athlete where Medal='Gold' group by ID) a1 \
#         on fid=a1.ID) p \
#         left join \
#         (select ID,count(Medal) as Silver from athlete where Medal='Silver' group by ID) a2 \
#         on fid=a2.ID) q \
#         left join \
#         (select ID,count(Medal) as Bronze from athlete where Medal='Bronze' group by ID) a3 \
#         on fid=a3.ID \
#         where Team='India' \
#         order by Rank"

#-------------------------------------------------------------------------------------------------------------
# #12) write a query to display distinct player their country from India
# query=select distinct Name from athlete where Team='India'
#-------------------------------------------------------------------------------------------------------------
#                 
# #13) display max weight of all time in olympics

#query="select Name,max(weight) as weight,Team as Country,Sport from athlete group by Name,Team,Sport order by weight desc"
#-------------------------------------------------------------------------------------------------------------

# #14) which country received most medals in 2004
# query=select Team as Country,count(Medal) as Total_Medals from athlete where Medal in ('Gold','Silver','Bronze') and Year=2004 group by Team
#-------------------------------------------------------------------------------------------------------------

# #15) In which sport Indian won most medals from 1896-2006
# query=select sport,count(medal) as Total_Medals from athlete where Team='India' and Medal in ('Gold','Silver','Bronze') group by sport order by Total_Medals desc
#-------------------------------------------------------------------------------------------------------------

# #16) in each year, for each country count of male and female  

# query="select r.year as year,IFNULL(F,0) as Female,M as Male from ((select distinct year from athlete) r \
#         left join \
#         (select year,count(sex) as F from athlete where sex='F' group by year) p \
#         on r.year=p.year) \
#         left join \
#         (select year,count(sex) as M from athlete where sex='M' group by year) q \
#         on r.year=q.year order by year"

#-------------------------------------------------------------------------------------------------------------

# #17) write a Query to display all years in which olympics held.
# query="SELECT DISTINCT year \
        # FROM athlete \
        # ORDER BY  year "
#-------------------------------------------------------------------------------------------------------------

# # 18) write a Query to display all the Countries participated in olympics from 1896-2006.
# query="SELECT DISTINCT region AS Country FROM noc ORDER BY Country" 
#-------------------------------------------------------------------------------------------------------------

# # 19) Write a Query to find in which year India got most medals.
# query="SELECT year, count(medal) AS Total_Medals \
        # FROM athlete \
        # WHERE medal IN ('Gold','Silver','Bronze') AND Team='India' \
        # GROUP BY  year \
        # ORDER BY  Total_Medals DESC" 
#-------------------------------------------------------------------------------------------------------------

# # 20) Write a Query to find Total_Medals,Gold Medals,Silver Medals and Bronze of Top 100 olympians with their country Name and sport Name.
# query="SELECT ROW_NUMBER() OVER(order by Total desc,Gold desc,Silver desc,Bronze desc) AS Rank, \
#         Name, \
#         Sex, \
#         Total AS Total_Medals, \
#         IFNULL(Gold,0) AS Gold, \
#         IFNULL(Silver,0) AS Silver, \
#         IFNULL(Bronze,0) AS Bronze, \
#         Sport, \
#         Team AS Country \
#         FROM (((SELECT Sport,Sex,Name,Team,ID AS fid,count(Medal) AS Total \
#         FROM athlete \
#         WHERE Medal='Gold'or Medal='Silver' OR Medal='Bronze' \
#         GROUP BY ID,Name,Sport,Sex,Team) a0 \
#         LEFT JOIN \
#         (SELECT ID,count(Medal) AS Gold \
#         FROM athlete \
#         WHERE Medal='Gold' \
#         GROUP BY  ID) a1 \
#         ON fid=a1.ID) p \
#         LEFT JOIN \
#         (SELECT ID,count(Medal) AS Silver \
#         FROM athlete \
#         WHERE Medal='Silver' \
#         GROUP BY  ID) a2 \
#         ON fid=a2.ID) q \
#         LEFT JOIN \
#         (SELECT ID,count(Medal) AS Bronze \
#         FROM athlete \
#         WHERE Medal='Bronze' \
#         GROUP BY  ID) a3 \
#         ON fid=a3.ID \
#         ORDER BY  Rank "          
#-------------------------------------------------------------------------------------------------------------          
              
# 21) Write a Query to find Total_Medals,Gold Medals,Silver Medals,Bronze Medals of every country in the year 1912 with their rank.
# query=\
#         "SELECT ROW_NUMBER() OVER(order by Total desc,Gold desc,Silver desc,Bronze desc) AS Rank,Country,Total AS Total_Medals, IFNULL(Gold,0) AS Gold, \
#         IFNULL(Silver,0) AS Silver,IFNULL(Bronze,0) AS Bronze \
#         FROM (((SELECT Team AS Country,count(Medal) AS Total \
#         FROM athlete \
#         WHERE Medal IN ('Gold','Silver','Bronze') AND year=1912 \
#         GROUP BY  Team) a0 \
#         LEFT JOIN \
#         (SELECT Team,count(Medal) AS Gold \
#         FROM athlete \
#         WHERE Medal='Gold' AND year=1912 \
#         GROUP BY  Team) a1 \
#         ON Country=a1.Team) p \
#         LEFT JOIN \
#         (SELECT Team,count(Medal) AS Silver \
#         FROM athlete \
#         WHERE Medal='Silver' AND year=1912 \
#         GROUP BY  Team) a2 \
#         ON Country=a2.Team) q \
#         LEFT JOIN \
#         (SELECT Team,count(Medal) AS Bronze \
#         FROM athlete \
#         WHERE Medal='Bronze' AND year=1912 \
#         GROUP BY  Team) a3 \
#         ON Country=a3.Team \
#         ORDER BY  Rank"



spark.sql(query).show(truncate=False)



