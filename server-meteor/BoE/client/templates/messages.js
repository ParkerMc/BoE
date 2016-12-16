function messages() {
  return Messages.find({}, { sort: { 'time': 1 } });
}

function time(time) {
  return moment(time).format("HH:mm:ss");
}
Template.messages.helpers({
  messages: messages,
  time: time
});
