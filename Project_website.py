from flask import Flask, redirect, url_for, render_template, request, session
import random
import asd123 as otto
import sqlite3
from sqlite3 import Error


app = Flask(__name__);
app.secret_key = "hello";

categories={"All Beauty":"ab"
            ,"CDs and Vinyl":"cdv"
            , "Digital Music":"dm"
            ,"Musical Instruments":"mi"
            ,"Video Games":"vg"
            ,"Software":"sw"
            ,"Office Products":"op"
            ,"Industrial and Scientific":"iss"
            ,"Cellphone and Accessories":"ca"
            ,"Luxury Beauty":"lb"};
            
list=[1,2,3,4,5,6,6,7,8,9,10];
item=random.choice(list);
x=[25,32,23,12,"aron"];

def minute_connection(filename):
    conn = None
    try:
        conn=sqlite3.connect(filename);
    except Error as e:
        print(e);
    return conn;
        
def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

    
@app.route("/",methods=["GET","POST"])
def home():
#    if request.method=="POST":
#        aux = request.form["nm"];
#        myurl=categories[aux];
#        print(myurl);
#        print(len(myurl));
#        return redirect(url_for(myurl));
#    else:
        return render_template("index.html");
    

@app.route("/ab",methods=["GET","POST"])
def ab():
    if request.method=="POST":
        filename=r"C:\sqlite\db\BigData2020.db";
        aux = request.form["nm"];
        item=random.choice(list);
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='All_Beauty' ORDER BY Random() LIMIT 1");
        auxitem=cur.fetchall();
        conn.close
        return redirect("http://127.0.0.1:5000/"+auxitem[0][0]);
    else:
        filename=r"C:\sqlite\db\BigData2020.db";
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='All_Beauty' ORDER BY Random() LIMIT 100");
        auxlist=cur.fetchall();
        shortlist=[];
        for item in auxlist:
            shortlist.append(item[0]);
        conn.close();
        return render_template("0_all_beauty.html",x = shortlist)

@app.route("/dm",methods=["GET","POST"])
def dm():
    if request.method=="POST":
        filename=r"C:\sqlite\db\BigData2020.db";
        aux = request.form["nm"];
        item=random.choice(list);
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Digital_Music' ORDER BY Random() LIMIT 1");
        auxitem=cur.fetchall();
        conn.close
        return redirect("http://127.0.0.1:5000/"+auxitem[0][0]);
    else:
        filename=r"C:\sqlite\db\BigData2020.db";
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Digital_Music' ORDER BY Random() LIMIT 100");
        auxlist=cur.fetchall();
        shortlist=[];
        for item in auxlist:
            shortlist.append(item[0]);
        conn.close();
        return render_template("0_digital_music.html",x = shortlist)

@app.route("/mi",methods=["GET","POST"])
def mi():
    if request.method=="POST":
        filename=r"C:\sqlite\db\BigData2020.db";
        aux = request.form["nm"];
        item=random.choice(list);
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Musical_Instruments' ORDER BY Random() LIMIT 1");
        auxitem=cur.fetchall();
        conn.close
        return redirect("http://127.0.0.1:5000/"+auxitem[0][0]);
    else:
        filename=r"C:\sqlite\db\BigData2020.db";
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Musical_Instruments' ORDER BY Random() LIMIT 100");
        auxlist=cur.fetchall();
        shortlist=[];
        for item in auxlist:
            shortlist.append(item[0]);
        conn.close();
        return render_template("0_music_instruments.html",x = shortlist);

@app.route("/cdv",methods=["GET","POST"])
def cdv():
    if request.method=="POST":
        filename=r"C:\sqlite\db\BigData2020.db";
        aux = request.form["nm"];
        item=random.choice(list);
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='CDs_and_Vinyl' ORDER BY Random() LIMIT 1");
        auxitem=cur.fetchall();
        conn.close
        return redirect("http://127.0.0.1:5000/"+auxitem[0][0]);
    else:
        filename=r"C:\sqlite\db\BigData2020.db";
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='CDs_and_Vinyl' ORDER BY Random() LIMIT 100");
        auxlist=cur.fetchall();
        shortlist=[];
        for item in auxlist:
            shortlist.append(item[0]);
        conn.close();
        return render_template("0_cds_vinyl.html",x = shortlist)

@app.route("/lb",methods=["GET","POST"])
def lb():
    if request.method=="POST":
        filename=r"C:\sqlite\db\BigData2020.db";
        aux = request.form["nm"];
        item=random.choice(list);
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Luxury_Beauty' ORDER BY Random() LIMIT 1");
        auxitem=cur.fetchall();
        conn.close
        return redirect("http://127.0.0.1:5000/"+auxitem[0][0]);
    else:
        filename=r"C:\sqlite\db\BigData2020.db";
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Luxury_Beauty' ORDER BY Random() LIMIT 100");
        auxlist=cur.fetchall();
        shortlist=[];
        for item in auxlist:
            shortlist.append(item[0]);
        conn.close();
        return render_template("0_luxury_beauty.html",x = shortlist)

