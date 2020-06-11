import numpy as np
#import pandas as pd
import os
import shutil
import json
import time
import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
#import matplotlib.dates as mdates
#from datetime import datetime
import math as mate


register_matplotlib_converters
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def populate_reviews_table(conn, name, contorise):
    myfile=name+'_5.json';
    with conn:
        cur=conn.cursor();
        with open(myfile) as f:
            for line in f:
                contorise+=1;
                data=json.loads(line);
            
                length=0;
                incentive=0;
                if ( 'reviewText' in data):
                    x=data['reviewText'].split(' ');
                    length=len(x);
                    for item in x:
                        if (('free' in item.lower())|('discount' in item.lower())|('bonus' in item.lower())|('contest' in item.lower())|('incentive' in item.lower())):
                            incentive=1;
                
                date=data['reviewTime'].replace(',','');
                date=date.split();
                date=date[2]+' '+date[0]+' '+date[1];
            
                verified=0;
                if (data['verified']==True):
                    verified=1;
                
                cur.execute(''' INSERT INTO Reviews(id,product_id,user_id,post_time,rating,length,incentive,verified,category)
                        VALUES(?,?,?,?,?,?,?,?,?) ''',[contorise,data['asin'],data['reviewerID'],date,data['overall'],length,incentive,verified,name]);
    return contorise;       
            
def populate_categories_table(conn):
    with conn:
        cur=conn.cursor();
        cur.execute(''' SELECT DISTINCT category FROM Reviews ''');
        rows=cur.fetchall();
        for row in rows:
            cur.execute(''' INSERT INTO Categories(category) VALUES(?)''',row);

def populate_products_table(conn):
    with conn:
        cur=conn.cursor();
        cur.execute(''' SELECT DISTINCT product_id, category FROM Reviews ''');
        rows=cur.fetchall();
        for row in rows:
            cur.execute(''' INSERT INTO Products(product_id, category) VALUES(?,?) ''',[row[0],row[1]]);
def populate_users_table(conn):
    with conn:
        cur=conn.cursor();
        cur.execute('''SELECT DISTINCT user_id FROM Reviews ''');
        rows=cur.fetchall();
        for row in rows:
            cur.execute(''' INSERT INTO Users(user_id) VALUES(?) ''',(row[0],));



def create_tables(conn):
    with conn:
        database=r"C:\sqlite\db\BigData2020.db"
        conn=create_connection(database);
        cur=conn.cursor();
        
        cur.execute(''' CREATE TABLE IF NOT EXISTS Products(
                product_id text PRIMARY KEY,
                category text )''');
        cur.execute(''' CREATE TABLE IF NOT EXISTS Categories(
            category text PRIMARY KEY ) ''');
        cur.execute(''' CREATE TABLE IF NOT EXISTS Reviews(
            id int PRIMARY KEY,
            product_id text,
            user_id text,
            post_time text,
            rating float,
            length float,
            incentive int,
            verified int,
            category text)''');
        cur.execute(''' CREATE TABLE IF NOT EXISTS Users(
            user_id text PRIMARY KEY)''');
    conn.close();
 



def populate_tables(conn):
    with conn:
        cur=conn.cursor();
        files=['All_Beauty','Digital_Music','CDs_and_Vinyl','Office_Products','Cell_Phones_and_Accessories','Luxury_Beauty','Software','Video_Games','Musical_Instruments','Industrial_and_Scientific'];
        contor=0;
        for file in files:
            contor = populate_reviews_table(conn, file, contor);
        createindex1="CREATE INDEX index_users_1 ON Reviews(user_id)";
        createindex2="CREATE INDEX index_products_1 ON Reviews(product_id)";
        cur.execute(createindex1);
        cur.execute(createindex2);
        populate_categories_table(conn);   
        populate_products_table(conn);   
        populate_users_table(conn);
    conn.close();
        
def create_indexes(conn):
    with conn:
        cur=conn.cursor();
        cur.execute(" CREATE INDEX category_index ON Reviews(category) ");
        cur.execute(" CREATE INDEX index_users ON Reviews(user_id)");
        cur.execute(" CREATE INDEX index_products on Reviews(product_id)");
    conn.close();




# COLLECTIVE REVIEW INFLUENCE ON THE GRADE

        
# Word Count

