from operator import itemgetter
import os
import calendar
from jira.client import JIRA
from datetime import datetime
from dateutil import relativedelta
from xlrd import open_workbook
from collections import OrderedDict


class JiraLibrary:

    def __init__(self):
        try:
            # JIRA username
            sJIRAUsername = 'meet.shah@einfochips.com'
            # JIRA password
            sJIRAPassword = 'einfochips@123'

            # create JIRA Object
            self.jira_obj = JIRA('https://scvsupport.atlassian.net', basic_auth=('{0}'.format(sJIRAUsername), '{0}'.format(sJIRAPassword)))

            self.getCustomerSolutionDataFromJIRA()

        except Exception as e:
            pass

    def convertListToString(self, dataParam_lst=None):
        try:
            # below code is used to convert list values into string values
            sValue = ''
            ilengthOfList = len(dataParam_lst)
            iCounter = 1

            # iterate over all the solution one-by-one
            for sTempValue in dataParam_lst:
                if ilengthOfList != iCounter:
                    sValue = sValue + '"{0}"'.format(sTempValue) + ', '
                else:
                    sValue = sValue + '"{0}"'.format(sTempValue)

                # increment the counter value by 1
                iCounter = iCounter + 1

        except Exception as e:
            pass

        return sValue

    def convertDateFormat(self, startDateParam=None, endDateParam=None):
        try:

            yyyyFormat = int(str(startDateParam).split('/')[1])
            mmFormat = int(str(startDateParam).split('/')[0])
            if (mmFormat != 10) and (mmFormat != 11) and (mmFormat != 12):
                startDateParam = '{0}-0{1}-01'.format(str(yyyyFormat), str(mmFormat))
            else:
                startDateParam = '{0}-{1}-01'.format(str(yyyyFormat), str(mmFormat))

            yyyyFormat = int(str(endDateParam).split('/')[1])
            mmFormat = int(str(endDateParam).split('/')[0])
            noOfDays_int = int(calendar.monthrange(yyyyFormat, mmFormat)[1])
            if (mmFormat != 10) and (mmFormat != 11) and (mmFormat != 12):
                endDateParam = '{0}-0{1}-{2}'.format(str(yyyyFormat), str(mmFormat), str(noOfDays_int))
            else:
                endDateParam = '{0}-{1}-{2}'.format(str(yyyyFormat), str(mmFormat), str(noOfDays_int))

        except Exception as e:
            pass

        return startDateParam, endDateParam

    def getSolutionFromListToString(self):
        try:
            # below code is used to convert list values into string values
            sUserSolutionValue = ''
            ilengthOfSolutionList = len(self.solutionData_lst)
            iSolutionCounter = 1

            # iterate over all the solution one-by-one
            for sSolution in self.solutionData_lst:
                if ilengthOfSolutionList != iSolutionCounter:
                    sUserSolutionValue = sUserSolutionValue + '"{0}"'.format(sSolution) + ', '
                else:
                    sUserSolutionValue = sUserSolutionValue + '"{0}"'.format(sSolution)

                # increment the counter value by 1
                iSolutionCounter = iSolutionCounter + 1

        except Exception as e:
            pass

        return sUserSolutionValue

    def getSiteNameFromListToString(self):
        try:
            sUserSiteNameValue = ''
            iLengthOfSiteNameList = len(self.organizationIdName_dict.keys())
            iSiteNameCounter = 1
            for id1 in self.organizationIdName_dict.keys():

                if iLengthOfSiteNameList != iSiteNameCounter:
                    sUserSiteNameValue = sUserSiteNameValue + str(id1) + ', '
                else:
                    sUserSiteNameValue = sUserSiteNameValue + str(id1)

                iSiteNameCounter = iSiteNameCounter + 1

        except Exception as e:
            pass

        return sUserSiteNameValue

    def getIssueTypeFromListToString(self):
        try:
            # below code is used to convert list values into string values
            sUserCaseTypeValue = ''
            ilengthOfCaseTypeList = len(self.caseType_lst)
            iCaseTypeCounter = 1

            # iterate over all the solution one-by-one
            for sCaseType in self.caseType_lst:
                if ilengthOfCaseTypeList != iCaseTypeCounter:
                    sUserCaseTypeValue = sUserCaseTypeValue + '"{0}"'.format(sCaseType) + ', '
                else:
                    sUserCaseTypeValue = sUserCaseTypeValue + '"{0}"'.format(sCaseType)

                # increment the counter value by 1
                iCaseTypeCounter = iCaseTypeCounter + 1

        except Exception as e:
            pass

        return sUserCaseTypeValue

    def getCustomerSolutionDataFromJIRA(self):
        '''
            Function Purpose:
                purpose : this function is used to retrieve all the solution and priority value from JIRA and storing that value into a list
        '''
        try:
            jqlQueryToRetrieveDataForSolutionAndCustomer = '(project = VSCS)'
            allJIRAIssues = self.jira_obj.search_issues(jqlQueryToRetrieveDataForSolutionAndCustomer, maxResults=False, fields='issuetype, customfield_10004, customfield_10045')

            # creating an empty list to store the company (organization) name
            self.customerData_lst = []
            # creating an empty list to store the site name
            self.siteData_lst = []
            # creating an empty list to store the Solution Value
            self.solutionData_lst = []
            # creating an dictionary to store the customer and site data. customer data as a key and site name as a value
            self.customerSiteData_dict = OrderedDict()
            # creating an dictionary to store the organization id as a dictionary key and customer name as a dictionary value
            self.organizationIdName_dict = OrderedDict()
            # creating an empty list to store the Case Type value
            self.caseType_lst = []
            # creating an dictionary to store Organization ID as a key and whole Name(Customer and Site Name) as value
            self.organizationIdCustomerSiteName_dict = OrderedDict()

            ''' Code Added as Stub '''

            # creating an empty list to store the Partner value
            self.partnerData_lst = []
            # creating an empty list to store the Resolution value
            self.resolutionData_lst = []

            ''' Stub Code Over '''

            # JIRA ISSUE FOUND
            if allJIRAIssues:

                # iterate over all the JIRA issue one-by-one
                for specificIssue in allJIRAIssues:
                    # this if condition is used to store the "Case Type" value into a list
                    if 'issuetype' in specificIssue.raw['fields'].keys():
                        if 'name' in specificIssue.raw['fields']['issuetype'].keys():
                            caseType_str = str(specificIssue.raw['fields']['issuetype']['name'])
                            self.caseType_lst.append(caseType_str)

                    # if data for customer name exists in fields dictionary then and then only go ahead
                    if 'customfield_10004' in specificIssue.raw['fields'].keys():
                        # if len of list is not equal to 0 then and then only go ahead
                        if len(specificIssue.raw['fields']['customfield_10004']) != 0:
                            organizationId_int = int(specificIssue.raw['fields']['customfield_10004'][0]['id'])
                            customerName_str = str(specificIssue.raw['fields']['customfield_10004'][0]['name'])
                            if customerName_str not in self.customerData_lst:
                                lenOfHypenInCustomerName_int = customerName_str.count('-')

                                self.organizationIdCustomerSiteName_dict[organizationId_int] = customerName_str

                                # this if condition is used for Partner - Verizon ( here, "-" (hyphen) is used for once only)
                                if lenOfHypenInCustomerName_int == 1:
                                    tempCustomerName_str = str(customerName_str).split('-')[0].strip()
                                    self.customerData_lst.append(tempCustomerName_str)
                                    tempSiteName_str = str(customerName_str).split('-')[1]
                                    siteName_str = str('{0}'.format(tempSiteName_str)).strip()
                                    self.siteData_lst.append(siteName_str)

                                    self.organizationIdName_dict[organizationId_int] = siteName_str
                                    if tempCustomerName_str not in self.customerSiteData_dict.keys():
                                        self.customerSiteData_dict[tempCustomerName_str] = [siteName_str]
                                    elif tempCustomerName_str in self.customerSiteData_dict.keys():
                                        if siteName_str not in self.customerSiteData_dict[tempCustomerName_str]:
                                            self.customerSiteData_dict[tempCustomerName_str] = self.customerSiteData_dict[tempCustomerName_str] + [siteName_str]

                                # this if condition is used for when two "-" (hyphen) are there in customer name
                                elif lenOfHypenInCustomerName_int == 2:
                                    tempCustomerName_str = str(customerName_str).split('-')[0].strip()
                                    self.customerData_lst.append(tempCustomerName_str)
                                    siteName_str = str('{0}-{1}'.format(str(customerName_str).split('-')[1], str(customerName_str).split('-')[2])).strip()
                                    self.siteData_lst.append(siteName_str)

                                    self.organizationIdName_dict[organizationId_int] = siteName_str
                                    if tempCustomerName_str not in self.customerSiteData_dict.keys():
                                        self.customerSiteData_dict[tempCustomerName_str] = [siteName_str]
                                    elif tempCustomerName_str in self.customerSiteData_dict.keys():
                                        if siteName_str not in self.customerSiteData_dict[tempCustomerName_str]:
                                            self.customerSiteData_dict[tempCustomerName_str] = self.customerSiteData_dict[tempCustomerName_str] + [siteName_str]

                    # if data for solution value exists in fields dictionary then and then only go ahead
                    if 'customfield_10045' in specificIssue.raw['fields'].keys():
                        # if dictionary (['customfield_10045']) value is not None then and then only go ahead
                        if specificIssue.raw['fields']['customfield_10045'] is not None:
                            if 'value' in specificIssue.raw['fields']['customfield_10045'].keys():
                                solutionName_str = str(specificIssue.raw['fields']['customfield_10045']['value'])
                                if solutionName_str not in self.solutionData_lst:
                                    self.solutionData_lst.append(solutionName_str)

        except Exception as e:
            pass

        finally:
            self.caseType_lst = list(set(self.caseType_lst))
            self.customerData_lst = list(set(self.customerData_lst))
            self.siteData_lst = list(set(self.siteData_lst))

            ''' Code Added as Stub '''

            self.partnerData_lst = ["PAR1", "PAR2", "PAR3"]
            self.resolutionData_lst = ["RES1", "RES2","RES3"]

            ''' Stub Code Over '''

    def getSiteNamesBasedOnCustomerName(self, customerName_str=None):
        try:
            if customerName_str in self.customerSiteData_dict.keys():
                return self.customerSiteData_dict[customerName_str]
        except Exception as e:
            pass

    def readBGCODataFromSpreadsheetFile(self):
        try:
            dirName = os.path.join(os.path.dirname(__file__), '../TestData/')
            bgcoTestDataFilePath_str = str(dirName + '/' + 'BGCO_TestData.xlsx')

            # if file exists then go ahead to read the file
            if os.path.isfile(bgcoTestDataFilePath_str):
                # open the workbook
                book = open_workbook(bgcoTestDataFilePath_str)
                # get sheet based on 0 index
                sheet = book.sheet_by_index(0)
                # iterate over the no.of.rows of sheet
                for rowNumber in range(1, sheet.nrows):
                    completed_str = str(sheet.cell(rowNumber, 15).value)
                    receivedDate_str = str(sheet.cell(rowNumber, 16).value)

                    completedDate_date = datetime.strptime(completed_str,'%d/%m/%Y %H:%M:%S MDT')
                    receivedDate_date = datetime.strptime(receivedDate_str,'%d/%m/%Y %H:%M:%S MDT')

        except Exception as e:
            pass

    def calculateValueForMeanTimeToRespondOrClose(self, sDifferenceOfRespondTime=None):
        '''
            Function Purpose:
                purpose : this function is used to calculate the difference time and provide the no.of.days as a return value
            Function Parameters:
                sDifferenceOfRespondTime (string) : '30 days, 00:00:00'
            Function Return Value:
                return value : this function return 1 integer value
        '''
        try:
            calculatedValueForMeanTimeToRespondOrClose = 0
            hour_str = sDifferenceOfRespondTime.split(':')[0]
            minute_str = sDifferenceOfRespondTime.split(':')[1]

            # if there are no.of.days
            if ',' in sDifferenceOfRespondTime:
                noOfDay_int = str(sDifferenceOfRespondTime).split( )[0]
                perDayMinute_int = int((int(noOfDay_int) * 24) * 60)
                hour_str = str(sDifferenceOfRespondTime).split(', ')[1].split(':')[0]
                minute_str = str(sDifferenceOfRespondTime).split(', ')[1].split(':')[1]

                # calculate value
                calculatedValueForMeanTimeToRespondOrClose = int(minute_str) + int(int(hour_str) * 60) + int(perDayMinute_int)

            # if there are no hours (0 hours)
            elif int(hour_str) == 0:
                calculatedValueForMeanTimeToRespondOrClose = int(minute_str)
            # if there are hours
            elif int(hour_str) != 0:
                calculatedValueForMeanTimeToRespondOrClose = int(minute_str) + int(int(hour_str) * 60)

        except Exception as e:
            pass

        # here, function return 1 integer value
        return int(calculatedValueForMeanTimeToRespondOrClose)

    def getAverageMeanTimeToRespondOrClose(self, allJIRAIssues=None, getAverageMeanTimeFor=None):
        '''
            Function Purpose:
                purpose : this function is used to calculate and get the "Average Mean Time To Respond Value"
            Function Parameters:
                allJIRAIssues (ResultSetList) : list of all JIRA issues (JIRA issue id)
            Function Return Value:
                return value : this function return 1 integer value
        '''
        try:
            averageMeanTimeValue_int = 0

            # iterate over all the JIRA issue one-by-one
            for specificIssue in allJIRAIssues:
                sCreatedDate = str(specificIssue.raw['fields']['created']).split('.')[0]
                createdDate_date = datetime.strptime(sCreatedDate,'%Y-%m-%dT%H:%M:%S')

                commentOrResolutionDate_date = None
                # if condition for - Mean Time to Respond
                if getAverageMeanTimeFor == 'Mean Time To Respond':
                    if len(specificIssue.raw['fields']['comment']['comments']) == 0:
                        continue
                    else:
                        sCommentDate = str(specificIssue.raw['fields']['comment']['comments'][0]['created']).split('.')[0]

                    # convert resolution date value string into date format in respect to get value for "Mean Time To Respond"
                    commentOrResolutionDate_date = datetime.strptime(sCommentDate,'%Y-%m-%dT%H:%M:%S')

                # if condition for - Mean Time To Close
                elif getAverageMeanTimeFor == 'Mean Time To Close':

                    # retrieve resolution date value from jira issue
                    if specificIssue.raw['fields']['resolutiondate'] is not None:
                        sResolutionDate = str(specificIssue.raw['fields']['resolutiondate']).split('.')[0]
                        # convert resolution date value string into date format in respect to get value for "Mean Time To Close"
                        commentOrResolutionDate_date = datetime.strptime(sResolutionDate,'%Y-%m-%dT%H:%M:%S')

                if commentOrResolutionDate_date is not None:
                    # here, we are subtracting two date (comment/resolution date - created date)
                    sDifferenceOfRespondTime = str(commentOrResolutionDate_date - createdDate_date)
                    calculatedValueForMeanTimeToRespondOrClose = self.calculateValueForMeanTimeToRespondOrClose(sDifferenceOfRespondTime=sDifferenceOfRespondTime)

                    averageMeanTimeValue_int = averageMeanTimeValue_int + calculatedValueForMeanTimeToRespondOrClose

        except Exception as e:
            pass

        # here, function return 1 integer value
        return int(averageMeanTimeValue_int)

    def getAverageMeanTime(self, startDateParam=None, endDateParam=None, solutionParam_str=None, priorityParam_str=None, siteNameParam_str=None, customerNameParam_str=None):
        '''
            Function Purpose:
                purpose : this function is used to get the average mean based on the requirement like: 'Mean Time To Respond', etc.
            Function Parameters:
                startDateParam (string) : '2018-07-01'
                endDateParam (string) : '2018-07-31'
                solutionParam_str (str) : 'IL - Intelligent Lighting'
                priorityParam_str (str) : 'Major'
            Function Return Value:
                return value : this function return 1 integer value
        '''
        try:
            # creating an dictionary to store the value for different charts value along with number.of.issues count, in this dictionary, -1 value means "No JIRA Issue found"
            averageMeanTimeData_dict = {}

            sUserSolutionValue = solutionParam_str
            sUserPriorityValue = priorityParam_str
            sUserSiteNameValue = siteNameParam_str

            # this if condition is used to convert list into string
            if solutionParam_str == 'ALL':
                sUserSolutionValue = self.getSolutionFromListToString()
            # this elif condition is used for only single Solution Value 
            else:
                sUserSolutionValue = '"{0}"'.format(sUserSolutionValue)

            # if priority value is ALL then consider all the priorities
            if priorityParam_str == 'ALL':
                sUserPriorityValue = '"Critical", "Major", "Minor"'
            # this else condition is used for Single Priority value
            else:
                sUserPriorityValue = '"{0}"'.format(sUserPriorityValue)

            if customerNameParam_str == 'ALL':
                # this if condition is used for multiple customers
                if siteNameParam_str == 'ALL':
                    sUserSiteNameValue = self.getSiteNameFromListToString()
                # this else condition is used for single customer
                else:
                    # here, we are iterating the loop over self.organizationIdName_dict to get the organization id based on the site name
                    sUserSiteNameValue = [id1 for id1, name in self.organizationIdName_dict.items() if name == siteNameParam_str][0]
            else:
                tempSiteName_lst = self.getSiteNamesBasedOnCustomerName(customerName_str=customerNameParam_str)

                if siteNameParam_str == 'ALL':
                    sUserSiteNameValue = ''
                    iCounter = 1
                    lengthOfTempSiteNameList_int = len(tempSiteName_lst)
                    for key, value in self.organizationIdName_dict.items():
                        if value in tempSiteName_lst:
                            if lengthOfTempSiteNameList_int != iCounter:
                                sUserSiteNameValue = sUserSiteNameValue + '{0}'.format(key) + ', '
                            else:
                                sUserSiteNameValue = sUserSiteNameValue + '{0}'.format(key)

                            # increment the counter value by 1
                            iCounter = iCounter + 1

                else:
                    sUserSiteNameValue = [id1 for id1, name in self.organizationIdName_dict.items() if name == siteNameParam_str][0]

            # creating an empty list and later on appending different charts name into this list
            chartName_lst = []
            chartName_lst.append('Mean Time To Respond')
            chartName_lst.append('Mean Time To Close')
            chartName_lst.append('Mean Time For Between Incidents')

            # iterate over all the chart one-by-one
            for chartName in chartName_lst:
                # below if condition is used for particular 1 chart i.e. "Mean Time To Close"
                if chartName == 'Mean Time To Close':
                    jqlQuery = '(project = VSCS) and (resolutiondate > {0} and resolutiondate < {1}) and ("Product Type" in ({2})) and (Priority in ({3})) and (Organizations in ({4}))'.format(startDateParam, endDateParam, sUserSolutionValue, sUserPriorityValue, str(sUserSiteNameValue))

                    # execute the JQL and search for the JIRA issues
                    allJIRAIssues = self.jira_obj.search_issues(jqlQuery, maxResults=False, fields='customfield_10045, priority, created, resolutiondate')

                # below else condition is used for charts like: "Mean Time To Respond" and "Mean Time For Between Incidents"
                else:
                    jqlQuery = '(project = VSCS) and (Created > {0} and Created < {1}) and ("Product Type" in ({2})) and (Priority in ({3})) and (Organizations in ({4}))'.format(startDateParam, endDateParam, sUserSolutionValue, sUserPriorityValue, str(sUserSiteNameValue))

                    # execute the JQL and search for the JIRA issues
                    allJIRAIssues = self.jira_obj.search_issues(jqlQuery, maxResults=False, fields='customfield_10045, priority, created, comment')

                # get total number of JIRA issues that are retrieve based on the JQL executed
                iLengthOfAllIssues = len(allJIRAIssues)

                # here, JIRA issue found
                if allJIRAIssues:
                    # this if condition is used for "Mean Time To Respond"
                    if chartName == 'Mean Time To Respond':
                        averageMeanTimeToRespondValue_int = self.getAverageMeanTimeToRespondOrClose(allJIRAIssues=allJIRAIssues, getAverageMeanTimeFor='Mean Time To Respond')
                        averageMeanTimeToRespondValue_int = averageMeanTimeToRespondValue_int / iLengthOfAllIssues
                        averageMeanTimeData_dict['Mean Time To Respond'] = '{0}|{1}'.format(averageMeanTimeToRespondValue_int, iLengthOfAllIssues)

                    # this elif condition is used for "Mean Time To Close"
                    elif chartName == 'Mean Time To Close':
                        averageMeanTimeToCloseValue_int = self.getAverageMeanTimeToRespondOrClose(allJIRAIssues=allJIRAIssues, getAverageMeanTimeFor='Mean Time To Close')
                        averageMeanTimeToCloseValue_int = averageMeanTimeToCloseValue_int / iLengthOfAllIssues
                        averageMeanTimeData_dict['Mean Time To Close'] = '{0}|{1}'.format(averageMeanTimeToCloseValue_int, iLengthOfAllIssues)

                    # this elif condition is used for "Mean Time For Between Incidents"
                    elif chartName == 'Mean Time For Between Incidents':
                        # convert start date value string into date format
                        startDate_date = datetime.strptime(startDateParam,'%Y-%m-%d')
                        # convert end date value string into date format
                        endDate_date = datetime.strptime(endDateParam,'%Y-%m-%d')
                        differenceValue_int = int((endDate_date - startDate_date).days) + 1
                        averageMeanTimeForBetweenIncidentsValue_int = (differenceValue_int * 24) / iLengthOfAllIssues
                        averageMeanTimeData_dict['Mean Time For Between Incidents'] = '{0}|{1}'.format(averageMeanTimeForBetweenIncidentsValue_int, iLengthOfAllIssues)

                # No JIRA issue found
                else:
                    # this if condition is used for "Mean Time To Respond"
                    if chartName == 'Mean Time To Respond':
                        averageMeanTimeData_dict['Mean Time To Respond'] = '-1|-1'
                    # this elif condition is used for "Mean Time To Close"
                    elif chartName == 'Mean Time To Close':
                        averageMeanTimeData_dict['Mean Time To Close'] = '-1|-1'
                    # this elif condition is used for "Mean Time For Between Incidents"
                    elif chartName == 'Mean Time For Between Incidents':
                        averageMeanTimeData_dict['Mean Time For Between Incidents'] = '-1|-1'

        except Exception as e:
            pass

        # here, function return 1 dictionary
        return averageMeanTimeData_dict

    def getCasesBySolutionData(self, startDateParam=None, endDateParam=None, solutionParam_str=None, priorityParam_str=None, siteNameParam_str=None, issueTypeParam_str=None, customerNameParam_str=None):
        '''
            Function Purpose:
                purpose : this function is used to get the data for the "Cases By Solution"
            Function Parameters:
                startDateParam (string) : '02/2018'
                endDateParam (string) : '08/2018'
                solutionParam_str (str) : 'ALL' or 'IL - Intelligent Lighting'
                priorityParam_str (str) : 'ALL' or 'Major'
                siteNameParam_str (str) : 'ALL' or 'Brea Mall - Brea CA'
                issueTypeParam_str (str) : 'ALL' or 'Product Issue'
                customerNameParam_str (str) : 'ALL' or 'Simon Properties'
            Function Return Value:
                return value : this function return list where list consists of dictionary.
                Example:
                    [{
                        "Month": "Jan-2018",
                        "IL - Intelligent Lighting": 10,
                        "IP - Intelligent Parking": 20
                    },
                    {
                        "Month": "Feb-2018",
                        "IL - Intelligent Lighting": 20,
                        "IP - Intelligent Parking": 10
                    }]
        '''
        try:
            tempSolutionData_lst = []
            for tempSolutionName in solutionParam_str.split(','):
                tempSolutionData_lst.append(str(tempSolutionName))

            # convert the date in appropriate format
            startDateParam, endDateParam = self.convertDateFormat(startDateParam=startDateParam, endDateParam=endDateParam)

            totalMonthNumber_lst = []
            startingMonthNumber_str = str(startDateParam).split('-')[1]
            tempStartDateParam = datetime.strptime(str(startDateParam), '%Y-%m-%d')
            tempEndDateParam = datetime.strptime(str(endDateParam), '%Y-%m-%d')
            relativeDeltaValue = relativedelta.relativedelta(tempEndDateParam, tempStartDateParam)

            # this if condition is used if no.of.years are 0
            if relativeDeltaValue.years == 0:
                for i in range(relativeDeltaValue.months + 1):
                    totalMonthNumber_lst.append(int(startingMonthNumber_str) + 0)
                    if int(startingMonthNumber_str) == 12:
                        startingMonthNumber_str = 1
                    else:
                        startingMonthNumber_str = int(startingMonthNumber_str) + 1
            # this else condition is used if no.of.years are 1 or more
            else:
                totalMonths = int(relativeDeltaValue.months) + 12
                for i in range(totalMonths + 1):
                    totalMonthNumber_lst.append(int(startingMonthNumber_str) + 0)
                    if int(startingMonthNumber_str) == 12:
                        startingMonthNumber_str = 1
                    else:
                        startingMonthNumber_str = int(startingMonthNumber_str) + 1

            totalMonthNumber_lst = list(set(totalMonthNumber_lst))
            # here, we are creating an empty list to store the dictionary
            casesBySolutionData_lst = []

            sUserSolutionValue = solutionParam_str
            sUserPriorityValue = priorityParam_str
            sUserSiteNameValue = siteNameParam_str
            sUserCaseTypeValue = issueTypeParam_str

            # this if condition is used to convert list into string
            if solutionParam_str == 'ALL':
                sUserSolutionValue = self.getSolutionFromListToString()
            # this elif condition is used for only single Solution Value
            else:
                sUserSolutionValue = self.convertListToString(dataParam_lst=tempSolutionData_lst)

            # if priority value is ALL then consider all the priorities
            if priorityParam_str == 'ALL':
                sUserPriorityValue = '"Critical", "Major", "Minor"'
            # this else condition is used for Single Priority value
            else:
                sUserPriorityValue = '"{0}"'.format(sUserPriorityValue)

            # this if condition is used to convert list into string
            if issueTypeParam_str == 'ALL':
                sUserCaseTypeValue = self.getIssueTypeFromListToString()
            else:
                sUserCaseTypeValue = '"{0}"'.format(sUserCaseTypeValue)

            if customerNameParam_str == 'ALL':
                # this if condition is used for multiple customers
                if siteNameParam_str == 'ALL':
                    sUserSiteNameValue = self.getSiteNameFromListToString()
                # this else condition is used for single customer
                else:
                    # here, we are iterating the loop over self.organizationIdName_dict to get the organization id based on the site name
                    sUserSiteNameValue = [id1 for id1, name in self.organizationIdName_dict.items() if name == siteNameParam_str][0]
            else:
                tempSiteName_lst = self.getSiteNamesBasedOnCustomerName(customerName_str=customerNameParam_str)

                if siteNameParam_str == 'ALL':
                    sUserSiteNameValue = ''
                    iCounter = 1
                    lengthOfTempSiteNameList_int = len(tempSiteName_lst)
                    for key, value in self.organizationIdName_dict.items():
                        if value in tempSiteName_lst:
                            if lengthOfTempSiteNameList_int != iCounter:
                                sUserSiteNameValue = sUserSiteNameValue + '{0}'.format(key) + ', '
                            else:
                                sUserSiteNameValue = sUserSiteNameValue + '{0}'.format(key)

                            # increment the counter value by 1
                            iCounter = iCounter + 1

                else:
                    sUserSiteNameValue = [id1 for id1, name in self.organizationIdName_dict.items() if name == siteNameParam_str][0]

            # this is the JQL Query which are going to execute for "Cases By Solution"
            jqlQuery = '(project = VSCS) and (Created > {0} and Created < {1}) and ("Product Type" in ({2})) and (Priority in ({3})) and (Organizations in ({4})) and (issuetype in ({5}))'.format(startDateParam, endDateParam, sUserSolutionValue, sUserPriorityValue, str(sUserSiteNameValue), sUserCaseTypeValue)

            # execute the JQL and search for the JIRA issues
            allJIRAIssues = self.jira_obj.search_issues(jqlQuery, maxResults=False, fields='created, customfield_10045, key')
            # here, JIRA issues found
            if allJIRAIssues:
                # iterate over all the JIRA issue one-by-one
                tempMonthWiseData_dict = {}

                # iterate over all the JIRA issue one-by-one
                for specificIssue in allJIRAIssues:

                    # if data for solution value exists in fields dictionary then and then only go ahead
                    if 'customfield_10045' in specificIssue.raw['fields'].keys():
                        # if dictionary (['customfield_10045']) value is not None then and then only go ahead
                        if specificIssue.raw['fields']['customfield_10045'] is not None:
                            if 'value' in specificIssue.raw['fields']['customfield_10045'].keys():
                                solutionName_str = str(specificIssue.raw['fields']['customfield_10045']['value'])

                    if 'created' in specificIssue.raw['fields'].keys():
                        yearNumber_str = str(specificIssue.raw['fields']['created']).split('-')[0]

                        if int(str(specificIssue.raw['fields']['created']).split('-')[1]) in totalMonthNumber_lst:
                            monthNumber_str = str(specificIssue.raw['fields']['created']).split('-')[1]
                            monthName_str = str(calendar.month_abbr[int(monthNumber_str)])
                            monthName_str = '{0}-{1}'.format(monthName_str, yearNumber_str)
                            monthName_str = datetime.strptime(monthName_str,'%b-%Y')

                    # if month does not exists then go ahead
                    if monthName_str not in tempMonthWiseData_dict.keys():
                        tempSolutionData_dict = {}
                        tempSolutionData_dict[solutionName_str] = 1
                        tempMonthWiseData_dict[monthName_str] = tempSolutionData_dict
                    # if month exists then go ahead
                    else:
                        tempRetrieveSolutionData_dict = tempMonthWiseData_dict[monthName_str]
                        # if solution does not exists then go ahead
                        if solutionName_str not in tempRetrieveSolutionData_dict.keys():
                            tempSolutionData_dict = {}
                            tempSolutionData_dict[solutionName_str] = 1
                            tempMonthWiseData_dict[monthName_str].update(tempSolutionData_dict)
                        # if solution exists then go ahead
                        else:
                            tempCountValue_int = tempRetrieveSolutionData_dict[solutionName_str]
                            tempCountValue_int = tempCountValue_int + 1
                            tempRetrieveSolutionData_dict[solutionName_str] = tempCountValue_int
                            tempMonthWiseData_dict[monthName_str].update(tempRetrieveSolutionData_dict)

                tempMonthWiseData_lst = sorted(tempMonthWiseData_dict.items(), key=itemgetter(0))
                # iterate month wise one-by-one
                for tempMonthWiseDataListValue in tempMonthWiseData_lst:
                    tempData_dict = {}
                    tempData_dict['Month'] = datetime.strftime(tempMonthWiseDataListValue[0], '%b-%Y')

                    for tempSolutionName in tempMonthWiseDataListValue[1].keys():
                        tempSolutionCounterValue = tempMonthWiseDataListValue[1][tempSolutionName]
                        tempData_dict[tempSolutionName] = tempSolutionCounterValue

                    # append the dictionary into a list
                    casesBySolutionData_lst.append(tempData_dict)

            else:
                casesBySolutionData_lst.append('-1')

        except Exception as e:
            pass

        return casesBySolutionData_lst

    ''' Code Added as Stub '''

    def getCasesByPartnerData(self, startDateParam=None, endDateParam=None, partnerParam_str=None, priorityParam_str=None, siteNameParam_str=None, resolutionParam_str=None,customerParam_str=None):
        '''
            Function Purpose:
                purpose : this function is used to get the data for the "Cases By Partner"
            Function Parameters:
                startDateParam (string) : '07/2018'
                endDateParam (string) : '07/2018'
                partnerParam_str (str) : 'BGCO'
                priorityParam_str (str) : 'Major'
                siteNameParam_str (str) : 'Brea Mall - Brea CA'
                resolutionParam_str (str) : 'Product Issue'
                customerParam_str (str) : 'Simon Properties'
            Function Return Value:
                return value : this function return list where list consists of dictionary.
                Example:
                    [{
                        "Month": "Jan - 2018",
                        "BGCO": 10,
                    },
                    {
                        "Month": "Feb - 2018",
                        "Axis": 20,
                    }]
        '''
        try:
            data = [{
                        "Month": "Jan - 2018",
                        "BGCO": 10,
                    },
                    {
                        "Month": "Feb - 2018",
                        "Axis": 20,
                    }]
            return data

        except Exception as e:
            pass

    def getRMAChartsData(self, startDateParam=None, endDateParam=None):
        '''
            Function Purpose:
                purpose : this function is used to get the data for the "RMA Charts"
            Function Parameters:
                startDateParam (string) : '07/2018'
                endDateParam (string) : '07/2018'
            Function Return Value:
                return value : this function return list where list consists of dictionary.
                Example:
                    [{
                        "Month": "Jan - 2018",
                        "Sensity Fixure": 0,
                        "Video Nodes":20
                    },
                    {
                        "Month": "Feb - 2018",
                        "Sensity Fixure": 30,
                        "Video Nodes":25
                    }]
        '''
        try:
            data = [{
                        "Month": "Jan - 2018",
                        "Sensity Fixure": 0,
                        "Video Nodes": 20
                    },
                    {
                        "Month": "Feb - 2018",
                        "Sensity Fixure": 25,
                        "Video Nodes": 30
                    },
                    {
                        "Month": "Mar - 2018",
                        "Sensity Fixure": 10,
                        "Video Nodes":25
                    }]
            return data

        except Exception as e:
            pass

    def getProactiveReactiveData(self, startDateParam=None, endDateParam=None):
        '''
            Function Purpose:
                purpose : this function is used to get the data for the "Proactive V/S Reactive"
            Function Parameters:
                startDateParam (string) : '07/2018'
                endDateParam (string) : '07/2018'
            Function Return Value:
                return value : this function return list where list consists of dictionary.
                Example:
                    [{
                        "Month": "Jan - 2018",
                        "Customer/Partner": 10,
                        "Sensity/einfochips":20
                    },
                    {
                        "Month": "Feb - 2018",
                        "Customer/Partner": 30,
                        "Sensity/einfochips":40
                    }]
        '''
        try:
            data = [{
                        "Month": "Jan - 2018",
                        "Customer/Partner": 10,
                        "Sensity/einfochips":20
                    },
                    {
                        "Month": "Feb - 2018",
                        "Customer/Partner": 30,
                        "Sensity/einfochips":40
                    }]
            return data

        except Exception as e:
            pass

        ''' Stub Code Over '''

