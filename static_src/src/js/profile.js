import '../less/portfolio.less';

import Vue from 'vue'
import Profile from './Profile.vue'

Vue.config.productionTip = false;
//Vue.config.delimiters = ['[[', ']]'];


new Vue({
  //delimiters: ['[[', ']]'],
  el: '#profile',
  template: '<Profile/>',
  components: { Profile }
});

