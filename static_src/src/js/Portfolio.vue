<template>
  <div>
    <h2>Portfolio</h2>
    <hello :greeting="greeting" />
    <message-box :theme='theme' :title='title' :contentList='contentList' />
    hahaho
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
      theme: 'green', //'black', 'red', 'green'
      greeting: 'kelvin-li',
      title: '本次会议需要解决的问题',
      contentList: [
        '操作元素的 class 列表和内联样式是数据绑定的一个常见需求。因为它们都是属性，',
        '所以我们可以用 v-bind 处理它们：只需要通过表达式计算出字符串结果即可。不过，',
        '字符串拼接麻烦且易错。因此，在将 v-bind 用于 class 和 style 时，Vue.js 做了专门的增强。',
        '表达式结果的类型除了字符串之外，还可以是对象或数组。\n'
      ],
      alertData: {
        theme: 'info', //
        title: '',
        content: 'hahahahhhahahah',
        isRemovable: true,
        iconClass: 'icon-remove'
      }
    }
  }
}
</script>

<style>
</style>
