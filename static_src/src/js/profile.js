const greeter = require('./Greeter.js');

if (module.hot) {
    module.hot.accept('./Greeter.js', function(){
        console.log('Accepting the updated Greeter module!');
    })
}

document.body.appendChild(greeter());
