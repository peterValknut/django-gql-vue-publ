<template>
    <div class="page">
        <h1>This is a Kartoteka page</h1>

        <h3>{{ organization.fullName }}</h3>
        <div>
        <v-text-field v-model="inn" required label="Paste in an INN" @keyup.enter="load_organization=true" />
        <v-btn ripple color="primary" @click="load_organization=true">Search</v-btn>
        </div>
        <v-divider
                class="mx-4"
                :inset="inset"
                vertical
        ></v-divider>
            <v-data-table
                    :loading= "$apollo.queries.organization.loading" loading-text="Loading... Please wait"
                    :headers="headers_top"
                    :items="org_info"
                    hide-default-header
                    hide-default-footer
                    class="elevation-1"
            ></v-data-table>
        <v-divider
                class="mx-4"
                :inset="inset"
                vertical
        ></v-divider>

        <template>
            <v-data-table
                    :loading= "$apollo.queries.organization.loading" loading-text="Loading... Please wait"
                    :headers="headers"
                    :items="org_decreases"
                    :items-per-page="5"
                    class="elevation-1"
            ></v-data-table>
        </template>

<!--        <div v-for="i in   organization" :key="i.id">-->
<!--            <ul>-->
<!--                <li>-->
<!--                    <strong>{{i.year}}</strong>:<span>{{i.code}}</span>:<span>{{i.value}}</span>-->
<!--                </li>-->
<!--            </ul>-->
<!--        </div>-->

        <v-divider
                class="mx-4"
                :inset="inset"
                vertical
        ></v-divider>
        <div>
        <v-btn ripple color="primary" @click="load_contracts=true">Load calculated contracts</v-btn>
        </div>
        <v-divider
                class="mx-4"
                :inset="inset"
                vertical
        ></v-divider>
        <template>
            <v-data-table
                    :loading= "$apollo.queries.contracts.loading" loading-text="Loading... Please wait"
                    :headers="headers_contracts"
                    :items="org_contracts"
                    :items-per-page="5"
                    class="elevation-1"
            ></v-data-table>
        </template>
<!--        <template>-->
<!--                <div v-for="i in   contracts" :key="i.id">-->
<!--                    <ul>-->
<!--                        <li>-->
<!--                            <strong>{{i}}</strong>-->
<!--                        </li>-->
<!--                    </ul>-->
<!--                </div>-->
<!--        </template>-->
    </div>
</template>

