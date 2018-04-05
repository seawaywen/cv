<template>
  <div class="tabs tabs-alt clearfix" id="tab-7">
    <ul class="tab-nav clearfix">
      <li v-for="(item, index) in tabData">
        <a :href="'#' + item.id"><i :class="item.icon" class="norightmargin"></i>{{ item.title }}</a>
      </li>
    </ul>

    <div class="tab-container">
      <div v-for="(item, index) in tabData"  class="tab-content clearfix" :id="item.id">
        {{ item.content }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    tabData: {
      type: Array,
      require: true
    }
  },
  computed: {
  }
}
</script>

<style>
</style>
