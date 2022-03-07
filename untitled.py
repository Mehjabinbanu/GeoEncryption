from flask import Flask, render_template, request, jsonify
from dbconnection import Db
app = Flask(__name__)

staticpath="C:\\Users\\Mumthazlatheef\\PycharmProjects\\untitled\\static\\"

@app.route('/')
def login():
   return render_template('login.html')

@app.route('/login_post',methods=["post"])
def login_post():
    uname=request.form["textfield"]
    pwd=request.form["textfield2"]
    qry="SELECT * FROM login WHERE username='"+uname+"' AND password='"+pwd+"'"
    rd=Db()
    res=rd.selectOne(qry)
    if res is not None:
        if res['type']=="admin":
            return render_template("admin/Home.html")
        else:
            return "<script>alert('Invalid username or password'); window.location='/'</script>"
    else:
        return "<script>alert('Invalid username or password'); window.location='/'</script>"



@app.route('/admin_add_dept')
def admin_add_dept():
    return render_template('admin/add_dept.html')

@app.route('/admin_add_dept_post',methods=["post"])
def admin_add_dept_post():
    dept1=request.form["textfield"]
    place1=request.form["textfield2"]
    lat = request.form["textfield3"]
    long = request.form["textfield4"]
    qry="INSERT INTO department(`dept_name`,`place`,`latitude`,`longitude`) VALUES('"+dept1+"','"+place1+"','"+lat+"','"+long+"')"
    d=Db()
    d.insert(qry)
    return '''<script>alert('success');window.location='/admin_add_dept'</script>'''

@app.route('/admin_manage_dept')
def admin_manage_dept():
    qry = "select * from department"
    d = Db()
    res = d.select(qry)
    return render_template('admin/manage_dept.html',n=res)

@app.route('/admin_edit_dept/<deptid>')
def admin_edit_dept(deptid):
    q = "select * from department WHERE dept_id='"+deptid+"'"
    d = Db()
    res=d.selectOne(q)
    return render_template('admin/edit_dept.html', a=res)

@app.route('/admin_edit_dept_post',methods=['post'])
def admin_edit_dept_post():
    deptid=request.form["dept_id"]
    dept1 = request.form["textfield"]
    place1 = request.form["textfield2"]
    lat = request.form["textfield3"]
    long = request.form["textfield4"]
    q="UPDATE department SET `dept_name`='"+dept1+"',`place`='"+place1+"',`latitude`='"+lat+"',`longitude`='"+long+"' WHERE `dept_id`='"+deptid+"'"
    d=Db()
    d.update(q)
    return '''<script>alert('successfully updated');window.location='/admin_manage_dept'</script>'''

@app.route('/admin_delete_depat/<did>')
def admin_delete_depat(did):
    q="DELETE FROM department WHERE dept_id='"+did+"'"
    d=Db()
    d.delete(q)
    return '''<script>alert('successfully deleted');window.location='/admin_manage_dept'</script>'''


@app.route('/admin_add_staff')
def admin_add_staff():
    qry="select * from department"
    d=Db()
    res=d.select(qry)
    return render_template('admin/add_staff.html',a=res)

@app.route('/admin_add_staff_post',methods=["post"])
def admin_add_staff_post():
    name=request.form["textfield"]
    img=request.files["fileField"]
    img.save(staticpath+"staff\\"+img.filename)
    url="/static/staff/"+img.filename
    dob=request.form["textfield2"]
    gen=request.form["radio"]
    dep=request.form["select"]
    des=request.form["textfield3"]
    qua = request.form["textfield4"]
    house = request.form["textfield5"]
    place = request.form["textfield6"]
    pin = request.form["textfield7"]
    dist = request.form["textfield8"]
    state = request.form["textfield9"]
    con = request.form["textfield10"]
    email = request.form["textfield11"]
    import random
    d=Db()
    pasw=str(random.randint(0000,9999))
    q="INSERT INTO login(`username`,`password`,`type`) VALUES('"+email+"','"+pasw+"','staff')"
    lid=d.insert(q)

    qry="INSERT INTO staff(`lid`,`name`,`photo`,`dob`,`gender`,`department`,`designation`,`qualification`,`house_name`,`place`,`pin`,`district`,`state`,`contact`,`email`) VALUES('"+str(lid)+"','"+name+"','"+url+"','"+dob+"','"+gen+"','"+dep+"','"+des+"','"+qua+"','"+house+"','"+place+"','"+pin+"','"+dist+"','"+state+"','"+con+"','"+email+"')"
    d.insert(qry)
    return '''<script>alert('success');window.location='/admin_add_staff'</script>'''



@app.route('/admin_manage_staff')
def admin_manage_staff():

    q="select * from department"
    qry= "select staff.*,`department`.`dept_name`  from staff inner join department on `department`.`dept_id`=`staff`.`department` "
    d = Db()
    res1 = d.select(q)
    res = d.select((qry))
    return render_template('admin/manage_staff.html',a=res,b=res1)

