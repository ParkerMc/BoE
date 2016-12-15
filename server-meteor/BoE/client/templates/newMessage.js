function createMessage(evt) {
  Messages.insert({
    message: evt.target.message.value,
    time: new Date()
  });
  evt.target.message.value = '';
  return false;
}
Template.newMessage.events({
  "submit form": createMessage
});