@app.route("/op",methods=["GET","POST"])
def op():
    if request.method=="POST":
        filename=r"C:\sqlite\db\BigData2020.db";
        aux = request.form["nm"];
        item=random.choice(list);
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Office_Products' ORDER BY Random() LIMIT 1");
        auxitem=cur.fetchall();
        conn.close
        return redirect("http://127.0.0.1:5000/"+auxitem[0][0]);
    else:
        filename=r"C:\sqlite\db\BigData2020.db";
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Office_Products' ORDER BY Random()  LIMIT 100");
        auxlist=cur.fetchall();
        shortlist=[];
        for item in auxlist:
            shortlist.append(item[0]);
        conn.close();
        return render_template("0_office_products.html",x = shortlist)

@app.route("/ca",methods=["GET","POST"])
def ca():
    if request.method=="POST":
        filename=r"C:\sqlite\db\BigData2020.db";
        aux = request.form["nm"];
        item=random.choice(list);
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Cell_Phones_and_Accessories' ORDER BY Random() LIMIT 1");
        auxitem=cur.fetchall();
        print(auxitem);
        conn.close
        return redirect("http://127.0.0.1:5000/"+auxitem[0][0]);
    else:
        filename=r"C:\sqlite\db\BigData2020.db";
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Cell_Phones_and_Accessories' ORDER BY Random() LIMIT 100");
        auxlist=cur.fetchall();
        shortlist=[];
        for item in auxlist:
            shortlist.append(item[0]);
        conn.close();
        return render_template("0_cellphone.html",x = shortlist)

@app.route("/iss",methods=["GET","POST"])
def iss():
    if request.method=="POST":
        filename=r"C:\sqlite\db\BigData2020.db";
        aux = request.form["nm"];
        item=random.choice(list);
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Industrial_and_Scientific' ORDER BY Random() LIMIT 1");
        auxitem=cur.fetchall();
        conn.close
        return redirect("http://127.0.0.1:5000/"+auxitem[0][0]);
    else:
        filename=r"C:\sqlite\db\BigData2020.db";
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Industrial_and_Scientific' ORDER BY Random() LIMIT 100");
        auxlist=cur.fetchall();
        shortlist=[];
        for item in auxlist:
            shortlist.append(item[0]);
        conn.close();
        return render_template("0_industrial_science.html",x = shortlist)

@app.route("/sw",methods=["GET","POST"])
def sw():
    if request.method=="POST":
        filename=r"C:\sqlite\db\BigData2020.db";
        aux = request.form["nm"];
        item=random.choice(list);
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Software' ORDER BY Random() LIMIT 1");
        auxitem=cur.fetchall();
        conn.close
        return redirect("http://127.0.0.1:5000/"+auxitem[0][0]);
    else:
        filename=r"C:\sqlite\db\BigData2020.db";
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Software' ORDER BY Random() LIMIT 100");
        auxlist=cur.fetchall();
        shortlist=[];
        for item in auxlist:
            shortlist.append(item[0]);
        conn.close();
        return render_template("0_software.html",x = shortlist)

@app.route("/vg",methods=["GET","POST"])
def vg():
    if request.method=="POST":
        filename=r"C:\sqlite\db\BigData2020.db";
        aux = request.form["nm"];
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Video_Games' ORDER BY Random() LIMIT 1");
        auxitem=cur.fetchall();
        conn.close
        return redirect("http://127.0.0.1:5000/"+auxitem[0][0]);
    else:
        filename=r"C:\sqlite\db\BigData2020.db";
        conn=minute_connection(filename);
        cur=conn.cursor();
        cur.execute("SELECT product_id FROM Products WHERE category='Video_Games' ORDER BY Random() LIMIT 100");
        auxlist=cur.fetchall();
        shortlist=[];
        for item in auxlist:
            shortlist.append(item[0]);
        conn.close();
        return render_template("0_video_games.html",x = shortlist)
    
@app.route("/foo1.png")
def photo():
    return render_template("wordcountinfo.html")


@app.route("/<item>",methods=["POST","GET"])
def product(item):
    filename=r"C:\sqlite\db\BigData2020.db";
    conn=minute_connection(filename);
    result=otto.THE_SEARCH(item,conn);
    print(result);
    conn.close();
    return render_template("product.html",item=item,nr_before=result[0],nr_after=result[1],average_before=result[2],average_after=result[3],wordcountresult=result[4],nrbins=result[5],ratingtrendresult=result[6],nrdays=result[7],c_ease=result[8],overlappingusers=result[9],nroverlapusers=result[10],flagunverified=result[11],nrunverified=result[12],flagincentivise=result[13],nrincentivise=result[14],suspicioususers=result[15],nrsuspicioususers=result[16],overlapflag=result[17],img1=result[18],img2=result[19]);

    
if __name__=='__main__':
    app.run();

