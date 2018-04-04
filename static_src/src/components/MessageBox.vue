<template>
  <div class="style-msg2" :class="classObject" :style="styleObject">
    <div class="msgtitle">
      <i class="icon-pencil2"></i>
      {{ messageData.title }}
    </div>
    <div class="sb-msg">
      <ul>
        <li v-for="(item, index) in messageData.contentList">
          {{ item }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'message-box',
  props: {
    messageData: {
      type: Object
    }
    /*
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
      type: Array,
      default: []
    }
    */
  },
  computed: {
    classObject () {
      let classMapping = {
        'red': 'errormsg',
        'green': 'successmsg',
        'black': 'style-msg-light',
        'grey': ''
      };
      return classMapping[this.messageData.theme]
    },
    styleObject () {
      let styleMapping = {
        'red': '',
        'green': '',
        'black': 'background-color: #444;',
        'grey': 'background-color: #EEE;'
      };
      return styleMapping[this.messageData.theme]
    }
  }
}
</script>

<style>
</style>
