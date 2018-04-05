<template>
  <div class="style-msg" :class="classObject" :style="styleObject">
    <div class="sb-msg">
      <i :class="alertData.iconClass"></i><strong>{{ alertData.title }}</strong>
      {{ alertData.content }}
    </div>
		<button v-if="alertData.isRemovable" type="button" class="close" data-dismiss="alert" aria-hidden="true" >&times;</button>
  </div>
</template>

<script>
export default {
  props: {
    alertData: {
      type: Object
    }
  },
  computed: {
    classObject () {
      let classMapping = {
        'info': 'infomsg',
        'alert': 'alertmsg',
        'success': 'successmsg',
        'error': 'errormsg',
        'black': 'style-msg-light',
        'grey': ''
      };
      //we should consider the abnormal key case here
      return classMapping[this.alertData.theme]
    },
    styleObject () {
      let styleMapping = {
        'info': '',
        'alert': '',
        'success': '',
        'error': '',
        'black': 'background-color: #333;',
        'grey': 'background-color: #EEE;'
      };
      return styleMapping[this.alertData.theme]
    }
  }
}
</script>

<style>
</style>
