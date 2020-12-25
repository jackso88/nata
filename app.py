import smtplib
import yaml

from flask import Flask, render_template, request, redirect, url_for
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

app = Flask(__name__)

def mail(subj, email, mess, per):
    addr_from = config['mail']['from']
    addr_to = config['mail']['to']
    password = config['mail']['pass']

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = subj

    body = str(per) + '\n' + str(email) + '\n' + str(mess)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(True)
    server.starttls()
    server.login(addr_from, password)
    try:
        server.send_message(msg)
    except:
        return "Your message is missing"
    server.quit()


@app.route('/')
def home() -> 'html':
    return render_template('home.html')
    

@app.route('/portfolio')
def portfolio() -> 'html':
    return render_template('portfolio.html')
    
    
@app.route('/pricing')
def pricing() -> 'html':
    return render_template('pricing.html')


@app.route('/blog')
def blog() -> 'html':
    return render_template('blog.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact() -> 'html':
    if request.method == 'POST':
        mail(
            request.form['subject'],
            request.form['email'],
            request.form['message'],
            request.form['name']
            )
        return render_template('contact.html')
    else:
        return render_template('contact.html')
    
if __name__ == '__main__':
    app.run(debug=True)
