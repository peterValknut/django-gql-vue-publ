<template>
    <div class="about">
        <h1>This is a President Grants page</h1>
        <v-divider
                class="mx-4"
                :inset="inset"
                vertical
        ></v-divider>
        <template v-if="grants.length >0">

            <h3 >{{ grants[0]['organizationName']}}</h3>
            <v-divider
                    class="mx-4"
                    :inset="inset"
                    vertical
            ></v-divider>
            <h5>{{ grants[0]['addressString']}}</h5>
            <h5>{{ grants[0]['email']}}</h5>
        </template>
        <v-divider
                class="mx-4"
                :inset="inset"
                vertical
        ></v-divider>
        <div>
        <v-text-field v-model="inn" required label="Paste in an INN" @keyup.enter="load_grants=true" />
        <v-btn ripple color="primary" @click="load_grants=true">Search</v-btn>
        </div>
        <v-divider
                class="mx-4"
                :inset="inset"
                vertical
        ></v-divider>

        <v-data-table
                :loading= "$apollo.queries.grants.loading" loading-text="Loading... Please wait"
                :headers="headers"
                :items="getGrants"
                class="elevation-1"
        ></v-data-table>

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

    const GrantsQuery = gql(`
query ($inn: String!) {
  grants(search: {inn: $inn}) {
    inn
    email
    grantSum
    organizationName
    grantName
    addressString,
    projectName,
    projectStatus,
    totalSum
  }
}
    `);


    export default {
        name: 'Grants',
        data() {
            return {
                // Initialize your apollo data
                full_name: '',
                grants: [],
                load_grants: false,
                inn: '',
                headers: [
                    {
                        text: 'Grant',
                        align: 'left',
                        value: 'grantName',
                    },
                    {text: 'Project', value: 'projectName'},
                    {text: 'Project Status', value: 'projectStatus'},
                    {text: 'Grant amount', value: 'grantSum',width: "10%"},
                    {text: 'Total amount', value: 'totalSum',width: "10%"},
                ],
            }
        },
        apollo: {
            grants() {
                return {
                    query: GrantsQuery,
                    variables() {
                        return {
                            inn: this.inn
                        }
                    },
                    skip() {
                        return !this.load_grants;
                    },
                    result(result) {
                        this.load_grants=false;
                    }
                }

            },
        },
        computed: {
            getGrants() {
                let org_list = [];
                // let grant_obj = {};
                for (let k in this.grants) {
                    org_list.push({
                        'grantName': this.grants[k]['grantName'],
                        'projectName': this.grants[k]['projectName'],
                        'projectStatus': this.grants[k]['projectStatus'],
                        'grantSum': this.grants[k]['grantSum'],
                        'totalSum': this.grants[k]['totalSum'],
                    });
                }

                return org_list;
            },
        },
        // methods: {
        //     loadGrants() {
        //         this.grants = this.$apollo.query({
        //             query: GrantsQuery,
        //             variables() {
        //                 return {
        //                     inn: this.inn
        //                 }
        //             }
        //         });
        //         this.load_grants = true;
        //     },
        // },

    }

</script>

<style scoped>
    input
    {
        border: 1px dashed rgba(0,0,0, .4);
    }
    .about {
        padding: 20px;
    }

</style>