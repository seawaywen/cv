import foxImage from '../images/fox.png'
import less from '../less/blog.less';

const greeter = require('./Greeter.js');

//document.body.appendChild(greeter());

var foxImg = new Image();
foxImg.src = foxImage;
foxImg.width = 200;

var element = document.createElement('div');
element.appendChild(foxImg);
//document.body.appendChild(element)