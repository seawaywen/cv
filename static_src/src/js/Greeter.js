import styles from '../css/main.css';
var config = require('./config.json');

module.exports = function() {
  var greet = document.createElement('div');
  greet.textContent = "Hmmmm, Hi there and greetings, ladies! \n\n HEROs \\n\\n [from webpack@memodir] (" + config.greetText + ")"
  //greet.classList.add(styles.blue);
  console.log('NY updates log');
  console.log('Tokyo updates log');
  console.log('Sydney updates log');
  return greet;
};
