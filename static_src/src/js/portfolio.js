import '../less/portfolio.less';

import Vue from 'vue'
import Portfolio from './Portfolio.vue'

Vue.config.productionTip = false;
//Vue.config.delimiters = ['[[', ']]'];

new Vue({
  //delimiters: ['[[', ']]'],
  el: '#portfolio',
  template: '<Portfolio/>',
  components: { Portfolio }
});

