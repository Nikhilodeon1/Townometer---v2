from flask import Flask, render_template, request, redirect, url_for, make_response
import urllib3
import requests
#4/15/23
http = urllib3.PoolManager()
app = Flask(__name__)
app.secret_key = "|\|||<|-|||_"

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    city = request.form["city"].lower()
    DEcity = city.replace(' ', '-')
    state = request.form["state"]
    PONum = int(request.form["PONum"])
    #cityPOP
    api_url = 'https://api.api-ninjas.com/v1/city?name={}'.format(city)
    egrass = requests.get(api_url, headers={'X-Api-Key': 'XMQcVMoacSgF1+0lmqW8Fw==7amKHAnddZzZRymT'})
    a = egrass.text.split('population": ')
    try:
        b = a[1].split(', "is_capital": false}]')
    except:
        return redirect(url_for('err'))
    cityPop = int(b[0])
    #crime rates
    violentRatio = 0.0570397112
    propertyRatio =  0.0199068685
    response1 = http.request("GET", "https://www.cityrating.com/crime-statistics/{}/{}.html".format(state, DEcity))
    resp1 = response1.data.decode("utf-8")
    rp1 = resp1.split('Property Crime</span></td><td class="value">')
    rp2 = rp1[1].split('<td class="key"><span class="total">Violent Crime')
    property = rp2[0]
    try:
        property = property.removesuffix('</td>\r\n</tr><tr>\r\n')
        p1 = property.split(',')
        intP = int(p1[0] + p1[1])
    except:
        intP= int(property)
    rv1 = resp1.split('<td class="key"><span class="total">Violent Crime</span></td><td class="value">')
    rv2 = rv1[1].split('<table class="table table-striped" cellspacing="0" id="contentMain_grdSummaryEstimate" style="border-collapse:collapse;">')
    
    violent = rv2[0]
    #violent = "12,132"
    
    try:
        violent = violent.removesuffix('</td>\r\n</tr>\r\n</table>\r\n</div>\r\n<div>\r\n')
        v1 = violent.split(',')
        intV = int(v1[0] + v1[1])
    except:
        violent = violent.removesuffix('</td>\r\n</tr>\r\n</table>\r\n</div>\r\n<div>\r\n')
        intV= int(violent)
    
    finalP = intP * propertyRatio
    finalV = intV * violentRatio
    cityAVG = round((finalP + finalV)/2)
    #police number
    recRatio = 450 #according to a .gov page
    cityRatio = round(cityPop / PONum)
    next = ''
    #return [cityAVG]
    if cityRatio - recRatio > 50 and cityAVG < 29:
        #need less officers
        next  = 'less'
    elif PONum > 100000:
        #need less officers
        next  = 'less'
    elif cityAVG > 50:
        #need more officers
        next = 'more'
    elif recRatio - cityRatio > 50 and cityAVG > 29:
        #need more officers
        next = 'more'
    else:
        #same officers
        next = 'same'

    return render_template('results.html', next=next, city=city, PONum=PONum, cityRatio=cityRatio, state=state)

@app.route('/err', methods=['GET', 'POST'])
def err():
    return render_template('err.html', problem="WRONG")