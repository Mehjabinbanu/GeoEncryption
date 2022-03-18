from flask import Flask, render_template, request, jsonify, session
from dbconnection import Db
app = Flask(__name__)

staticpath="C:\\Users\\Mumthazlatheef\\PycharmProjects\\untitled\\static\\"
app.secret_key="kkkk"

@app.route('/')
def index_login():
    return render_template('index.html')

@app.route('/login')
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
        elif res['type']=="leader":
            session["lid"]=res["lid"]
            q="SELECT dept_id FROM team_leader WHERE staff_id='"+str(session["lid"])+"'"
            d=Db()
            r=d.selectOne(q)
            session["dpid"]=r["dept_id"]
            return render_template("teamleader/Home.html")
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
    q="DELETE FROM staff WHERE lid='"+sid+"'"
    d=Db()
    d.delete(q)
    return '''<script>alert('successfully deleted');window.location='/admin_manage_staff'</script>'''


@app.route('/admin_add_work')
def admin_add_work():
    qry = "select * from department"
    d = Db()
    res = d.select(qry)
    return render_template('admin/add_work.html',a=res)

@app.route('/admin_add_work_post',methods=["post"])
def admin_add_work_post():
    title = request.form["textfield"]
    dep=request.form["select"]
    desc = request.form["textfield2"]
    sdate = request.form["textfield3"]
    stime = request.form["textfield4"]
    udate=request.form["textfield5"]
    qry = "INSERT INTO works(`title`,`dept_id`,`description`,`sdate`,`stime`,`uploaddate`) VALUES ('"+title+"','"+dep+"','"+desc+"','"+sdate+"','"+stime+"','"+udate+"')"
    d = Db()
    d.insert(qry)
    return '''<script>alert('success');window.location='/admin_add_work'</script>'''

@app.route('/admin_manage_work')
def admin_manage_work():
    qry = "SELECT works.*,`department`.`dept_name`  FROM works INNER JOIN department ON `department`.`dept_id`=`works`.`dept_id` "
    d = Db()
    res = d.select(qry)
    return render_template('admin/manage_work.html',a=res)

@app.route('/admin_edit_works/<workid>')
def admin_edit_works(workid):
    q = "select * from works WHERE work_id='"+workid+"'"
    d = Db()
    res=d.selectOne(q)
    qry = "select * from department"
    d = Db()
    res1 = d.select(qry)
    return render_template('admin/edit_work.html', a=res1,d=res)

@app.route('/admin_edit_work_post',methods=['post'])
def admin_edit_work_post():
    workid=request.form["work_id"]
    title = request.form["textfield"]
    dep=request.form["select"]
    desc = request.form["textfield2"]
    sdate = request.form["textfield3"]
    stime = request.form["textfield4"]
    udate = request.form["textfield5"]
    q="UPDATE works SET `title`='"+title+"',`dept_id`='"+dep+"',`description`='"+desc+"',`sdate`='"+sdate+"',`stime`='"+stime+"',`uploaddate`='"+udate+"' WHERE work_id='"+workid+"'"
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
    # qry1 = "SELECT `assigned_work`.* ,`works`.* FROM `assigned_work` INNER JOIN `works` ON `works`.`work_id`=`assigned_work`.`work_id`"
    # res1 = d.select(qry1)

    return render_template('admin/view_assignedwork.html',leader=res)

@app.route('/admin_view_assignedwork_search',methods=['post'])
def admin_view_assignedwork_search():
    tid = request.form["select"]
    qry = "SELECT `assigned_work`.* ,`works`.* FROM `assigned_work` INNER JOIN `works` ON `works`.`work_id`=`assigned_work`.`work_id`  WHERE `assigned_work`.`leader_id`='"+tid+"'"
    d = Db()
    res = d.select(qry)

    print(qry)

    # q = "SELECT team_leader.* ,staff.* FROM team_leader INNER JOIN staff ON staff.lid=team_leader.staff_id  WHERE team_leader.leader_id='"+tid+"'"
    # res1=d.select(q)

    if res is not None:
        q = "SELECT team_leader.* ,staff.* FROM team_leader INNER JOIN staff ON staff.lid=team_leader.staff_id "
        d = Db()
        ress = d.select(q)
        return render_template('admin/view_assignedwork.html',work=res,leader=ress)
    else:
        return "<html><h1 style='color:red'>No work assigned!!!!!!!!!!!!</h1></html>"

@app.route('/admin_view_status/<wid>')
def admin_view_status(wid):
    q="select assigned_work.*,teamleader_status.* from teamleader_status INNER JOIN assigned_work ON assigned_work.work_id=teamleader_status.work_id WHERE assigned_work.work_id='"+wid+"'"
    d=Db()
    res=d.selectOne(q)
    return render_template('admin/view_status.html',i=res,wid=wid)


