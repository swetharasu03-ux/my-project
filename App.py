from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import mysql.connector
from ecies.utils import generate_key
from ecies import encrypt, decrypt
import base64, os
import sys

app = Flask(__name__)
app.secret_key = 'a'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ServerLogin')
def ServerLogin():
    return render_template('ServerLogin.html')


@app.route('/CloudServerLogin')
def CloudServerLogin():
    return render_template('CloudServerLogin.html')


@app.route('/OwnerLogin')
def OwnerLogin():
    return render_template('OwnerLogin.html')


@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')


@app.route('/NewOwner')
def NewOwner():
    return render_template('NewOwner.html')


@app.route('/NewUser')
def NewUser():
    return render_template('NewUser.html')


@app.route('/TALogin')
def TALogin():
    return render_template('TALogin.html')


@app.route("/serverlogin", methods=['GET', 'POST'])
def serverlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'server' and request.form['password'] == 'server':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
            cur = conn.cursor()
            cur.execute("SELECT * FROM ownertb ")
            data = cur.fetchall()
            return render_template('ServerHome.html', data=data)

        else:
            flash('Username or Password is wrong')
            return render_template('ServerLogin.html')


@app.route("/ServerHome")
def ServerHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb ")
    data = cur.fetchall()
    return render_template('ServerHome.html', data=data)


@app.route("/SUserInfo")
def SUserInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()
    return render_template('SUserInfo.html', data=data)


@app.route('/SFileInfo')
def SFileInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
    cur = conn.cursor()
    cur.execute("SELECT * FROM filetb ")
    data1 = cur.fetchall()
    return render_template('SFileInfo.html', data=data1)


@app.route("/Approved")
def Approved():
    id = request.args.get('lid')
    email = request.args.get('email')
    import random
    loginkey = random.randint(1111, 9999)
    message = "Owner Login Key :" + str(loginkey)

    sendmail(email, message)

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
    cursor = conn.cursor()
    cursor.execute("Update ownertb set Status='Active',LoginKey='" + str(loginkey) + "' where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status='Active'")
    data1 = cur.fetchall()

    return render_template('TAHome.html', data=data, data1=data1)


@app.route("/Reject")
def Reject():
    id = request.args.get('lid')
    email = request.args.get('email')

    message = "Your Request  Rejected"

    sendmail(email, message)

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
    cursor = conn.cursor()
    cursor.execute("Update ownertb set Status='reject' where id='" + id + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status='waiting'")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where status !='waiting'")
    data1 = cur.fetchall()

    return render_template('TAHome.html', data=data, data1=data1)


@app.route("/newowner", methods=['GET', 'POST'])
def newowner():
    if request.method == 'POST':
        uname = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
        cursor = conn.cursor()
        cursor.execute("SELECT * from ownertb where username='" + username + "'  ")
        data = cursor.fetchone()
        if data is None:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ownertb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + address + "','" + username + "','" + password + "')")
            conn.commit()
            conn.close()

            import LiveRecognition as liv
            liv.att()

            del sys.modules["LiveRecognition"]

            flash('Record Saved!')
            return render_template('NewOwner.html')
        else:
            flash('Already Register This  UserName!')
            return render_template('NewOwner.html')


