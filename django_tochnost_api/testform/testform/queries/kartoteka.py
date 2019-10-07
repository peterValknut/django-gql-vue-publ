import graphene

from testform.scripts.kartoteka import Kartoteka, KartotekaInfo

# YEARS = ['2014', '2015', '2016', '2017']
CODES = ['6300','6310','6320','6330','6350']

class KartotekaOrganizationDecreaseType(graphene.ObjectType):
    year = graphene.String()
    code = graphene.String()
    measure = graphene.String()
    value = graphene.String()

class KartotekaOrganizationContractsType(graphene.ObjectType):
    year = graphene.String()
    role = graphene.String()
    value = graphene.String()

class KartotekaOrganization(graphene.ObjectType):
    fullName = graphene.String()
    shortName = graphene.String()
    address = graphene.String()
    inn = graphene.String()
    director = graphene.String()
    ogrn = graphene.String()
    okpo = graphene.String()
    kpp = graphene.String()
    status = graphene.String()
    phones = graphene.String()
    okato = graphene.String()
    reg_date = graphene.String()
    okopf_code = graphene.String()
    okopf_name = graphene.String()
    decreases = graphene.List(KartotekaOrganizationDecreaseType)
    contracts = graphene.List(KartotekaOrganizationContractsType)
    def resolve_decreases(self, info, **kwargs):
        try:
            dec = []
            kart = KartotekaInfo()
            kart.searchbyRequisite(self['inn'])
            kart.getCard()
            years = kart.getBoYearsList()
            years = years.get('year', '')
            for year in years:
                codes_bo = kart.getBoYear(year, CODES)

                for k, v in codes_bo.items():
                    if k != 'measure' and k != 'year':
                        cont = {}
                        cont['year'] = year
                        cont['measure'] = codes_bo['measure']
                        cont['code'] = k
                        cont['value'] = v
                        dec.append(cont)
            return dec
        except Exception as e:
            print(e)
            return None

    def resolve_contracts(self, info, **kwargs):
        try:
            kart = Kartoteka()
            kart.searchbyRequisite(self['inn'])
            kart.getAccounting()
            response = kart.data
            cont_contracts = []
            for k, v in response.items():
                if 'customer' in str(k) or 'supplier' in str(k):
                    splitted = str(k).split('_')
                    cont = {}
                    cont['year'] = splitted[2]
                    cont['role'] = splitted[0]
                    cont['value'] = v
                    cont_contracts.append(cont)
            return cont_contracts

        except Exception as e:
            print(e)
            return None




class Input(graphene.InputObjectType):
    inn = graphene.String()

class KartotekaQuery(graphene.ObjectType):
    organization = graphene.Field(KartotekaOrganization,search=Input(required=True))
    contracts = graphene.List(KartotekaOrganizationContractsType,search=Input(required=True))
    def resolve_organization(self, info, search):
        if search.inn is not None:
            try:
                kart = KartotekaInfo()
                kart.searchbyRequisite(search.inn)
                kart.getCard()
                response = kart.parseResponse()
                return response
            except Exception as e:
                print(e)
                return None
        return None

    def resolve_contracts(self,info, search):
        if search.inn is not None:
            try:
                kart = Kartoteka()
                kart.searchbyRequisite(search.inn)
                kart.getAccounting()
                response = kart.data
                cont_contracts=[]
                for k,v in response.items():
                    if 'customer' in str(k) or 'supplier' in str(k):
                        splitted = str(k).split('_')
                        cont = {}
                        cont['year'] = splitted[2]
                        cont['role'] = splitted[0]
                        cont['value'] = v
                        cont_contracts.append(cont)
                return cont_contracts

            except Exception as e:
                print(e)
                return None
        return None

