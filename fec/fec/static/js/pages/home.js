'use strict';

var homepageEvents = require('../modules/home-events');

// accessible tabs for alt sidebar
require('../vendor/tablist').init();

// Home Page: Events and deadlines
new homepageEvents.HomepageEvents();
