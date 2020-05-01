const WS_HOST = window.location.hostname.split(".")[0].slice(0,-5)

export const SETTINGS = {
  CAMERA_FEED_SERVER: "https://" + WS_HOST + "-3004.udacity-student-workspaces.com",
  CAMERA_FEED_WIDTH: 852,
  MAX_POINTS: 10,
  SLICE_LENGTH: -10,
};

export const LABELS = {
  START_TEXT: "Click me! ",
  END_TEXT: "The count is now: ",
};

export const HTTP = {
  CAMERA_FEED: `${SETTINGS.CAMERA_FEED_SERVER}/facstream.mjpeg`, // POST
};

export const MQTT = {
  MQTT_SERVER: "wss://" + WS_HOST + "-3002.udacity-student-workspaces.com",
  TOPICS: {
    PERSON: "person", // how many people did we see
    DURATION: "person/duration", // how long were they on frame
  },
};
