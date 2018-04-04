<template>
  <div class="style-msg2" v-bind:class="classObject" v-bind:style="styleObject">
    <div class="msgtitle">
      <i class="icon-pencil2"></i>
      {{ title }}
    </div>
    <div class="sb-msg">
      <ul>
        <li v-for="(item, index) in contentList">
          {{ item }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    theme: {
      type: String,
      //'grey','black', 'red', 'green'
      default: 'grey'
    },
    title: {
      type: String,
      default: 'Topic'
    },
    contentList: {
      type: Object,
      default: []
    }
  },
  computed: {
    classObject () {
      let classMapping = {
        'red': 'errormsg',
        'green': 'successmsg',
        'black': 'style-msg-light',
        'grey': ''
      };
      return classMapping[this.theme]
    },
    styleObject () {
      let styleMapping = {
        'red': '',
        'green': '',
        'black': 'background-color: #444;',
        'grey': 'background-color: #EEE;'
      };
      return styleMapping[this.theme]
    }
  }
}
</script>

<style>
</style>