@app.route('/admin_manage_staffsearch',methods=['post'])
def admin_manage_staffsearch():
    depid=request.form["select"]
    q="select * from department"
    qry= "select staff.*,`department`.`dept_name`  from staff inner join department on `department`.`dept_id`=`staff`.`department` where `department`.`dept_id`='"+depid+"'  "
    d = Db()
    res1 = d.select(q)
    res = d.select((qry))
    return render_template('admin/manage_staff.html',a=res,b=res1)

@app.route('/admin_edit_staff/<stid>')
def admin_edit_staff(stid):
    q="select staff.*,`department`.* from staff inner join department on `department`.`dept_id`=`staff`.`department` where staff.lid='"+stid+"'"
    d=Db()
    res=d.selectOne(q)

    q = "select * from department"
    dep=d.select(q)

    return render_template('admin/edit_staff.html',a=res,dept=dep)

@app.route('/admin_edit_staff_post',methods=["post"])
def admin_edit_staff_post():
    stid=request.form["lid"]
    name = request.form["textfield"]
    dob = request.form["textfield2"]
    gen = request.form["radio"]
    dep = request.form["select"]
    des = request.form["textfield3"]
    qua = request.form["textfield4"]
    house = request.form["textfield5"]
    place = request.form["textfield6"]
    pin = request.form["textfield7"]
    dist = request.form["textfield8"]
    state = request.form["textfield9"]
    con = request.form["textfield10"]
    d = Db()
    if 'fileField' in request.files:
        img = request.files["fileField"]
        if img.filename !="":
            img.save(staticpath + "staff\\" + img.filename)
            url = "/static/staff/" + img.filename
            qry="UPDATE staff SET `name`='"+name+"',`photo`='"+url+"',`dob`='"+dob+"',`gender`='"+gen+"',`department`='"+dep+"',`designation`='"+des+"',`qualification`='"+qua+"',`house_name`='"+house+"',`place`='"+place+"',`pin`='"+pin+"',`district`='"+dist+"',`state`='"+state+"',`contact`='"+con+"' where staff.lid='"+stid+"'"
        else:
            qry = "UPDATE staff SET `name`='" + name + "',`dob`='" + dob + "',`gender`='" + gen + "',`department`='" + dep + "',`designation`='" + des + "',`qualification`='" + qua + "',`house_name`='" + house + "',`place`='" + place + "',`pin`='" + pin + "',`district`='" + dist + "',`state`='" + state + "',`contact`='" + con + "' where staff.lid='" + stid + "'"


    else:
        qry = "UPDATE staff SET `name`='" + name + "',`dob`='" + dob + "',`gender`='" + gen + "',`department`='" + dep + "',`designation`='" + des + "',`qualification`='" + qua + "',`house_name`='" + house + "',`place`='" + place + "',`pin`='" + pin + "',`district`='" + dist + "',`state`='" + state + "',`contact`='" + con + "' where staff.lid='" + stid + "'"

    d.update(qry)
    return '''<script>alert('successfully updated');window.location='/admin_manage_staff'</script>'''

@app.route('/admin_delete_staff/<sid>')
def admin_delete_staff(sid):
    q="DELETE FROM staff WHERE staff_id='"+sid+"'"
    d=Db()
    d.delete(q)
    return '''<script>alert('successfully deleted');window.location='/admin_manage_staff'</script>'''


@app.route('/admin_add_work')
def admin_add_work():
    return render_template('admin/add_work.html')

@app.route('/admin_add_work_post',methods=["post"])
def admin_add_work_post():
    title = request.form["textfield"]
    desc = request.form["textfield2"]
    sdate = request.form["textfield3"]
    stime = request.form["textfield4"]
    udate=request.form["textfield5"]
    qry = "INSERT INTO works(`title`,`description`,`sdate`,`stime`,`uploaded_date`) VALUES ('"+title+"','"+desc+"','"+sdate+"','"+stime+"','"+udate+"')"
    d = Db()
    d.insert(qry)
    return '''<script>alert('success');window.location='/admin_add_dept'</script>'''

@app.route('/admin_manage_work')
def admin_manage_work():
    qry = "select * from works"
    d = Db()
    res = d.select(qry)
    return render_template('admin/manage_work.html',a=res)

@app.route('/admin_edit_works/<workid>')
def admin_edit_works(workid):
    q = "select * from works WHERE work_id='"+workid+"'"
    d = Db()
    res=d.selectOne(q)
    return render_template('admin/edit_work.html', a=res)

@app.route('/admin_edit_work_post',methods=['post'])
def admin_edit_work_post():
    workid=request.form["work_id"]
    title = request.form["textfield"]
    desc = request.form["textfield2"]
    sdate = request.form["textfield3"]
    stime = request.form["textfield4"]
    udate = request.form["textfield5"]
    q="UPDATE works SET `title`='"+title+"',`description`='"+desc+"',`sdate`='"+sdate+"',`stime`='"+stime+"',`uploaddate`='"+udate+"' WHERE work_id='"+workid+"'"
    d=Db()
    d.update(q)
    return '''<script>alert('successfully updated');window.location='/admin_manage_work'</script>'''