def Word_Count(p_id,conn):
    with conn:
        cur=conn.cursor();
        cur.execute('''SELECT Bin1,Bin2,Bin3,Bin4,Bin5,Bin6,Bin7,Bin8,Bin9
                FROM
                (
                WITH s1 as
                (
                        SELECT category,Bins,COUNT(*) as nr FROM Reviews
                        GROUP BY category,Bins
                )
                SELECT category, 
                SUM((CASE
                     WHEN Bins=1 THEN nr 
                     ELSE 0 
                END)) AS Bin1,
                SUM((CASE
                     WHEN Bins=2 THEN nr 
                     ELSE 0 
                END)) AS Bin2,
                SUM((CASE
                     WHEN Bins=3 THEN nr 
                     ELSE 0 
                END)) AS Bin3,
                SUM((CASE
                     WHEN Bins=4 THEN nr 
                     ELSE 0 
                END)) AS Bin4,
                SUM((CASE
                     WHEN Bins=5 THEN nr 
                     ELSE 0 
                END)) AS Bin5,
                SUM((CASE
                     WHEN Bins=6 THEN nr 
                     ELSE 0 
                END)) AS Bin6,
                SUM((CASE
                     WHEN Bins=7 THEN nr 
                     ELSE 0 
                END)) AS Bin7,
                SUM((CASE
                     WHEN Bins=8 THEN nr 
                     ELSE 0 
                END)) AS Bin8,
                SUM((CASE
                     WHEN Bins=9 THEN nr 
                     ELSE 0 
                END)) AS Bin9
                FROM s1
                GROUP BY category
                ) a1
                JOIN
                Products p1 ON a1.category=p1.category
                WHERE p1.product_id=?''',(p_id,));
        rows1=cur.fetchall();
        if rows1== None:
            return None;
        cur.execute('''WITH s1 as
                (
                        SELECT Bins,COUNT(*) as nr FROM Reviews
                        WHERE product_id=?
                        GROUP BY Bins
                )
                SELECT 
                SUM((CASE
                     WHEN Bins=1 THEN nr 
                     ELSE 0 
                END)) AS Bin1,
                SUM((CASE
                     WHEN Bins=2 THEN nr 
                     ELSE 0 
                END)) AS Bin2,
                SUM((CASE
                     WHEN Bins=3 THEN nr 
                     ELSE 0 
                END)) AS Bin3,
                SUM((CASE
                     WHEN Bins=4 THEN nr 
                     ELSE 0 
                END)) AS Bin4,
                SUM((CASE
                     WHEN Bins=5 THEN nr 
                     ELSE 0 
                END)) AS Bin5,
                SUM((CASE
                     WHEN Bins=6 THEN nr 
                     ELSE 0 
                END)) AS Bin6,
                SUM((CASE
                     WHEN Bins=7 THEN nr 
                     ELSE 0 
                END)) AS Bin7,
                SUM((CASE
                     WHEN Bins=8 THEN nr 
                     ELSE 0 
                END)) AS Bin8,
                SUM((CASE
                     WHEN Bins=9 THEN nr 
                     ELSE 0 
                END)) AS Bin9
                FROM s1''',(p_id,));
        rows2=cur.fetchall();
        bins=[0,1,2,3,4,5,6,7,8];
        figures,axes = plt.subplots(figsize=(10,4))
        y1=[];
        y2=[];
        print(p_id);
        print(rows1);
        print(rows2);
        for i in range(len(rows2[0])):
            y1.append(rows1[0][i]/sum(rows1[0]));
            y2.append(rows2[0][i]/sum(rows2[0]));
        axes.scatter(bins,y1,color='blue');
        axes.scatter(bins,y2,color='orange');
        axes.set_xlabel('Bins with varying ranges')
        axes.set_ylabel('Percentage of reviews per bin');
        axes.set_title('Word Count Comparison');
