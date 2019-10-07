import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
  icons: {
    iconfont: 'mdi',
  },
  theme: {
    dark : false,
    themes: {
      light: {
        primary: '#009688',
        secondary: '#e91e63',
        accent: '#4caf50',
        error: '#f44336',
        warning: '#ffc107',
        info: '#673ab7',
        success: '#ff5722'
      }
    }
  }
});
