<template>
  <div id="greeting">
    <p>Hello, {{ greeting }} </p>
  </div>
</template>

<script>
export default {
  name: 'hello',
  props: {
    greeting: {
      type: String,
      default: 'no-one'
    }
  }
}
</script>

<style>
#greeting {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