#        os.remove(r'C:\Users\vlade\Desktop\UNITN\BD\PROJECT\Create_Databases\My_Website\static\foo1.png');
        transfer=time.time();
        name='foo'+str(transfer)+'.png';
        plt.savefig(name, bbox_inches='tight');
        shutil.move('C:/Users/vlade/Desktop/UNITN/BD/PROJECT/Create_Databases/My_Website/'+name, 'C:/Users/vlade/Desktop/UNITN/BD/PROJECT/Create_Databases/My_Website/static/'+name);
    
        if (sum(rows2[0])>25):
            weird_bins='';
            percentage=0;
            for i in range(len(y1)):
                if ((y1[i]/sum(y1))*1.4 < y2[i]/sum(y2)):
                    print("bin number",i,"has issues");
                    weird_bins=weird_bins+str(i)+',';
                    percentage+=y2[i];
            weird_bins=weird_bins[0:-1];
            select_command=''' SELECT SUM(rating)/COUNT(rating) FROM Reviews
                    WHERE Bins in ('''+weird_bins+''') AND product_id=?'''
            cur.execute(select_command,(p_id,));
            sum_weird=cur.fetchall();
            sum_weird=sum_weird[0][0];
            select_command=''' SELECT SUM(rating)/COUNT(rating) FROM Reviews
                    WHERE Bins NOT IN ('''+weird_bins+''') AND product_id=?''';
            cur.execute(select_command,(p_id,));
            sum_normal=cur.fetchall();
            if (sum_weird!= None):
                sum_normal=sum_normal[0][0];
                print('diff between weird and normal is',abs(sum_weird-sum_normal));
                print('percentage of weird compared to normal is',percentage/sum(y2));
                if (( 0.766 - percentage/sum(y2) * 2.667) < abs(sum_weird - sum_normal)):
                    print('check the reviews with that length');
                    weird_bins=weird_bins.split(",");
                    return [weird_bins, 1, sum_normal,name];
                else:
                    print('let them be');
                    return [weird_bins, 0, sum_normal,name];
            else:
                print('no weird days');
        else:
            print('''the number of reviews is too low to compare with the usual distribution
              however we can try to see what happens''')
            cur.execute(''' SELECT category FROM Products WHERE product_id=?''',(p_id,));
            product_category=cur.fetchall();
            product_category=product_category[0];
            cur.execute(''' SELECT SUM(length)/COUNT(length) FROM Reviews 
                        WHERE category=?''',(product_category[0],)) 
            category_mean=cur.fetchall();
            category_mean=category_mean[0][0];
            cur.execute(''' SELECT * FROM Reviews WHERE product_id=?''',(p_id,));
            rows=cur.fetchall();
            std_dev=0;
            for row in rows:
                std_dev+=(row[5]-category_mean)**2;
            std_dev=std_dev/len(rows);
            percentage=0;
            for row in rows:
                if ((row[5]>(2*std_dev+category_mean)) | (row[5]<(category_mean-2*std_dev))):
                    percentage+=1;
            percentage=percentage/len(rows);
            if(percentage> 0.2):
                print('given the low number of reviews, we cant say much, but its weird'); 
                return 'warning';
            else:
#                return 'okay';
                return None;
        axes.scatter(bins,y1,color='blue');
        axes.scatter(bins,y2,color='orange');

# Rating Trend

def Rating_Trend(p_id,conn):
    with conn:
        cur=conn.cursor();
        cur.execute('''SELECT SUM(rating),COUNT(rating), post_time
                    FROM Reviews
                    WHERE product_id=?
                    GROUP BY post_time
                    ORDER BY post_time
                    ''',(p_id,));
        rows1=cur.fetchall();
        x=[];
        y=[];
        average_post=0;
        for index in range(len(rows1)):
            y.append(rows1[index][1]);
            average_post+=rows1[index][1];
            k=rows1[index][2].split();
            if (len(k[2])==1):
                k[2]='0'+k[2];
            k=k[0]+'-'+k[1]+'-'+k[2];
            x.append(np.datetime64(k));
        figures, axes =plt.subplots(figsize=(10,4));
        axes.set_xlabel('Days across all-time usage')
        axes.set_ylabel('Number of reviews per day');
        axes.set_title('Rating Trend');
        plt.xticks(rotation=45);
        axes.scatter(x,y);
