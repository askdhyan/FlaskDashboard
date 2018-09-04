import requests
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, render_template
from gevent.pywsgi import WSGIServer
from jiralibrary import JiraLibrary
import json
from os import path


app = Flask(__name__)
url = "https://scvsupport.atlassian.net/rest/api/2/"

global ObjjiraLibrary
ObjjiraLibrary = None


@app.route('/')
def welcome():
    global ObjjiraLibrary
    ObjjiraLibrary = JiraLibrary()
    return render_template("Welcome.html")

@app.route('/CustomerExperienceCharts')
def Dashboard_Page1():
    global ObjjiraLibrary
    data2 = dict(ObjjiraLibrary.customerSiteData_dict)
    return render_template("CustomerExperienceCharts.html", customer_data=ObjjiraLibrary.customerData_lst, Site_data=ObjjiraLibrary.siteData_lst, Solution_data=ObjjiraLibrary.solutionData_lst, customersite_data=data2)

@app.route('/CasesBySolution')
def Dashboard_Page2():
    global ObjjiraLibrary
    data2 = dict(ObjjiraLibrary.customerSiteData_dict)
    return render_template("CasesBySolution.html", customer_data=ObjjiraLibrary.customerData_lst, Site_data=ObjjiraLibrary.siteData_lst, Solution_data=ObjjiraLibrary.solutionData_lst,casetype_data=ObjjiraLibrary.caseType_lst,  customersite_data=data2)

@app.route('/CasesByPartner')
def Dashboard_Page3():
    global ObjjiraLibrary
    data2 = dict(ObjjiraLibrary.customerSiteData_dict)
    return render_template("CasesByPartner.html", customer_data=ObjjiraLibrary.customerData_lst, Site_data=ObjjiraLibrary.siteData_lst, Partner_data=ObjjiraLibrary.partnerData_lst, Resolution_data=ObjjiraLibrary.resolutionData_lst, customersite_data=data2)

@app.route('/RMACharts')
def Dashboard_Page4():
    global ObjjiraLibrary
    return render_template("RMACharts.html")

@app.route('/ProactiveVsReactive')
def Dashboard_Page5():
    return render_template("ProactiveVsReactive.html")


@app.route('/creategraph', methods=['POST'])
def create_issue():
    try:
        global ObjjiraLibrary
        sEndDate = request.form['enddate']
        sStartDate = request.form['startdate']
        solutionParam_lst = request.form['solutionList']
        priorityParam_lst = request.form['priorityList']
        sitenameParam_lst = request.form["sitenameList"]
        customernameParam_lst = request.form["customerList"]

        # Call Function To Get Values For Gauge Charts
        data = ObjjiraLibrary.getAverageMeanTime(sStartDate, sEndDate, solutionParam_lst, priorityParam_lst, sitenameParam_lst, customernameParam_lst)
        return jsonify(data), 200

    except Exception as e:
        return "{0}Internal Server Error".format(e), 500

@app.route('/createChartForCasesBySolution', methods=['POST'])
def casesBySolution():
    try:
        global ObjjiraLibrary
        sEndDate = request.form['enddate']
        sStartDate = request.form['startdate']
        solutionParam_lst = request.form['solutionList']
        priorityParam_lst = request.form['priorityList']
        siteNameParam_lst = request.form['siteNameList']
        caseTypeParam_lst = request.form['caseTypeList']
        customernameParam_lst = request.form["customerList"]
        # Call Function To Get Values For Charts
        data = ObjjiraLibrary.getCasesBySolutionData(sStartDate, sEndDate, solutionParam_lst, priorityParam_lst, siteNameParam_lst, caseTypeParam_lst, customernameParam_lst)
        return jsonify(data), 200

    except Exception as e:

        return "{0}Internal Server Error".format(e), 500

@app.route('/createChartForCasesByPartner', methods=['POST'])
def casesByPartner():
    try:
        global ObjjiraLibrary
        sEndDate = request.form['enddate']
        sStartDate = request.form['startdate']
        partnerParam_lst = request.form['partnerList']
        priorityParam_lst = request.form['priorityList']
        siteNameParam_lst = request.form['siteNameList']
        resolutionParam_lst = request.form['resolutionList']
        customernameParam_lst = request.form["customerList"]

        # Call Function To Get Values For Charts
        data = ObjjiraLibrary.getCasesByPartnerData(sStartDate, sEndDate, partnerParam_lst, priorityParam_lst, siteNameParam_lst, resolutionParam_lst, customernameParam_lst)
        return jsonify(data), 200

    except Exception as e:

        return "{0}Internal Server Error".format(e), 500

@app.route('/CreateChartForRMACharts', methods=['POST'])
def RMACharts():
    try:
        global ObjjiraLibrary
        sEndDate = request.form['enddate']
        sStartDate = request.form['startdate']
        print sEndDate, sStartDate

        # Call Function To Get Values For Gauge Charts
        data = ObjjiraLibrary.getRMAChartsData(sStartDate, sEndDate)
        return jsonify(data), 200

    except Exception as e:

        return "{0}Internal Server Error".format(e), 500

@app.route('/CreateChartForProactiveVsReactive', methods=['POST'])
def ProactiveVsReactive():
    try:
        global ObjjiraLibrary
        sEndDate = request.form['enddate']
        sStartDate = request.form['startdate']

        # Call Function To Get Values For Gauge Charts
        data = ObjjiraLibrary.getProactiveReactiveData(sStartDate, sEndDate)
        return jsonify(data), 200

    except Exception as e:

        return "{0}Internal Server Error".format(e), 500

if __name__ == "__main__":

    http_server = WSGIServer(('0.0.0.0', 5001), app)
    http_server.serve_forever()
