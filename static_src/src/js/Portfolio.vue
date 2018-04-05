<template>
  <div>
    <h2>Portfolio</h2>
    <hello :greeting="greeting" />

    <message-box :messageData='messageData' />

    <div class='divider' />
    <alert :alertData='alertData' />

    <div class="line"></div>

    <tab :tabData='tabData' />

  </div>
</template>

<script>
import Hello from '../components/Hello.vue'
import MessageBox from '../components/MessageBox.vue'
import Alert from '../components/Alert.vue'
import Tab from '../components/Tab.vue'

export default {
  components: {
    Hello, MessageBox, Alert, Tab
  },
  data () {
    return {
      greeting: 'kelvin-li',

      messageData: {
        theme: 'black', //'black', 'red', 'green'
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
      },
      tabData: {
        type: 'horizontal', //'vertical' or 'horizontal'
        contentList: [
          {
            title: '',
            content: 'v- 前缀作为一种视觉提示，用来识别模板中 Vue 特定的特性。当你在使用 Vue.js 为现有标签添加动态行为 (dynamic behavior) 时，v- 前缀很有帮助，然而，对于一些频繁用到的指令来说，就会感到使用繁琐。同时，在构建由 Vue.js 管理所有模板的单页面应用程序 (SPA - single page application) 时，v- 前缀也变得没那么重要了。因此，Vue.js 为 v-bind 和 v-on 这两个最常用的指令，提供了特定简写：',
            icon: 'icon-home2',
            id: 'tab-24'

          },
          {
            title: 'name1',
            content: 'my name is Kelvin',
            icon: '',
            id: 'tab-25'

          },
          {
            title: 'name2',
            content: 'my name is Trinity',
            icon: '',
            id: 'tab-26'
          }
        ]
      }
    }
  }
}
</script>

<style>
</style>