#        os.remove(r'C:\Users\vlade\Desktop\UNITN\BD\PROJECT\Create_Databases\My_Website\static\foo2.png');
        transfer=time.time();
        name='foo'+str(transfer)+'.png'
        plt.savefig(name, bbox_inches='tight');
        shutil.move('C:/Users/vlade/Desktop/UNITN/BD/PROJECT/Create_Databases/My_Website/'+name, 'C:/Users/vlade/Desktop/UNITN/BD/PROJECT/Create_Databases/My_Website/static/'+name);
        average_post=average_post/len(rows1);
        standard_dev=0;
        for index in range(len(rows1)): 
            standard_dev+=(rows1[index][1]-average_post)**2;
        standard_dev=mate.sqrt(standard_dev)/(len(rows1));
        average_weird_post_rating=0;
        contor_weird_days=0;
        average_normal_post_rating=0;
        weird_days_list=[];
        for index in range(len(rows1)):
            if(rows1[index][1] > (average_post+2*standard_dev)):
                print(rows1[index][1],average_post)
                average_weird_post_rating+=rows1[index][0]/rows1[index][1];
                contor_weird_days+=1;
                weird_days_list.append(rows1[index][2]);
            else:
                average_normal_post_rating+=rows1[index][0]/rows1[index][1];
        if(contor_weird_days!=0):
            print(contor_weird_days);
            average_weird_post_rating=average_weird_post_rating/contor_weird_days;
            average_normal_post_rating=average_normal_post_rating/(len(rows1)-contor_weird_days);
    #        print(' the percentage of weird days is', contor_weird_days*100/len(rows1));
    #        print('the mean of weird days is',average_weird_post_rating);
    #        print('the mean of normal days is',average_normal_post_rating);
            weird_days_percentage=contor_weird_days/len(rows1);
            avg_normal_rating=average_normal_post_rating/(len(rows1)-contor_weird_days);
            if (0.9 - 8* weird_days_percentage < average_weird_post_rating):
                return [weird_days_list,1,avg_normal_rating,name];
            else:
                return [weird_days_list,0,avg_normal_rating,name];
        else:
            print('nimic gresit aiciea');
           

# User Overlapping History

def User_Overlapping_History(p_id,conn):
    with conn:
        cur=conn.cursor();
        cur.execute('''
                with 
                    v1 as
                        (				
                                SELECT DISTINCT ui1.user_id as user_ini
                                FROM Reviews ui1
                                WHERE ui1.product_id=?
                        ),
                    v2 as 			
                        (
                                SELECT DISTINCT ui2.user_id as user_mate, ui2.product_id as other_products 
                                FROM Reviews ui2
                                WHERE ui2.product_id<>? and ui2.user_id in (select user_ini from v1)
                        ),
                    v3 as 
                        (
                                select other_products
                                from v2
                                group by other_products
                                having count(*) > 1
                        ),
                    v4 as
                        (
                                select v2.*
                                from v2,v3
                                where v2.other_products=v3.other_products
                        ),
                    v5 as
                        (
                                select v41.user_mate as u1, v42.user_mate as u2, v41.other_products as u2 
                                FROM v4 v41 JOIN v4 v42 ON v41.other_products=v42.other_products
                                WHERE v41.user_mate <> v42.user_mate               
                        )
                SELECT u1,u2, COUNT(*) FROM v5 
                GROUP BY u1,u2;
        ''',[p_id,p_id]);
        rows=cur.fetchall();
        if(len(rows)!=0):
            average=0;
            for row in rows:
                average=average+row[2];
            average=2*average/len(rows);
            stddev=0;
            for row in rows:
                stddev=(row[2]-average)**2;
            stddev=2*mate.sqrt(stddev)/(len(rows)-1);
            weird_users=[];
            wu='(';
            for row in rows:
                if (row[2]> average + 2*stddev):
                    print(row);
                    weird_users.append(row[1]);
                    weird_users.append(row[0]);
            weird_users=list(set(weird_users));
            for i in weird_users:
                wu=wu+"'"+i+"'"+",";
            wu=wu[0:-1]+')';
    #    print (weird_users);
            if (wu!=')'):
                cur.execute(''' SELECT COUNT(DISTINCT user_id) FROM Reviews WHERE product_id=?''',(p_id,));
                total_users=cur.fetchall();
    #    print(len(weird_users)*100/total_users[0][0]);
                cur.execute(''' SELECT SUM(rating)/COUNT(rating)FROM Reviews
                        WHERE user_id NOT IN ''' + wu + ''' AND product_id=? ''',(p_id,));
                rating_without_overlap=cur.fetchall();
                rating_without_overlap=rating_without_overlap[0][0];
                cur.execute(''' SELECT SUM(rating)/COUNT(rating) FROM Reviews
                    WHERE product_id=?''',(p_id,));
                rating_with_overlap=cur.fetchall();
                rating_with_overlap=rating_with_overlap[0][0];
                print(rating_without_overlap);
                print(rating_with_overlap);
                if (abs(rating_with_overlap - rating_without_overlap)> 0.1):
                    print('gotta remove overlap');
                    return [weird_users,1];
                else:
                    print(' we can leave it there');
                    return [weird_users,0];
            else:
                print('no weird users');
                return ["none",0]
        else:
            print('no weird users');
            return ["none",0];

