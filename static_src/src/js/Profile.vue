<template>
  <div>
  </div>
</template>

<script>
import Hello from '../components/Hello.vue'
import MediumEditor from '../components/MediumEditor.vue'
//import MediumEditor from 'medium-editor'

//var editor = new MediumEditor('.cool-editor');

export default {
  components: {
    //Hello,
    MediumEditor
  },
  data () {
    return {
      //greeting: 'Welcome to the cool-editor to start writing...'
    }
  }
}
</script>

<!--style lang="css">
@import "~medium-editor/dist/css/medium-editor.css";
@import "~medium-editor/dist/css/themes/default.min.css";
</style-->
