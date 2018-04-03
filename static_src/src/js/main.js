import less from '../less/blog.less';

import Vue from 'vue'
import Hello from './Hello'

const greeter = require('./Greeter.js');

//document.body.appendChild(greeter());

Vue.config.productionTip = false;

var app = new Vue({
  el: '#app',
  template: '<Hello/>',
  components: { Hello },
  data: {
    greeting: 'kelvin'
  }
});