# Unverified Purchases

def Unverified_Purchases(p_id,conn):
    with conn:
        cur=conn.cursor();
        cur.execute (''' SELECT SUM(verified) as Sum_Verified, COUNT(verified) as Length
                     FROM Reviews
                     WHERE product_id=?''',(p_id,));
        row=cur.fetchall();
        unverified_count=row[0][1]-row[0][0];
        verified_count=row[0][1];
        print('We have a percentage of unverified that is equal to',(row[0][1]-row[0][0])/row[0][1]);
        cur.execute (''' SELECT SUM(rating) FROM Reviews
                     WHERE product_id=? AND verified=0''',(p_id,));
        row=cur.fetchall();
        if(row[0][0]!= None):
            unverified_average=row[0][0]/unverified_count;
        else:
            unverified_average=0;
        cur.execute (''' SELECT SUM(rating) FROM Reviews
                     WHERE product_id=? AND verified=1''',(p_id,));
        row=cur.fetchall();
        if (row[0][0]!= None):
            verified_average=row[0][0]/verified_count;
            print('The unverified average is',unverified_average,' while the verified average is',verified_average);
    #cur.execute(''' SELECT SUM(rating),COUNT(rating) FROM Reviews
    #            WHERE product_id=?''',(searched_product,));
            cur.execute(''' SELECT SUM(rating)/COUNT(rating) FROM Reviews WHERE product_id=?''',(p_id,));
            unchanged_average=cur.fetchall();
            unchanged_average=unchanged_average[0][0];
            if(abs(unchanged_average-verified_average)>=0.1):
                print(unchanged_average-verified_average)
                print('we should remove unverified');
                return [1,unverified_count];
            else:
                print('it dont matter');
                return [0,unverified_count];
        else:
            return [0,"none"];
        



# Incentivized Reviews

def Incentivized_Reviews(p_id,conn):
    with conn:
        cur=conn.cursor();
        cur.execute(''' SELECT SUM(incentive),COUNT(incentive) FROM Reviews
                    WHERE product_id=?''',(p_id,));
        row=cur.fetchall();
        print('The percentage number of incentivized reviews is',row[0][0]/row[0][1]);
        cur.execute('''SELECT SUM(rating),COUNT(rating) FROM Reviews
                    WHERE product_id=? AND incentive=1''',(p_id,));
        row=cur.fetchall();
        if (row[0][0]!= None):
            incentive_count=row[0][1];
            incentive_sum=row[0][0];
            cur.execute('''SELECT SUM(rating),COUNT(rating) FROM Reviews
                    WHERE product_id=? AND incentive=0''',(p_id,));
            row=cur.fetchall();
            no_incentive_count=row[0][1];
            no_incentive_sum=row[0][0];
            normal_average=(incentive_sum+no_incentive_sum)/(no_incentive_count+incentive_count);
            if (abs(normal_average- ( no_incentive_sum/no_incentive_count))>=0.1):
                print('we should remove incentivised revs');
                return [1,incentive_count];
            else:
                return [0,incentive_count];
        else:
            return [0,"none"];


# Category Ease
def Category_Ease(p_id,conn):
    with conn:
        cur=conn.cursor();
        cur.execute(''' SELECT category FROM Products
                    WHERE product_id=?''',(p_id,));
        category=cur.fetchall();
        category=category[0][0];
        cur.execute(''' SELECT total FROM Category_Ease WHERE categ=?''',(category,));
        category_ease=cur.fetchall();
        return(category_ease[0][0]);

## USER OWN INFLUENCE ON THE GRADE
        
## User Ease
def  User_Ease(u_id, c_ease,conn):
    with conn:
        cur=conn.cursor();
        cur.execute('''
                    SELECT SUM(rating) AS SUM, COUNT(rating) AS LENGTH
                    FROM Reviews 
                    WHERE user_id=?;        
                    ''',(u_id,));
        rows=cur.fetchall();
    #    print((rows[0][0]/rows[0][1]),c_ease);
        return [(rows[0][0]/rows[0][1]),c_ease];
    
# User Behaviour

