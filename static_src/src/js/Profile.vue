<template>
  <div>
    <Hello :greeting="greeting" />
  </div>
</template>

<script>
import Hello from '../components/Hello.vue'

export default {
  components: {
    Hello
  },
  data () {
    return {
      greeting: 'trinity-zhang'
    }
  }
}
</script>

<style>
</style>
