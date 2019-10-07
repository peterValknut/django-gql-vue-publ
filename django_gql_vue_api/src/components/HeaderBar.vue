<template>
    <div>

        <v-navigation-drawer
                v-model="drawer"
                app

        >
            <v-list dense>
                    <v-list-item to="/kartoteka" >
                        <v-list-item-action>
                            <v-icon>mdi-checkbox-multiple-blank-circle</v-icon>
                        </v-list-item-action>
                        <v-list-item-content>
                            <v-list-item-title>Kartoteka</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>

                <v-list-item to="/grants" >
                    <v-list-item-action>
                        <v-icon>mdi-plus-outline</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>President Grants</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>

                <v-list-item @click="$router.push('/about')">
                    <v-list-item-action>
                        <v-icon>mdi-contact_mail</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Contact</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>

        <v-app-bar
                app
                dark
                color="primary"
        >
            <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-toolbar-title>Application</v-toolbar-title>
        </v-app-bar>
    </div>


</template>

<script>
    export default {
        name: "HeaderBar",
        data: () => ({
            drawer: false
        })
    }
</script>

<style scoped>

</style>