def User_Behaviour(u_id,p_id,conn):
    with conn:
        cur=conn.cursor();
        cur.execute('''SELECT SUM(rating),COUNT(rating), post_time FROM Reviews 
                WHERE user_id=?
                GROUP BY post_time
                ORDER BY post_time''',(u_id,));
        rows1=cur.fetchall();
        x=[];
        y=[];
        for i in range(len(rows1)):
            k=rows1[i][2].split(' ');
            if (len(k[2])==1):
                k[2]='0'+k[2];
            k=k[0]+'-'+k[1]+'-'+k[2];
            x.append(np.datetime64(k));
            y.append(rows1[i][1]);
    
        average_posts_per_day=0;
        for i in range(len(rows1)):
            average_posts_per_day+=rows1[i][1];
        average_posts_per_day=average_posts_per_day/len(rows1);
    
        standard_dev=0;
        for i in range(len(rows1)):
            standard_dev+=(rows1[i][1]-average_posts_per_day)**2;
        standard_dev=standard_dev/(len(rows1));
    
        avg_score_weird_days=0;
        weird_days_count=0;
        weird_dates=[];
        for i in range(len(rows1)):
            if(rows1[i][1]>= (average_posts_per_day + 2*standard_dev)):
                weird_days_count+=1;
                avg_score_weird_days+=rows1[i][0]/rows1[i][1];
                weird_dates.append(rows1[i][2]);
    #    if (weird_days_count!=0):
    #        print('weird days score is',avg_score_weird_days/weird_days_count);
    #    else:
    #        print('neka');
        cur.execute('''SELECT COUNT(rating) FROM Reviews
                    WHERE user_id=?''',(u_id,));
        number_of_revs=cur.fetchall();
        number_of_revs=number_of_revs[0][0];
    #    print(len(y)/number_of_revs);
        if (len(y)/number_of_revs < 0.5):
            flag_post_day=1;
        else:
            flag_post_day=0;
        # here we check the unverified/verified ratio
        cur.execute(''' SELECT SUM(rating),COUNT(rating) FROM Reviews
                    WHERE user_id=? AND verified=0''',(u_id,));
        uur=cur.fetchall();
        if ((uur!= None)&(uur[0][0]!= None)&(uur[0][1]!= None)):
            unverified_user_revs=uur[0][1];
            unverified_user_avg_rating=uur[0][0]/uur[0][1];        
            cur.execute(''' SELECT SUM(rating),COUNT(*) FROM Reviews
                    WHERE user_id=? AND verified=1''',(u_id,));
            ur=cur.fetchall();
            if ((ur!= None)&(ur[0][0]!= None)&(ur[0][1] != None)):
                user_revs=ur[0][1];
                user_avg_rating=ur[0][0]/ur[0][1];
    #            print(user_avg_rating-unverified_user_avg_rating);
    #            print(unverified_user_revs,user_revs);
                if (abs(unverified_user_avg_rating - user_avg_rating) > 0.1):
                    flag_verified_rating=1;
                else:
                    flag_verified_rating=0;
                if (unverified_user_revs/(unverified_user_revs+user_revs)>0.2):
                    flag_number_verified=1;
                else:
                    flag_number_verified=0;
            else:
                flag_number_verified=1;
                flag_verified_rating=1;
        else:
            flag_verified_rating=0;
            flag_number_verified=0;
        # ano
        # here we check more reviews from the same user in the same product
        cur.execute('''SELECT COUNT(*) FROM Reviews
                    WHERE user_id=? AND product_id=?''',[u_id,p_id]);
        same_user_revs=cur.fetchall();
        same_user_revs=same_user_revs[0][0];
        sur_coefficient=1/same_user_revs;
        cur.execute('''SELECT COUNT(*) FROM Reviews
                    WHERE user_id=? 
                    GROUP BY product_id''',(u_id,));
        more_revs_same_product=cur.fetchall();
        more_than_1=0;
        exactly_1=0;
        for prod in more_revs_same_product:
            if (prod==1):
                exactly_1+=1;
            else:
                more_than_1+=1;
        if (more_than_1/(more_than_1+exactly_1)>=0.4):
            more_revs_one_post_flag=1;
        else:
            more_revs_one_post_flag=0;
        return [weird_dates,sur_coefficient,flag_verified_rating,flag_number_verified,flag_post_day,more_revs_one_post_flag];
        

