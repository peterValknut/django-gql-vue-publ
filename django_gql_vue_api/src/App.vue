<template>
  <v-app>

    <SidebarDrawer/>
    <HeaderBar/>
    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
// import Kartoteka from './components/kartoteka';
// import SidebarDrawer from './components/SidebarDrawer';
import HeaderBar from './components/HeaderBar';
import router from './router'

export default {
  name: 'App',
  router,
  components: {


    HeaderBar,

  },
  data: () => ({
    //
  }),
};
</script>