@app.route('/admin_delete_assignedworks/<wid>')
def admin_delete_assignedworks(wid):
    q="DELETE FROM `assigned_work` WHERE `work_id`='"+wid+"'"
    d=Db()
    d.delete(q)
    return '''<script>alert('successfully deleted');window.location='/admin_view_assignedwork'</script>'''

@app.route('/teamleader_view_profile')
def teamleader_view_profile():
    q="SELECT `login`.`lid`,`staff`.* FROM `login` INNER JOIN  `staff` ON `staff`.`lid`=`login`.`lid` WHERE staff.lid='"+str(session["lid"])+"'"
    d=Db()
    res=d.selectOne(q)
    return render_template('teamleader/view_profile.html',i=res)

@app.route('/teamleader_changepassword')
def teamleader_changepassword():
    return render_template("teamleader/change_password.html")

@app.route('/teamleader_changepassword_post',methods=['post'])
def teamleader_changepassword_post():
    old=request.form['textfield']
    new=request.form['textfield2']
    cn=request.form['textfield3']
    d = Db()
    qry1="select * from login where password='"+old+"'"
    res1=d.selectOne(qry1)
    if(new==cn):
        qry="UPDATE login SET PASSWORD='"+cn+"' WHERE lid='"+str(session["lid"])+"'"
        res=d.update(qry)
        return '''<script>alert('Password Changed ');window.location='/'</script>'''
    else:
        return '''<script>alert('Error');window.location='/teamleader_changepassword'</script>'''

@app.route('/teamleader_view_assignedwork')
def teamleader_view_assignedwork():
    q="SELECT `assigned_work`.* ,`works`.* FROM `assigned_work` INNER JOIN `works` ON `works`.`work_id`=`assigned_work`.`work_id` where assigned_work.leader_id='"+str(session["lid"])+"'"
    d=Db()
    res=d.select(q)
    print(res)
    print(q)
    return render_template('teamleader/teamleader_assignedwork.html',work=res)

@app.route('/teamleader_upload_status/<wid>')
def teamleader_upload_status(wid):
    q="SELECT `assigned_work`.* ,`works`.* FROM `assigned_work` INNER JOIN `works` ON `works`.`work_id`=`assigned_work`.`work_id` where assigned_work.leader_id='"+str(session["lid"])+"' and works.work_id='"+wid+"'"
    d=Db()
    res=d.selectOne(q)
    return render_template('teamleader/upload_status.html',a=res,wid=wid)

@app.route('/teamleader_upload_status_insert',methods=['post'])
def teamleader_upload_status_insert():
    wid=request.form['work_id']
    file=request.files['fileField']
    file.save(staticpath + "status\\" + file.filename)
    url = "/static/status/" + file.filename
    desc=request.form['textfield']
    q = "INSERT INTO `teamleader_status`(`work_id`,`file`,`description`)VALUES('" + wid + "','" + url + "','"+desc+"')"
    d = Db()
    d.insert(q)
    return '''<script>alert('successfully uploaded');window.location='/teamleader_view_assignedwork'</script>'''


@app.route('/teamleader_subduty_creation/<id>')
def teamleader_subduty_creation(id):
    q="SELECT `assigned_work`.* ,`works`.* FROM `assigned_work` INNER JOIN `works` ON `works`.`work_id`=`assigned_work`.`work_id` WHERE assigned_work.leader_id='"+str(session["lid"])+"' and works.work_id='"+id+"'"
    d=Db()
    res=d.selectOne(q)
    print(res)
    return render_template('teamleader/subduty_creation.html',a=res)

@app.route('/teamleader_subduty_creation_post',methods=['post'])
def teamleader_subduty_creation_post():
    workid = request.form['wid']
    print("-----------",workid)
    title=request.form['textfield']
    desc=request.form['textfield2']
    sdate=request.form['textfield3']
    udate=request.form['textfield4']
    d = Db()

    qry="INSERT INTO `subduties` (`work_id`,`title`,`description`,`sdate`,`udate`) VALUES ('"+workid+"','"+title+"','"+desc+"','"+sdate+"','"+udate+"')"
    print(qry)
    res = d.insert(qry)
    print(res)
    return '''<script>alert('success');window.location='/teamleader_view_assignedwork'</script>'''