def THE_SEARCH(searched_product,conn):
    #start
#    searched_product='B00000IRGG';
    #word_count
    with conn:
        cur=conn.cursor();
        word_count_result=Word_Count(searched_product,conn);
    
        #unverified_purchases
        unverified_purchases_result=Unverified_Purchases(searched_product,conn);
        
        #incentivized
        incentivized_purchases_result=Incentivized_Reviews(searched_product,conn);
        
        #user_overlapping
        overlapping_users_result=User_Overlapping_History(searched_product,conn);
        
        #rating_trend
        rating_trend_results=Rating_Trend(searched_product,conn);
    
        print('------------------------------------------------------');
    
        print(word_count_result);
        print(unverified_purchases_result);
        print(incentivized_purchases_result);
        print(overlapping_users_result);
        print(rating_trend_results);
        if (unverified_purchases_result[0] == 1):
            if (incentivized_purchases_result[0] == 1):
                cur.execute(''' SELECT * FROM Reviews 
            WHERE product_id=? AND verified=? AND incentive=?''',[searched_product,1,0]);       
            else:
                cur.execute(''' SELECT * FROM Reviews 
            WHERE product_id=? AND verified=?''',[searched_product,1]);              
        else:
            if (incentivized_purchases_result[0] == 1):
                cur.execute(''' SELECT * FROM Reviews 
            WHERE product_id=?  AND incentive=?''',[searched_product,0]);
            else:
                cur.execute('''SELECT * FROM Reviews
            WHERE product_id = ?''',(searched_product,));
        reviews=cur.fetchall();
    
        category_ease=Category_Ease(searched_product,conn);
    
        overlap_flag=0;
        if (overlapping_users_result!= None):
            if (overlapping_users_result[1]==1):
                overlap_flag=1;
            else:
                avg_with_overlap=0;
                avg_without_overlap=0;
                counter_without_overlap=0;
                for review in reviews:
                    if (review[2] not in overlapping_users_result[0]):
                        avg_without_overlap+=review[4];
                        counter_without_overlap+=1;
                    avg_with_overlap+=review[4];
                if (abs(avg_with_overlap - avg_without_overlap)>0.1):
                    overlap_flag=1;
            
                
        normal_avg=0;
        changed_avg=0;
        changed_count=0;       
        before_counter=0;
        after_counter=0;
        suspicious_reviewers=[];
        for review in reviews:
            normal_avg+=review[4];
            uease=User_Ease(review[2],category_ease,conn);
            user_coef=uease[1]/uease[0];
            if (overlap_flag == 1):
                if (review[2] in overlapping_users_result[0]):
                    user_coef=0;
                    print('overlap removal');
            if(word_count_result!= None):
                if ((word_count_result!='warning') & (word_count_result!='okay')):
                    if(word_count_result[1]==1):
                        if(str(review[9]) in word_count_result[0]):
                            user_coef=user_coef*word_count_result[2]/review[4];
                else:
                    if (word_count_result=='warning'):
                        print('theres a warning');
                    else:
                        print('we believe its ok'); 
            user_behave=User_Behaviour(review[2],review[1],conn);
            user_coef=user_coef*user_behave[1]
            if ((user_behave[2]+user_behave[3]+user_behave[4]+user_behave[5])>=3):
                user_coef=0;
                print('removed user');
                suspicious_reviewers.append(review[2]);
    #        print('changed one');
            else:
                if ((user_behave[2]+user_behave[3]+user_behave[4]+user_behave[5])!=0):
                    if (rating_trend_results!= None):
                        if (rating_trend_results[1]==1):
                            if ((review[2] in user_behave[0])&(review[2] in rating_trend_results[0])):
                                user_coef=rating_trend_results[2]/review[4];
                                suspicious_reviewers.append(review[2]);
    #                    print('changed one');
                            
                    
            changed_count+=user_coef;
            before_counter+=1;
            if (user_coef==0):
                after_counter+=1;
            changed_avg+=review[4]*user_coef;
        if (overlapping_users_result==None):
            overlapping_users_result="none"
        print('before was', round(normal_avg/len(reviews),1));
        if (word_count_result==None):
            wcr="none";
        else:
            wcr=word_count_result[3];
        if (rating_trend_results==None):
            rtr="none";
        else:
            rtr=rating_trend_results[3];
        if (changed_count!=0):
            print('after is', round(changed_avg/changed_count,1));
            if (word_count_result!= None ):
                if (rating_trend_results!=None):
                    return [before_counter,before_counter-after_counter, round(normal_avg/len(reviews),1),round(changed_avg/changed_count,1),word_count_result[0],len(word_count_result[0]),rating_trend_results[0],len(rating_trend_results[0]),uease[1],overlapping_users_result[0],len(overlapping_users_result[0]),unverified_purchases_result[0],unverified_purchases_result[1],incentivized_purchases_result[0],incentivized_purchases_result[0],suspicious_reviewers,len(suspicious_reviewers),overlap_flag,wcr,rtr];
                else:
                    return [before_counter,before_counter-after_counter, round(normal_avg/len(reviews),1),round(changed_avg/changed_count,1),word_count_result[0],len(word_count_result[0]),["none"],1,uease[1],overlapping_users_result[0],len(overlapping_users_result[0]),unverified_purchases_result[0],unverified_purchases_result[1],incentivized_purchases_result[0],incentivized_purchases_result[0],suspicious_reviewers,len(suspicious_reviewers),overlap_flag,wcr,rtr];
            else:
                if (rating_trend_results!=None):
                    return [before_counter,before_counter-after_counter, round(normal_avg/len(reviews),1),round(changed_avg/changed_count,1),["none"],1,rating_trend_results[0],len(rating_trend_results[0]),uease[1],overlapping_users_result[0],len(overlapping_users_result[0]),unverified_purchases_result[0],unverified_purchases_result[1],incentivized_purchases_result[0],incentivized_purchases_result[0],suspicious_reviewers,len(suspicious_reviewers),overlap_flag,wcr,rtr];
                else:
                    return [before_counter,before_counter-after_counter, round(normal_avg/len(reviews),1),round(changed_avg/changed_count,1),["none"],1,["none"],1,uease[1],overlapping_users_result[0],len(overlapping_users_result[0]),unverified_purchases_result[0],unverified_purchases_result[1],incentivized_purchases_result[0],incentivized_purchases_result[0],suspicious_reviewers,len(suspicious_reviewers),overlap_flag,wcr,rtr];
        else:
            print('no trustworthy reviews');    
        print('total number is', before_counter);
        print('after deleting number is',before_counter-after_counter);
        return [before_counter,before_counter-after_counter, round(normal_avg/len(reviews),1),'no trustworthy reviews',["none"],1,["none"],1,uease[1],overlapping_users_result[0],len(overlapping_users_result[0]),unverified_purchases_result[0],unverified_purchases_result[1],incentivized_purchases_result[0],incentivized_purchases_result[0],suspicious_reviewers,len(suspicious_reviewers),overlap_flag,wcr,rtr]
        


