<template>
  <div class="tabs tabs-responsive clearfix" :class="layoutType">
    <ul class="tab-nav clearfix">
      <li v-for="(item, index) in tabData.contentList">
        <a :href="'#' + item.id">
          <i v-if="item.icon !== ''" :class="item.icon" class="norightmargin"></i>
          <span v-if="item.title != ''">{{ item.title }}</span>
        </a>
      </li>
    </ul>

    <div class="tab-container">
      <div v-for="(item, index) in tabData.contentList" class="tab-content clearfix" :id="item.id">
        {{ item.content }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    tabData: {
      type: Object,
      require: true
    }
  },
  computed: {
    layoutType () {
      let mappingType = {
        'horizontal': 'tabs-alt' ,
        'vertical': 'side-tabs'
      };
      // if the type is not either 'horizontal' or 'vertical', return the horizontal by default
      if (this.tabData.type === null || this.tabData.type === '' ||
          !Object.keys(mappingType).includes(this.tabData.type))
        return 'tabs-alt';
      return mappingType[this.tabData.type]
    }
  }
}
</script>

<style>
</style>
