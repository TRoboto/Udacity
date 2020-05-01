const config = require('./config');

/* Start the MQTT server */
mqtt = require('./mqtt');
mqtt.configure(config);
mqtt.start();