#User_Behaviour('AEMZRE6QYVQBS',searched_product);
        
 
#cur.execute('''CREATE VIEW IF NOT EXISTS Bins  AS
#            SELECT user_id as U_ID, product_id as P_ID, category as CAT,
#                (CASE
#                     WHEN length BETWEEN 0 and 15 THEN 1
#                     WHEN length BETWEEN 15 and 30 THEN 2
#                     WHEN length BETWEEN 30 and 40 THEN 3
#                     WHEN length BETWEEN 40 and 50 THEN 4
#                     WHEN length BETWEEN 50 and 60 THEN 5
#                     WHEN length BETWEEN 60 and 70 THEN 6
#                     WHEN length BETWEEN 70 and 85 THEN 7
#                     WHEN length BETWEEN 85 and 100 THEN 8
#                     ELSE 9
#                END 
#                ) AS Bin
#                FROM Reviews
#            ''')      

#cur.execute('''ALTER TABLE Reviews ADD COLUMN Bins int''');
#cur.execute(''' UPDATE Reviews SET Bins = (CASE
#                     WHEN length BETWEEN 0 and 15 THEN 1
#                     WHEN length BETWEEN 15 and 30 THEN 2
#                     WHEN length BETWEEN 30 and 40 THEN 3
#                     WHEN length BETWEEN 40 and 50 THEN 4
#                     WHEN length BETWEEN 50 and 60 THEN 5
#                     WHEN length BETWEEN 60 and 70 THEN 6
#                     WHEN length BETWEEN 70 and 85 THEN 7
#                     WHEN length BETWEEN 85 and 100 THEN 8
#                     ELSE 9
#                END)''');


