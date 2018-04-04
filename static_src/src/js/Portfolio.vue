<template>
  <div>
    <h2>Portfolio</h2>
    <hello :greeting="greeting" />

    <message-box :messageData='messageData' />

    <alert :alertData='alertData' />

  </div>
</template>

<script>
import Hello from '../components/Hello.vue'
import MessageBox from '../components/MessageBox.vue'
import Alert from '../components/Alert.vue'

export default {
  components: {
    Hello, MessageBox, Alert
  },
  data () {
    return {
      greeting: 'kelvin-li',

      messageData: {
        theme: 'green', //'black', 'red', 'green'
        title: '本次会议需要解决的问题',
        contentList: [
          '操作元素的 class 列表和内联样式是数据绑定的一个常见需求。因为它们都是属性，',
          '所以我们可以用 v-bind 处理它们：只需要通过表达式计算出字符串结果即可。不过，',
          '字符串拼接麻烦且易错。因此，在将 v-bind 用于 class 和 style 时，Vue.js 做了专门的增强。',
          '表达式结果的类型除了字符串之外，还可以是对象或数组。\n'
        ]
      },
      alertData: {
        theme: 'info', //
        title: '通知',
        content: 'Element, a Vue 2.0 based component library for developers, designers and product managers',
        isRemovable: true,
        iconClass: 'icon-info-sign' //'icon-remove', 'icon-info-sign', 'icon-warning-sign', 'icon-question-sign'
      }
    }
  }
}
</script>

<style>
</style>