@app.route('/admin_delete_works/<wid>')

def admin_delete_works(wid):
    q="DELETE FROM works WHERE work_id='"+wid+"'"
    d=Db()
    d.delete(q)
    return '''<script>alert('successfully deleted');window.location='/admin_manage_work'</script>'''

@app.route('/admin_teamleader_assign')
def admin_teamleader_assign():

    qry= "select * from department"
    d = Db()
    res = d.select(qry)

    return render_template('admin/teamleader_assign.html',department=res)

@app.route('/admin_leader_assign_post_ajax',methods=['post'])
def admin_leader_assign_post_ajax():
    depid = request.form["dept_id"]
    qry="select * from staff where department='"+depid+"'"
    d=Db()
    res=d.select(qry)
    return jsonify(status="ok",data=res)

@app.route('/admin_leader_insert',methods=['post'])
def admin_leader_insert():
    did=request.form['select']
    sid=request.form['select2']
    d=Db()
    q="SELECT * FROM `team_leader` WHERE `dept_id`='"+did+"'"
    res=d.selectOne(q)
    print(q)
    print(res)
    if res is not None:
        pre_up="UPDATE `login` SET `type`='staff' WHERE `lid`='"+str(res["staff_id"])+"'"
        d.update(pre_up)

        q="UPDATE `team_leader` SET `staff_id`='"+sid+"' WHERE `dept_id`='"+did+"'"
        d.update(q)

        new_up="UPDATE `login` SET `type`='leader' WHERE `lid`='"+sid+"'"
        d.update(new_up)
        return '''<script>alert('success');window.location='/admin_teamleader_assign'</script>'''

    else:
        q="INSERT INTO team_leader(`staff_id`,`dept_id`) VALUES('"+sid+"','"+did+"')"
        d.insert(q)
        return '''<script>alert('success');window.location='/admin_teamleader_assign'</script>'''

@app.route('/admin_view_teamleader')
def admin_view_teamleader():
    d=Db()
    q="select * from department"
    res1 = d.select(q)

    return render_template('admin/view_teamleader.html',a=res1,i="")

@app.route('/admin_view_teamleadersearch',methods=['post'])
def admin_view_teamleadersearch():
    depid=request.form["select"]

    qry = "SELECT team_leader.* ,staff.* FROM team_leader INNER JOIN staff ON staff.`lid`=team_leader.`staff_id` WHERE `team_leader`.`dept_id`='"+depid+"'"
    d = Db()
    res = d.selectOne(qry)
    print(qry)

    q = "select * from department"
    res1 = d.select(q)
    if res is not None:
        return render_template('admin/view_teamleader.html',i=res,a=res1)
    else:
        return "<html><h1 style='color:red'>No leader found!!!!!!!!!!!!!</h1></html>"

@app.route('/admin_delete_teamleader/<tid>')
def admin_delete_teamleader(tid):
    q="DELETE FROM `team_leader` WHERE `leader_id`='"+tid+"'"
    d=Db()
    d.delete(q)
    return '''<script>alert('successfully deleted');window.location='/admin_view_teamleader'</script>'''

@app.route('/admin_work_assign/<workid>')
def admin_work_assign(workid):
    q="SELECT team_leader.* ,staff.* FROM team_leader INNER JOIN staff ON staff.lid=team_leader.staff_id "
    d=Db()
    res=d.select(q)
    return render_template('admin/work_assign.html.',leader=res,workid=workid)

@app.route('/admin_work_assign_insert',methods=['post'])
def admin_work_assign_insert():
    tid=request.form['select']
    wid=request.form['work_id']
    q="INSERT INTO `assigned_work`(`leader_id`,`work_id`,`date`)VALUES('"+tid+"','"+wid+"',curdate())"
    d=Db()
    d.insert(q)
    return '''<script>alert('successfully assigned');window.location='/admin_manage_work'</script>'''
    
@app.route('/admin_view_assignedwork')
def admin_view_assignedwork():
    q = "SELECT team_leader.* ,staff.* FROM team_leader INNER JOIN staff ON staff.lid=team_leader.staff_id "
    d = Db()
    res = d.select(q)
    return render_template('admin/view_assignedwork.html',leader=res,i="")

@app.route('/admin_view_assignedwork_search',methods=['post'])
def admin_view_assignedwork_search():
    tid = request.form["select"]
    qry = "select * from works"
    d = Db()
    res = d.selectOne(qry)

    q = "SELECT team_leader.* ,staff.* FROM team_leader INNER JOIN staff ON staff.lid=team_leader.staff_id "
    res1 = d.select(q)

    if res is not None:
        return render_template('admin/view_assignedwork.html',i=res,a=res1)
    else:
        return "<html><h1 style='color:red'>No work assigned!!!!!!!!!!!!</h1></html>"

if __name__ == '__main__':
    app.run(debug=True)