@app.route("/ownerlogin", methods=['GET', 'POST'])
def ownerlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['password']

        session['oname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
        cursor = conn.cursor()
        cursor.execute("SELECT * from ownertb where username='" + username + "' and Password='" + password + "' ")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('OwnerLogin.html')

        else:
            session['email'] = data[3]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
            cursor = conn.cursor()
            cursor.execute("truncate table temptb")
            conn.commit()
            conn.close()

            import LiveRecognition1 as liv1
            del sys.modules["LiveRecognition1"]

            return facelogin()


@app.route("/facelogin")
def facelogin():
    uname = session['oname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
    cursor = conn.cursor()
    cursor.execute("SELECT * from temptb where username='" + uname + "' ")
    data = cursor.fetchone()
    if data is None:

        flash('Face  is wrong')
        return render_template('OwnerLogin.html')


    else:

        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                       database='26documentfacedb1')
        cur = conn.cursor()
        cur.execute("SELECT * FROM ownertb where username='" + session['oname'] + "'")
        data1 = cur.fetchall()
        return render_template('OwnerHome.html', data=data1)


def loginvales1():
    uname = session['oname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ownertb where username='" + uname + "'")
    data = cursor.fetchone()

    if data:
        Email = data[3]
        Phone = data[2]




    else:
        return 'Incorrect username / password !'

    return uname, Email, Phone


@app.route('/OwnerHome')
def OwnerHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb where username='" + session['oname'] + "'")
    data1 = cur.fetchall()
    return render_template('OwnerHome.html', data=data1)


@app.route('/OwnerFileUpload')
def OwnerFileUpload():
    return render_template('OwnerFileUpload.html', oname=session['oname'])


import pyAesCrypt
import random
import string


def randStr(chars=string.ascii_uppercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))


def aeencrypt(key, source, des):
    output = des
    pyAesCrypt.encryptFile(source, output, key)
    return output


def aedecrypt(key, source, des):
    dfile = source.split(".")
    output = des

    pyAesCrypt.decryptFile(source, output, key)
    return output


import hmac
import hashlib
import binascii


def create_sha256_signature(key, message):
    byte_key = binascii.unhexlify(key)
    message = message.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()


@app.route("/owfileupload", methods=['GET', 'POST'])
def owfileupload():
    if request.method == 'POST':
        oname = session['oname']
        info = request.form['info']
        file = request.files['file']
        import random
        fnew = random.randint(111, 999)
        savename = str(fnew) + file.filename

        file.save("static/upload/" + savename)

        filepath = "./static/upload/" + savename
        head, tail = os.path.split(filepath)

        newfilepath1 = './static/upload/' + str(tail)
        newfilepath2 = './static/Encrypt/' + str(tail)

        fpubhex = randStr(chars='abcdef123456')
        key = fpubhex
        aeencrypt(key, newfilepath1, newfilepath2)

        from ecies.utils import generate_key
        from ecies import encrypt, decrypt

        # ----------------------------------
        # 1. Generate ECC key pair (secp256k1)
        # ----------------------------------
        secp_k = generate_key()
        privhex = secp_k.to_hex()  # Private key (hex)
        pubhex = secp_k.public_key.format(True).hex()  # Public key (compressed hex)

        print("Private Key:", privhex)
        print("Public Key :", pubhex)

        # ----------------------------------
        # 2. Plain text message
        # ----------------------------------
        message = fpubhex
        message_bytes = message.encode("utf-8")

        # ----------------------------------
        # 3. Encryption (using PUBLIC key)
        # ----------------------------------
        ciphertext = encrypt(pubhex, message_bytes)
        print("Encrypted (hex):", ciphertext.hex())

        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                       database='26documentfacedb1')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO filetb VALUES ('','" + oname + "','" + info + "','" + savename + "','" + ciphertext.hex() + "','" + pubhex + "','" + privhex + "')")
        conn.commit()
        conn.close()

        flash('File Upload And Encrypt Successfully ')
        return render_template('OwnerFileUpload.html', pkey=pubhex, oname=oname)


@app.route('/OwnerFileInfo')
def OwnerFileInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
    cur = conn.cursor()
    cur.execute("SELECT * FROM filetb where OwnerName='" + session['oname'] + "'")
    data1 = cur.fetchall()
    return render_template('OwnerFileInfo.html', data=data1)


@app.route("/ODownload1")
def ODownload1():
    fid = request.args.get('fid')
    session['fid'] = fid

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM  filetb where  id='" + fid + "'")
    data = cursor.fetchone()
    if data:
        prkey = data[6]
        fname = data[3]
        session["prkey"] = prkey

        sendmail(session['email'],"File Id:"+ fid + " Decrypkey: "+prkey)

        flash('Decrypt Send Successfully ')
        return render_template('OwnDownload.html')

    else:
        return 'Incorrect username / password !'





@app.route("/ODownload", methods=['GET', 'POST'])
def ODownload():
    if request.method == 'POST':
        Dkey = request.form['uname']

        if session["prkey"] ==Dkey:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='26documentfacedb1')
            cursor = conn.cursor()
            cursor.execute("SELECT  *  FROM  filetb where  id='" + session['fid'] + "'")
            data = cursor.fetchone()
            if data:
                prkey = ""
                eprkey = data[4]
                fname = data[3]

                # *****
                key = bytes.fromhex(eprkey)
                decrypted_bytes = decrypt(Dkey,key )
                decrypted_message = decrypted_bytes.decode("utf-8")

                print("Decrypted Message:", decrypted_message)



                filepath = "./static/Encrypt/" + fname
                head, tail = os.path.split(filepath)

                newfilepath1 = './static/Encrypt/' + str(tail)
                newfilepath2 = './static/Decrypt/' + str(tail)
                aedecrypt(decrypted_message, newfilepath1, newfilepath2)
                return send_file(newfilepath2, as_attachment=True)





        else:
            flash('Decrypt Key Wrong..! ')
            sendmail(session['email'],"Unknown User Access your Account..!")
            return render_template('OwnDownload.html')






def sendmail(Mailid, message):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = Mailid

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr,"tdyr kebi hnyr yzyh")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, port=10000)
    app.run(debug=True, use_reloader=True)
