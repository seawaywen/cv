<template>
</template>

<script>
  require('imports-loader?define=>false&exports=>false!blueimp-file-upload/js/jquery.fileupload.js');

  import MediumEditor from 'medium-editor'
  import MediumInsert from 'medium-editor-insert-plugin'

  // A workaround for the console error:
  // TypeError: undefined is not an object (evaluating 'window.MediumInsert.Templates')
  window.MediumInsert = MediumInsert.MediumInsert;

  let editor = new MediumEditor('.cool-editor', {
    placeholder: {
        text: 'Start your writing...',
        hideOnClick: true
    },
    toolbar: {
      buttons: [
        'bold',
        'italic',
        'underline',
        'strikethrough',
        {
          name: 'h1',
          action: 'append-h2',
          aria: 'header type 1',
          tagNames: ['h2'],
          contentDefault: '<b>H1</b>',
          classList: ['custom-class-h1'],
          attrs: {
            'data-custom-attr': 'attr-value-h1'
          }
        },
        {
          name: 'h2',
          action: 'append-h3',
          aria: 'header type 2',
          tagNames: ['h3'],
          contentDefault: '<b>H2</b>',
          classList: ['custom-class-h2'],
          attrs: {
            'data-custom-attr': 'attr-value-h2'
          }
        },
        'justifyCenter',
        'quote',
        'anchor'
      ]
    }
  });

  $('.cool-editor').mediumInsert({
    editor: editor
  });
</script>

<style lang="css">
@import "~medium-editor/dist/css/medium-editor.min.css";
@import "~medium-editor/dist/css/themes/default.min.css";
@import "~medium-editor-insert-plugin/dist/css/medium-editor-insert-plugin.min.css";
</style>
