import styles from '../css/main.css';
var config = require('./config.json')

module.exports = function() {
  var greet = document.createElement('div');
  greet.textContent = "Hi there and greetings! [from webpack@memodir] (" + config.greetText + ")"
  greet.classList.add(styles.red)
  return greet;
};