@app.route('/teamleader_manage_subduties/<subid>')
def teamleader_manage_subduties(subid):
    # qry="SELECT subduties.*,assigned_work.* FROM subduties INNER JOIN assigned_work ON assigned_work.work_id=subduties.work_id WHERE  assigned_work.leader_id='"+str(session["lid"])+"' and subduties.sub_id='"+subid+"'"
    # d=Db()
    # res=d.select(qry)


    q="SELECT * FROM subduties WHERE work_id='"+subid+"'"
    d=Db()
    res=d.select(q)
    return render_template('teamleader/manage_subduty.html',sub=res)


@app.route('/teamleader_edit_subduties/<subid>')
def teamleader_edit_subduties(subid):
    q="SELECT subduties.*,assigned_work.* FROM subduties INNER JOIN assigned_work ON assigned_work.work_id=subduties.work_id WHERE  assigned_work.leader_id='"+str(session["lid"])+"' and subduties.sub_id='"+subid+"'"
    print(q)
    d=Db()
    res=d.selectOne(q)
    return render_template('teamleader/edit_subduty.html',sd=res)

@app.route('/teamleader_edit_subduties_post',methods=['post'])
def teamleader_edit_subduties_post():
    subid = request.form["sub_id"]
    title = request.form["textfield"]
    desc = request.form["textfield2"]
    sdate = request.form["textfield3"]
    udate = request.form["textfield4"]
    qry="UPDATE subduties SET `title`='"+title+"',`description`='"+desc+"',`sdate`='"+sdate+"',`udate`='"+udate+"' WHERE sub_id='"+subid+"'"
    d = Db()
    d.update(qry)
    return '''<script>alert('successfully updated');window.location='/teamleader_manage_subduties'</script>'''

@app.route('/teamleader_delete_subduties/<subid>')

def teamleader_delete_subduties(subid):
    q="DELETE FROM subduties WHERE sub_id='"+subid+"'"
    d=Db()
    d.delete(q)
    return '''<script>alert('successfully deleted');window.location='/teamleader_manage_subduties'</script>'''

@app.route('/teamleader_assign_subduty/<subid>')
def teamleader_assign_subduty(subid):
    q="select staff.* from staff where department='"+str(session["dpid"])+"'"
    d = Db()
    res = d.select(q)
    print(subid)
    return render_template('teamleader/assign_staff.html.', staff=res,sid=subid)


@app.route('/teamleader_assign_subduty_insert', methods=['post'])
def teamleaer_assign_subduty_insert():
    sid = request.form['select']
    subid= request.form['sub_id']
    q = "INSERT INTO `assigned_subduty`(`sub_id`,`staff_id`,`date`)VALUES('" + subid + "','" + sid + "',curdate())"
    d = Db()
    d.insert(q)
    return '''<script>alert('successfully assigned');window.location='/teamleader_view_assignedwork'</script>'''

@app.route('/teamleader_view_assigned_subduty')
def teamleader_view_assigned_subduty():
    q = "select staff.* from staff where department='"+str(session["dpid"])+"'"
    d = Db()
    res = d.select(q)
    return render_template('teamleader/view_subduty.html', staff=res)

@app.route('/teamleader_assigned_subduty_search',methods=['post'])
def teamleader_assigned_subduty_search():
    sid = request.form["select"]
    qry = "SELECT `assigned_subduty`.* ,`subduties`.* FROM `assigned_subduty` INNER JOIN `subduties` ON `subduties`.`sub_id`=`assigned_subduty`.`sub_id`  WHERE `assigned_subduty`.`staff_id`='" + sid + "'"
    d = Db()
    res = d.select(qry)
    if res is not None:
        q = "select staff.* from staff where department='"+str(session["dpid"])+"'"
        d = Db()
        ress = d.select(q)
        return render_template('teamleader/view_subduty.html',sub=res,staff=ress)
    else:
        return "<html><h1 style='color:red'>No work assigned!!!!!!!!!!!!</h1></html>"

@app.route('/teamleader_view_status/<sub_id>')
def teamleader_view_status(sub_id):
    q="select assigned_subduty.*,staff_status.* from staff_status INNER JOIN assigned_subduty ON assigned_subduty.sub_id=staff_status.sub_id WHERE assigned_subduty.sub_id='"+sub_id+"'"
    d=Db()
    res=d.selectOne(q)
    return render_template('teamleader/view_status.html',i=res,sid=sub_id)

@app.route('/teamleader_delete_assignedsubduty/<subid>')
def teamleader_delete_assignedsubduty(subid):
    q = "DELETE FROM `assigned_subduty` WHERE `sub_id`='" + subid + "'"
    d = Db()
    d.delete(q)
    return '''<script>alert('successfully deleted');window.location='/teamleader_view_assigned_subduty'</script>'''



if __name__ == '__main__':
    app.run(debug=True)