<script>
    import gql from 'graphql-tag'

    //   const TaskQuery = gql`
    // query{
    //   grants (search:{name:"Нужна"}) {
    //     inn
    //     organizationName
    //     addressString
    //     grantSum
    //     email
    //   }
    // }
    //     `;

    const KartotekaQuery = gql(`
query($inn: String!){
  organization (search:{inn: $inn}) {
    inn,
    status,
    fullName,
    shortName,
    address,
    director,
    phones,
    ogrn,
    okopfName,
    regDate,
    decreases{
      year,
      code,
      measure,
      value
    }
  }
}
    `);
    const KartotekaContractsQuery = gql(`
query($inn: String!){
  contracts (search:{inn:$inn}) {
      role,
      year,
      value
  }
}
    `);

    export default {
        name: 'Kartoteka',
        data() {
            return {
                // Initialize your apollo data
                organization: '',
                contracts: [],
                load_organization: false,
                load_contracts: false,
                inn: '',
                headers_top: [
                    {text: 'Param', value: 'param'},
                    {text: 'Value', value: 'value'},
                ],
                headers: [
                    {
                        text: 'Year',
                        align: 'left',
                        sortable: false,
                        value: 'year',
                    },
                    {text: 'Code', value: 'code'},
                    {text: 'Code Name', value: 'name'},
                    {text: 'Measure', value: 'measure'},
                    {text: 'Value', value: 'value'},
                ],
                headers_contracts: [
                    {
                        text: 'Role',
                        align: 'left',
                        sortable: false,
                        value: 'role',
                    },
                    {text: '2014', value: '2014'},
                    {text: '2015', value: '2015'},
                    {text: '2016', value: '2016'},
                    {text: '2017', value: '2017'},
                    {text: '2018', value: '2018'},
                ],
            }
        },
        apollo: {
            organization() {
                return {
                    query: KartotekaQuery,
                    variables() {
                        return {
                            inn: this.inn
                        }
                    },
                    result(result) {
                        this.load_organization=false;
                    },
                    skip() {
                        return !this.load_organization;
                    }
                }

            },
            contracts() {
                return {
                    query: KartotekaContractsQuery,
                    variables() {
                        return {
                            inn: this.inn
                        }
                    },
                    result(result) {
                        this.load_contracts=false;
                    },
                    skip() {
                        return !this.load_contracts;
                    }

                }
            }
        },
        computed: {
            org_info() {
                const new_keys_card = {
                    'inn': 'ИНН',
                    'status': 'Статус',
                    'fullName': 'Полное наименование',
                    'shortName': 'Короткое наименование',
                    'address': 'Адрес',
                    'director': 'Руководитель',
                    'phones': 'Телефон',
                    'ogrn': 'ОГРН',
                    'okopfName': 'ОКОПФ',
                    'regDate': 'Дата регистрации',
                };

                let org_list = [];
                for (let k in this.organization) {
                    if (k !== '__typename' && k !== 'decreases') {
                        org_list.push({'param': new_keys_card[k], 'value': this.organization[k]});
                    }
                }
                return org_list;
            },
            org_decreases() {
                const new_keys_decreses = {
                    '6300': 'Всего использовано средств',
                    '6310': 'Расходы на целевые мероприятия',
                    '6320': 'Расходы на содержание аппарата управления',
                    '6330': 'Приобретение основных средств, инвентаря и иного имущества',
                    '6350': 'Прочие'
                };
                let decrease_cont=[];
                var decreases = this.organization['decreases'];
                for (let k in decreases) {
                    decreases[k]['name'] = new_keys_decreses[decreases[k]['code']];
                    decrease_cont.push(decreases[k]);
                }
                return decrease_cont;
            },
            org_contracts() {
                let contracts_cont=[];
                for (let k in this.contracts) {
                    if (k !== '__typename') {
                        contracts_cont.push({
                            'role': this.contracts[k]['role'],
                            'year': this.contracts[k]['year'],
                            'value': this.contracts[k]['value']
                        });
                    }
                }
                // workaround
                let contracts_cont2 = [];
                let supplier = contracts_cont.filter(item => item.role === 'supplier');
                let customer = contracts_cont.filter(item => item.role === 'customer');
                let supplier_obj = {'role':'Поставщик'};
                let customer_obj = {'role':'Заказчик'};
                for (let k in supplier) {
                    supplier_obj[supplier[k]['year']] = supplier[k]['value']
                }
                for (let k in customer) {
                    customer_obj[customer[k]['year']] = customer[k]['value']
                }
                contracts_cont2.push(supplier_obj);
                contracts_cont2.push(customer_obj);
                // end workaround

                return contracts_cont2;
            },

        },
        // methods: {
        //     loadOrganization() {
        //         this.organization = this.$apollo.query({
        //             query: KartotekaQuery,
        //             variables() {
        //             return {
        //                 inn: this.inn
        //             }
        //         }});
        //         this.load_organization = true;
        //     },
        //     loadContracts() {
        //         this.contracts = this.$apollo.query({
        //             query: KartotekaContractsQuery,
        //             variables() {
        //                 return {
        //                     inn: this.inn
        //                 }
        //             }
        //         });
        //         this.load_contracts = true;
        //     },
        // },



    }

</script>

<style scoped>
    input
    {
        border: 1px dashed rgba(0,0,0, .4);
    }
    .page {
        padding: 20px;
    }

</style>