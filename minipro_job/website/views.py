from django.shortcuts import render
import pandas as pd 
from .wordcloud_img import make_wordcloud
from .updater import task_crawling



# Create your views here.
def home(request):
    data = request.GET.copy()
    result_data= dict()
    if 'select' in data.keys():
        scode = change(data['select'])
        result_data['name'] = make_wordcloud(scode)

    return render(request, 'website/home.html', context=result_data)

def update(request):
    data = request.GET.copy()
    if 'select' in data.keys():
        scode = chan(data['select'])
        task_crawling(scode)
    return render(request, 'website/temp.html', context=data)

def change(value):
    codict = {
        "1": "872",
        "2": "873",
        "3": "669",
        "4": "660",
        "5": "677",
        "6": "678",
        "7": "899",
        "8": "655",
        "9": "674",
        "10": "895",
        "11": "900",
        "12": "1634",
        "13": "665",
        "14": "1024",
        "15": "877",
        "16": "565",
        "17": "564",
        "18": "559",
        "19": "563",
        "20": "554",
        "21": "656",
        "22": "552",
        "23": "1030",
        "24": "710",
        "25": "719",
        "26": "1635",
        "27": "707",
        "28": "721",
        "29": "717",
        "30": "599",
        "31": "597",
        "32": "594",
        "33": "592",
        "34": "595",
        "35": "603",
        "36": "879",
        "37": "1036",
        "38": "770",
        "39": "954",
        "40": "766",
        "41": "768",
        "42": "1035",
        "43": "955",
        "44": "1028",
        "45": "758",
        "46": "586",
        "47": "760",
        "48": "901",
        "49": "769",
        "50": "754",
        "51": "1046",
        "52": "723",
        "53": "727",
        "54": "725",
        "55": "3351",
        "56": "724",
        "57": "957",
        "58": "643",
        "59": "649",
        "60": "644",
        "61": "648",
        "62": "645",
        "63": "1043",
        "64": "647",
        "65": "1048",
        "66": "538",
        "67": "534",
        "68": "920",
        "69": "542",
        "70": "1047",
        "71": "882",
        "72": "822",
        "73": "823",
        "74": "821",
        "75": "843",
        "76": "856",
        "77": "859",
        "78": "817",
        "79": "959",
        "80": "515",
        "81": "522",
        "82": "532",
        "83": "10057",
        "84": "521",
        "85": "509",
        "86": "514"
    }
    scode = codict[value]
    return scode

def chan(value):
    codict={
        '1' : '518/872',
        '2' : '518/873',
        '3' : '518/669',
        '4' : '518/660',
        '5' : '518/677',
        '6' : '518/678',
        '7' : '518/899',
        '8' : '518/655',
        '9' : '518/674',
        '10' : '518/895',
        '11' : '518/900',
        '12' : '518/1634',
        '13' : '518/665',
        '14' : '518/1024',
        '15' : '518/877',
        '16' : '507/565',
        '17' : '507/564',
        '18' : '507/559',
        '19' : '507/563',
        '20' : '507/554',
        '21' : '507/656',
        '22' : '507/552',
        '23' : '523/1030',
        '24' : '523/710',
        '25' : '523/719',
        '26' : '523/1635',
        '27' : '523/707',
        '28' : '523/721',
        '29' : '523/717',
        '30' : '511/599',
        '31' : '511/597',
        '32' : '511/594',
        '33' : '511/592',
        '34' : '511/595',
        '35' : '511/603',
        '36' : '511/879',
        '37' : '530/1036',
        '38' : '530/770',
        '39' : '530/954',
        '40' : '530/766',
        '41' : '530/768',
        '42' : '530/1035',
        '43' : '530/955',
        '44' : '510/1028',
        '45' : '510/758',
        '46' : '510/586',
        '47' : '510/760',
        '48' : '510/901',
        '49' : '510/769',
        '50' : '510/754',
        '51' : '524/1046',
        '52' : '524/723',
        '53' : '524/727',
        '54' : '524/725',
        '55' : '524/3351',
        '56' : '524/724',
        '57' : '524/957',
        '58' : '517/643',
        '59' : '517/649',
        '60' : '517/644',
        '61' : '517/648',
        '62' : '517/645',
        '63' : '517/1043',
        '64' : '517/647',
        '65' : '508/1048',
        '66' : '508/538',
        '67' : '508/534',
        '68' : '508/920',
        '69' : '508/542',
        '70' : '508/1047',
        '71' : '508/882',
        '72' : '513/822',
        '73' : '513/823',
        '74' : '513/821',
        '75' : '513/843',
        '76' : '513/856',
        '77' : '513/859',
        '78' : '513/817',
        '79' : '959',
        '80' : '515',
        '81' : '522',
        '82' : '532',
        '83' : '10057',
        '84' : '521',
        '85' : '509',
        '86' : '514',
    }
    scode = codict[value]
    return scode


# def showwordcloud(request):
#     data = request.GET.copy()
#     # makewordcloud(data) 
#     return render(request, 'webstie/wordcloud_page.html', context=data)
