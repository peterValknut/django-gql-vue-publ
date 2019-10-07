import graphene

from testform.scripts.persons import (get_dadata_by_inn,
                                      get_dadata_by_name,
                                      get_sbis_by_name,
                                      get_sbis_by_inn,
                                      get_grants_by_inn,
                                      get_grants_by_name)

from testform.scripts.kartoteka import Kartoteka, KartotekaInfo


class DadataOrganizationType(graphene.ObjectType):
    name = graphene.String()
    inn = graphene.String()
    ogrn = graphene.String()
    region = graphene.String()

class SbisOrganizationType(graphene.ObjectType):
    name = graphene.String()
    inn = graphene.String()
    activity = graphene.String()
    region = graphene.String()
    director = graphene.String()

class GrantType(graphene.ObjectType):
    inn = graphene.String()
    grant_name = graphene.String()
    organization_name = graphene.String()
    address_string  = graphene.String()
    grant_sum  = graphene.String()
    email  = graphene.String()
    project_name = graphene.String()
    project_status = graphene.String()
    total_sum = graphene.String()
    organizations_dadata = graphene.List(DadataOrganizationType)
    def resolve_organizations_dadata(self, info, **kwargs):
        inn = self.inn
        if inn is not None:
            names = get_dadata_by_inn(inn)
            l = []
            for n in names:
                name_t = DadataOrganizationType(**n)
                l.append(name_t)
            return l
        return None


class OrgInput(graphene.InputObjectType):
    name = graphene.String()
    inn = graphene.String()

class OrgsQuery(graphene.ObjectType):
    organizations_dadata = graphene.List(DadataOrganizationType,search=OrgInput(required=False))
    organizations_sbis = graphene.List(SbisOrganizationType,search=OrgInput(required=False))
    grants = graphene.List(GrantType,search=OrgInput(required=False))

    def resolve_organizations_dadata(self, info, search):

        if search.name is not None:
            names = get_dadata_by_name(search.name)
            l = []
            for n in names:
                name_t = DadataOrganizationType(**n)
                l.append(name_t)
            return l
        if search.inn is not None:
            names = get_dadata_by_inn(search.inn)
            l = []
            for n in names:
                name_t = DadataOrganizationType(**n)
                l.append(name_t)
            return l
        return None

    def resolve_organizations_sbis(self, info, search):

        if search.name is not None:
            names = get_sbis_by_name(search.name)
            l = []
            for n in names:
                name_t = SbisOrganizationType(**n)
                l.append(name_t)
            return l
        if search.inn is not None:
            names = get_sbis_by_inn(search.inn)
            l = []
            for n in names:
                name_t = SbisOrganizationType(**n)
                l.append(name_t)
            return l
        return None

    def resolve_grants(self,info,search):
        if search.name is not None:
            names = get_grants_by_name(search.name)
            l = []
            for n in names:
                name_t = GrantType(**n)
                l.append(name_t)
            return l
        if search.inn is not None:
            names = get_grants_by_inn(search.inn)
            l = []
            for n in names:
                name_t = GrantType(**n)
                l.append(name_t)
            return l
        return None
