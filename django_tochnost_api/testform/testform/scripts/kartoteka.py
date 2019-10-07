from zeep import Client
from zeep.transports import Transport
from zeep import helpers
from datetime import date

from dotenv import load_dotenv
load_dotenv()

import os



cred = {
    'login': os.getenv("KARTOTEKA_PASS"),
    'password': os.getenv("KARTOTEKA_LOGIN")
}
transport = Transport()
transport.session.headers['User-Agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

# base
class Kartoteka:
    def __init__(self):
        client = Client(wsdl='http://api.kartoteka.ru/auth/v3/soap/auth.wsdl',transport=transport)
        r = client.service.login(cred)
        self.SESSIONID = r['id']
        self.client = Client(wsdl='http://api.kartoteka.ru/search/v3/soap/search.wsdl',transport=transport)
        self.client.set_default_soapheaders({'sessionId': self.SESSIONID})
        self.years=[2014,2015,2016,2017,2018]
        self.numPages = None
        self.data = {}
        self.companyData= {}

    def searchbyRequisite(self,inn):
        r = self.client.service.searchByRequisite(request={
            'detailSearchRequest':{
                'inn':inn
            }
        })
        companyData = helpers.serialize_object(r, target_cls=dict)
        try:
            companyData=companyData['rows']['_value_1'][0]['orgMainInfo']
            self.data['fullName'] = companyData['fullName']
            self.data['shortName'] = companyData['shortName']
            self.data['addressEgrul'] = companyData['addressEgrul']
            self.data['inn'] = companyData['inn']
            self.data['hash'] = companyData['hash']
        except Exception as e:
            raise e


    def getAccounts(self,page):
        self.ImportantFacts=self.client.bind(service_name='ImportantFatcs')
        hash = self.data['hash']
        r = self.ImportantFacts.getGovernmentContracts(request={
            'cardHash': hash,
            'page': str(page),
            'rowsPerPage':'100' #100 cap
        })
        response = helpers.serialize_object(r, target_cls=dict)
        return response

    def parseAccountingResponse(self,r):
        if self.numPages is None:
            self.numPages = int(r['pageCount']) - 1
        contracts = r['contracts']['contract']
        for year in self.years:
            for contract in contracts:
                if contract['signDate'].year == year:
                    if contract['customer'] == self.data['shortName']:
                        self.data['customer_summ_'+str(year)] += contract['summ']
                    else:
                        self.data['supplier_summ_' + str(year)] += contract['summ']


    def getAccounting(self):
        for year in self.years:
            self.data['customer_summ_' + str(year)] = int()
            self.data['supplier_summ_' + str(year)] = int()
        num = 1
        try:
            self.parseAccountingResponse(self.getAccounts(num))
            for i in range(self.numPages):
                num += 1
                self.parseAccountingResponse(self.getAccounts(num))
        except Exception as e:
            print(e)
            pass
        self.numPages = None

    def getSingleInn(self):
        page = 1
        cont = []
        try:
            self.parseSingleInn(self.getAccounts(page))
            for i in range(self.numPages):
                page += 1
                c = self.parseSingleInn(self.getAccounts(page))
                if c:
                    cont.extend(c)
        except Exception as e:
            print(e)
            pass
        self.numPages = None
        return cont

    def parseSingleInn(self, r):
        if self.numPages is None:
            self.numPages = int(r['pageCount']) - 1
        contracts = r['contracts']['contract']
        cont = []
        for year in self.years:
            for contract in contracts:
                if contract['signDate'].year == year:
                    if contract['customer'] == self.data['shortName']:
                        t = {
                            'year':year,
                            'amount':contract['summ'],
                            'number': contract.get('number',''),
                            'regNum': contract.get('regNum',''),
                            'signDate': date.strftime(contract.get('signDate', ''),'%Y-%m-%d') if 'signDate' in contract else '',
                            'supplier' : contract.get('supplier', '')[0] if 'supplier' in contract else '',
                        }
                        cont.append(t)
        if cont:
            return cont



# Card and Fin endpoints
class KartotekaInfo(Kartoteka):

    def searchbyRequisite(self,inn):
        r = self.client.service.searchByRequisite(request={
            'detailSearchRequest':{
                'inn':inn
            }
        })
        companyData = helpers.serialize_object(r, target_cls=dict)
        try:
            companyData=companyData['rows']['_value_1'][0]['orgMainInfo']
            self.data['hash'] = companyData['hash']
            self.data['director'] = ''
            director = companyData.get('control',None)
            if director is not None:
                name = director.get('name','')
                post = director.get('post','')
                self.data['director'] = name + ' ' + post
        except Exception as e:
            raise e

    def getCard(self):
        hash = self.data['hash']
        self.Card = self.client.bind(service_name='Card')
        r = self.Card.getCardInfo(hash=hash)
        response = helpers.serialize_object(r, target_cls=dict)
        self.org_info = response

    def getBoYearsList(self):
        hash = self.data['hash']

        self.Bo = self.client.bind(service_name='Fin')
        r = self.Bo.getBoYears(
            request={
                'cardHash': hash
            }
        )
        response = helpers.serialize_object(r, target_cls=dict)
        return response

    def getBoYear(self,year,codes):
        hash = self.data['hash']

        self.Bo = self.client.bind(service_name='Fin')
        t = {}
        t['year'] = year
        t['measure'] = None
        for code in codes:
            t[code] = None
        try:
            r = self.Bo.getBoYearReport(
                request={
                    'cardHash': hash,
                    'year': year
                }
            )
            response = helpers.serialize_object(r, target_cls=dict)
            t = self.parse_bo_decreases(response,codes,t)
        except Exception as e:
            print(e)
            pass
        return t

    def parse_bo_decreases(self,data,codes,t):

        try:
            t['measure'] = data['bo']['rosstat']['report']['boReportAfter2011']['infoBBO']['unit']
            decreases = data['bo']['rosstat']['report']['boReportAfter2011']['form6']['decreases']['decrease']
            for d in decreases:
                for code in codes:
                    if d['num'] == int(code):
                        t[code] = d.get('current',None)

        except Exception as e:
            print(e)
            pass
        return t

    def parseResponse(self):
        r = self.org_info['orgCard']
        t = {}
        t['inn'] = r['inn']
        t['ogrn'] = r['ogrn']
        t['okpo'] = r.get('okpo',None)
        t['kpp'] = r.get('kpp', None)
        t['status'] = r.get('status', None)
        t['fullName'] = r.get('fullName', '')
        t['shortName'] = r.get('shortName', None)
        t['address'] = r.get('address', '')
        t['phones'] = r.get('phones', None)
        t['okato'] = r.get('okato', None)
        t['director'] = self.data['director']
        t['reg_date'] = date.strftime(r.get('regDate', ''),'%Y-%m-%d') if 'regDate' in r else ''
        t['okopf_code'] = ''
        t['okopf_name'] = ''
        for k,v in r.items():
            if 'okopf' in k and v is not None:
                t['okopf_code'] = v.get('code','')
                t['okopf_name'] = v.get('name','')
        return t
